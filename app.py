import asyncio
import os
import time
import uuid
import threading

from flask import Flask
from flask import request, jsonify
from flask_api import status
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Table, create_engine
from sqlalchemy import create_engine, MetaData, Table, Column

# from annotation_pipeline import annotateVideoAsync
from annotation_pipeline import annotateVideo
from config import Config
import models
from downloadManager import manageDownload
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


@app.route("/annotate", methods=["POST"])
async def annotate():
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
            if (requested_expiry > DEFAULT_EXPIRES_IN):
                # Cannot allow a expiresin more than default
                requested_expiry = DEFAULT_EXPIRES_IN
        else:
            requested_expiry = DEFAULT_EXPIRES_IN

    # Saving task details to database and call annotation
    task_generated_time = int(round(time.time() * 1000))
    print("init-time" + str(task_generated_time))
    last_polled_time = task_generated_time
    hashed_id = str(uuid.uuid4())
    task = models.Tasks(id=hashed_id, themobe_id=str(id), expires_in=requested_expiry,
                        interval=DEFAULT_POLLING_INTERVAL,
                        task_generated_time=task_generated_time, last_polled_time=last_polled_time,
                        task_status="PROCESSING")
    db.session.add(task)
    db.session.commit()

    # Need to be async
    annotateVideo(APP_ROOT, video_file, emo_annotation, behav_annotation, threat_annotation,video_id)

    response = {"themobe_id": id, "video": filename, "video_status": "processing", "expires_in": requested_expiry,
                "interval": DEFAULT_POLLING_INTERVAL}
    return jsonify(response)

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
            task_generated_time = record.task_generated_time
            expires_in = record.expires_in
            current_time = int(round(time.time() * 1000))
            interval = record.interval
            last_polled_time = record.last_polled_time
            task_status = record.task_status

            # check for the authenticity of id
            if (task_generated_time + expires_in > current_time):
                response = {"error_id": "access denied", "error_message": "'themobe_id' expired."}
                return jsonify(response), status.HTTP_400_BAD_REQUEST

            # Update interval when polling is heavy
            if (last_polled_time + interval * 1000 > current_time):
                record.interval = interval + 3
                db.session.commit()
                response = {"error_id": "slow down", "error_message": "polling is too heavy"}
                return jsonify(response), status.HTTP_400_BAD_REQUEST

            if (task_status != "ANNOTATED"):
                # update polling
                record.last_polled_time = current_time
                db.session.commit()
                response = {"error_id": "task not completed", "error_message": "annotation process is taking time."}
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

@app.route("/download")
def downloadFile():
    if 'themobe_id' in request.args:
        id = request.args.get('themobe_id')
        return manageDownload(id, APP_ROOT)


if __name__ == "__main__":
    app.run(debug=True)
