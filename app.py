import os, time
import uuid

from flask import Flask, render_template, request, send_file,request, jsonify
from flask_api import status

from AnnotationManager import annotateVideo

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/annotate",methods=["POST"])
def annotate():
    target = "/".join([APP_ROOT,"toAnnotate"])

    if not os.path.isdir(target):
        os.mkdir(target)

    # Obtain filename
    file = request.files['video']
    filename = file.filename

    # Check for video formats
    if not (".mp4" in file.filename):
        return render_template("file Error.html")

    id = uuid.uuid1()
    # Save file
    if file:
        # Adding to datastore/database
        video_file = target+'/'+str(id)+'.mp4'
        file.save(video_file)

        # Annotate video for emotions
        if 'emo' in request.args:
            emo_annotation = request.args['emo']

        else:
            response = {"error_id": "Bad Request", "error_message": "parameters missing : 'emo' "}
            return response, status.HTTP_400_BAD_REQUEST


        if 'behav' in request.args:
            behav_annotation = request.args['behav']

        else:
            response = {"error_id": "Bad Request", "error_message": "parameters missing : 'behav' "}
            return response, status.HTTP_400_BAD_REQUEST

        if 'threat' in request.args:
            threat_annotation = request.args['threat']

        else:
            response = {"error_id": "Bad Request", "error_message": "parameters missing : 'emo' "}
            return response, status.HTTP_400_BAD_REQUEST

    annotateVideo(id,emo_annotation,behav_annotation,threat_annotation)

    response = {"themobe_id":id,"video":filename,"video_status":"processing"}
    return jsonify(response)

@app.route("/poll")
def polling():
    if 'themobe_id' in request.args:
        id = request.args.get('themobe_id')





@app.route("/download")
def downloadFile():
    # For windows you need to use drive name [ex: F:/Example.pdf]
    if 'themobe_id' in request.args:
        id = request.args.get('themobe_id')
        path =  "/".join([APP_ROOT,"toAnnotate"])
        print(path)
        video = path+'/'+id+'.mp4'
    return send_file(video, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
    # qttest.main(app)
