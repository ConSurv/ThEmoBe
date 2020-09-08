import os, time

from flask import Flask, render_template, request, send_file

# import blei_executable_and_tethne,FilterTweetDataByMonth,plotting,FilterTweetDataByDate,

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/annotate",methods=["GET"])
def annotate():
    print(APP_ROOT)
    target = os.path.join(APP_ROOT, "/annotate")

    if not os.path.isdir(target):
        os.mkdir(target)

    file = request.files['video']
    filename = file.filename

    # Check for video formats
    if not (".mp4" in file.filename):
        return render_template("file Error.html")

    if file:
        destination = "/".join([target, filename])
        file.save(destination)

    #     Annotate video for emotions

    return render_template("index1.html", fileExists=True)




@app.route("/viewResults")
def viewResults(filename):
    if os.path.isfile(APP_ROOT + filename):
        print(True)
        return render_template("index1.html", fileExists=True)
    else:
        return render_template("index1.html", fileExists=False)


@app.route("/download")
def downloadFile(filename):
    # For windows you need to use drive name [ex: F:/Example.pdf]
    path = "static/03.png"
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
    # qttest.main(app)
