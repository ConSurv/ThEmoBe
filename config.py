import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    # # For Sqlite-database
    # target= os.path.join(basedir,"annotation.db")
    # target = "/".join([basedir, "annotation.db"])
    # print("db:"+target)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + target

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_TASK_SERIALIZER = 'pickle'
    # # MySQL Database
    SQLALCHEMY_DATABASE_URI = "mysql://root@localhost/annotate"

    SQLALCHEMY_TRACK_MODIFICATIONS = False