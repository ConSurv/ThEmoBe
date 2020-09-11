from flask import send_file


def manageDownload(id,APP_ROOT):
    path =  "/".join([APP_ROOT,"output"])
    print(path)
    video = path+'/'+id+'.mp4'

    # Check for task_status,update status (and delete) and then prepare for download

    return send_file(video, as_attachment=True)