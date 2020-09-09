import os, time
import uuid

from flask import Flask, render_template, request, send_file,request, jsonify

app = Flask(__name__)
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
        # if 'emo' in request.args:
            # annotate_emo(id)
        # if 'emo' in request.args:
            # annotate_behav(id)
        # if 'emo' in request.args:
            # annotate_threat(id)


    response = {"themobe_id":id,"video":filename,"video_status":"processing"}
    return jsonify(response)

@app.route("/viewResults")
def viewResults(filename):
    if os.path.isfile(APP_ROOT + filename):
        print(True)
        return render_template("index1.html", fileExists=True)
    else:
        return render_template("index1.html", fileExists=False)


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
