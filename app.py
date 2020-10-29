import asyncio
import os
import time
import uuid
import threading

from flask import Flask, send_file
from flask import request, jsonify
from flask_api import status
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Table, create_engine
from sqlalchemy import create_engine, MetaData, Table, Column

from annotation_pipeline import annotateVideo
from config import Config
import models
from pollingManager import handlePolling

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# db.init_app(app)
# db.create_all()

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

DEFAULT_EXPIRES_IN = 900  # In sec
DEFAULT_POLLING_INTERVAL = 2  # In sec
DEFAULT_PERSISTENT_STATUS = True


@app.route("/annotate", methods=["POST"])
def annotate():
    target = "/".join([APP_ROOT, "toAnnotate"])

    if not os.path.isdir(target):
        os.mkdir(target)

    # Obtain filename
    file = request.files['video']
    filename = file.filename

    # Check for video formats
    if not (".mp4" in file.filename):
        response = {"error_id": "Bad Request", "error_message": "video file missing"}
        return jsonify(response), status.HTTP_400_BAD_REQUEST

    id = uuid.uuid1()
    # Save file
    if file:
        # Adding to datastore/database- temporarily
        video_file = target + '/' + str(id) + '.mp4'
        print("dest:" + target)
        file.save(video_file)

        # Annotate video for emotions
        if 'emo' in request.form:
            emo_annotation = request.form['emo']
        else:
            response = {"error_id": "Bad Request", "error_message": "parameters missing : 'emo' "}
            return jsonify(response), status.HTTP_400_BAD_REQUEST

        if 'behav' in request.form:
            behav_annotation = request.form['behav']
        else:
            response = {"error_id": "Bad Request", "error_message": "parameters missing : 'behav' "}
            return jsonify(response), status.HTTP_400_BAD_REQUEST

        if 'threat' in request.form:
            threat_annotation = request.form['threat']
        else:
            response = {"error_id": "Bad Request", "error_message": "parameters missing : 'emo' "}
            return jsonify(response), status.HTTP_400_BAD_REQUEST

        if 'expires_in' in request.form:
            requested_expiry = request.form['expires_in']
            if (int(requested_expiry) > DEFAULT_EXPIRES_IN):
                # Cannot allow a expires_in more than default
                requested_expiry = DEFAULT_EXPIRES_IN
        else:
            requested_expiry = DEFAULT_EXPIRES_IN


        if 'persistent_status' in request.form:
            persistent_status = request.form['persistent_status']
            persistent_status = persistent_status
        else:
            persistent_status = DEFAULT_PERSISTENT_STATUS


    # Saving task details to database and call annotation
    last_polled_time = int(round(time.time() * 1000))
    hashed_id = str(uuid.uuid4())
    task = models.Tasks(id=hashed_id, themobe_id=str(id), expires_in=requested_expiry,
                        interval=DEFAULT_POLLING_INTERVAL,last_polled_time=last_polled_time,
                        task_status="PROCESSING",download_count=0,persistent_status=persistent_status)
    db.session.add(task)
    db.session.commit()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # asyncio.ensure_future(annotateAsync(APP_ROOT, video_file, emo_annotation, behav_annotation, threat_annotation,str(id)))
    # annotateAsync(APP_ROOT, video_file, emo_annotation, behav_annotation, threat_annotation, str(id))
    annotateVideo(APP_ROOT, video_file, emo_annotation, behav_annotation, threat_annotation, str(id))
    # result=asyncio.ensure_future(annotateAsync(APP_ROOT, video_file, emo_annotation, behav_annotation, threat_annotation,str(id)))
    # Need to be asyncr

    response = {"themobe_id": id, "video": filename, "video_status": "processing", "expires_in": requested_expiry,
                "interval": DEFAULT_POLLING_INTERVAL}
    return jsonify(response)

async def annotateAsync(APP_ROOT, video_file, emo_annotation, behav_annotation, threat_annotation,id):
    # await asyncio.sleep(20)
    print("commited changes")
    task = db.session.query(models.Tasks)
    task = task.filter(models.Tasks.themobe_id == id)
    record = task.one()
    current_time = int(round(time.time() * 1000))
    record.task_status = "ANNOTATED"
    record.download_allocation_time = current_time
    record.download_req_id = str(uuid.uuid4())
    db.session.commit()
    print("commited changes")
    return "sucessfull"

@app.route("/poll")
def polling():
    if 'themobe_id' in request.args:
        id = request.args.get('themobe_id')
        if (db.session.query(models.Tasks).filter_by(themobe_id=id).scalar()) is None:
            response = {"error_id": "Unauthorized Request", "error_message": "'themobe_id' does not exist"}
            return jsonify(response), status.HTTP_401_UNAUTHORIZED

        else:
            # task = models.Tasks.query().filter(models.Tasks.themobe_id == id).first()
            task = db.session.query(models.Tasks)
            task = task.filter(models.Tasks.themobe_id == id)
            record = task.one()
            current_time = int(round(time.time() * 1000))
            interval = record.interval
            last_polled_time = record.last_polled_time
            task_status = record.task_status
            download_req_id = record.download_req_id

            # Update interval when polling is heavy
            if (last_polled_time + interval * 1000 > current_time):
                record.interval = interval + 3
                db.session.commit()
                response = {"error_id": "slow down", "error_message": "heavy polling adding load to endpoint"}
                return jsonify(response), status.HTTP_400_BAD_REQUEST

            if (task_status == "DOWNLOADED" or task_status == "EXPIRED"):
                # update polling
                record.last_polled_time = current_time
                db.session.commit()
                response = {"error_id": "task completed", "error_message": "task already downlaoded or expired."}
                return jsonify(response), status.HTTP_400_BAD_REQUEST

            if (task_status == "PROCESSING"):
                # update polling
                record.last_polled_time = current_time
                db.session.commit()
                response = {"error_id": "task not completed", "error_message": "annotation engine is still processing the video"}
                return jsonify(response), status.HTTP_400_BAD_REQUEST

            if (task_status == "ANNOTATED"):
                # update polling
                record.last_polled_time = current_time
                db.session.commit()
                response = {"download_req_id":download_req_id,"task status": "Annotated","download status": "Downloadable"}
                return jsonify(response), status.HTTP_400_BAD_REQUEST

    else:
        response = {"error_id": "Bad Request", "error_message": "'themobe_id' is missing"}
        return jsonify(response), status.HTTP_400_BAD_REQUEST

# async def annotateVideoAsync(APP_ROOT, video_path, emo_annotation, behav_annotation, threat_annotation, video_id):
#     await asyncio.sleep(10)
#     task = db.session.query(models.Tasks)
#     task = task.filter(models.Tasks.themobe_id == video_id)
#     record = task.one()
#     record.task_status = "ANNOTATED"
#     print("commited change")
#     db.session.commit()
#     # return jsonify({"result": result})
#     return 1
#
def manageDownload(id, APP_ROOT):
    path = "/".join([APP_ROOT, "output"])
    # print(path)
    video = path + '/' + id + '.mp4'

    return send_file(video, as_attachment=True)

@app.route("/download")
def downloadFile():

    if 'download_req_id' in request.args:
        download_req_id = request.args.get('download_req_id')
        if (db.session.query(models.Tasks).filter_by(download_req_id=download_req_id).scalar()) is None:
            response = {"error_id": "Unauthorized Request", "error_message": "'download_req_id' does not exist"}
            return jsonify(response), status.HTTP_401_UNAUTHORIZED

        else:
            # task = models.Tasks.query().filter(models.Tasks.themobe_id == id).first()
            task = db.session.query(models.Tasks)
            task = task.filter(models.Tasks.download_req_id == download_req_id)
            record = task.one()
            task_status = record.task_status
            download_count=record.download_count
            persistent_status=record.persistent_status

            download_allocation_time = record.download_allocation_time
            expires_in = record.expires_in
            current_time = int(round(time.time() * 1000))
            themobe_id = record.themobe_id

            # check for the authenticity of id
            if (download_allocation_time + expires_in*1000 < current_time):
                response = {"error_id": "access denied", "error_message": "'download_req_id' expired."}
                record.task_status = "EXPIRED"
                db.session.commit()
                return jsonify(response), status.HTTP_400_BAD_REQUEST

            if (task_status == "PROCESSING"):
                response = {"error_id": "Bad Request", "error_message": "wrong endpoint. Task is still being processed."}
                return jsonify(response), status.HTTP_400_BAD_REQUEST

            if (task_status == "EXPIRED"):
                response = {"error_id": "Bad Request", "error_message": "Task expired. Try again."}
                return jsonify(response), status.HTTP_400_BAD_REQUEST

            if (task_status == "DOWNLOADED"):
                if(download_count>5):
                    response = {"error_id": "Bad Request", "error_message": "maximum downloads reached."}
                    return jsonify(response), status.HTTP_400_BAD_REQUEST
                else:
                    record.download_count = download_count + 1
                    db.session.commit()
                    if (persistent_status == 0):
                        path = "/".join([APP_ROOT, "output"])
                        annotated_video = path + '/' + themobe_id + '.mp4'

                        original_path = "/".join([APP_ROOT, "toAnnotate"])
                        original_video = original_path + '/' + themobe_id + '.mp4'

                        if os.path.exists(original_video):
                            os.remove(original_video)

                        if os.path.exists(annotated_video):
                            os.remove(annotated_video)

                    return manageDownload(themobe_id, APP_ROOT)

            if(task_status == "ANNOTATED"):
                record.task_status = "DOWNLOADED"
                record.download_count=download_count+1
                db.session.commit()

                if (persistent_status == False):
                    path = "/".join([APP_ROOT, "output"])
                    annotated_video = path + '/' + themobe_id + '.mp4'

                    original_path = "/".join([APP_ROOT, "toAnnotate"])
                    original_video = original_path + '/' + themobe_id + '.mp4'

                    if os.path.exists(original_video):
                        os.remove(original_video)

                    if os.path.exists(annotated_video):
                        os.remove(annotated_video)

                return manageDownload(themobe_id, APP_ROOT)

    else:
        response = {"error_id": "Bad Request", "error_message": "'themobe_id' is missing"}
        return jsonify(response), status.HTTP_400_BAD_REQUEST


if __name__ == "__main__":
    app.run(debug=True)

