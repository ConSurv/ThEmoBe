from app import db

class Tasks(db.Model):
    __tablename__ = 'tasks_table'
    id = db.Column(db.String(128), primary_key=True)
    themobe_id = db.Column(db.String(128),index=True, unique=True)
    expires_in = db.Column(db.BigInteger)
    interval= db.Column(db.BigInteger)
    last_polled_time = db.Column(db.BigInteger)
    download_allocation_time = db.Column(db.BigInteger)
    download_req_id = db.Column(db.String(128),index=True, unique=True)
    task_status = db.Column(db.String(100))
    download_count = db.Column(db.Integer)
    persistent_status = db.Column(db.Boolean)

    def __repr__(self):
        # return '<Tasks {}>'.format(self.themobe_id)
        return "<Tasks(theombe_id='%s', interval='%s', task_status='%s')>" % (self.themobe_id, self.interval, self.task_status)
        # return '<Tasks %r>' % self.themobe_id'

    def getExpiresin(self):
        return self.expires_in

db.create_all()




