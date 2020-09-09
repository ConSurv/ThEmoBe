from app import db

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    themobe_id = db.Column(db.String(128),index=True, unique=True)
    expires_in = db.Column(db.Float)
    last_polled_time = db.Column(db.Float)
    task_status = db.Column(db.String(100))

    def __repr__(self):
        return '<Tasks {}>'.format(self.id)


class Agents(db.Model):
    agent_id = db.Column(db.Integer, primary_key=True)
    username = db.Col(db.String(120),unique=True)
    password = db.Col(db.String(120))
    callback_endpoint = db.Col(db.String(120),unique=True)
    persistence_preference = db.Col(db.Boolean)


    def __repr__(self):
        return '<Tasks {}>'.format(self.id)