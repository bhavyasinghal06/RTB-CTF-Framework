''' Models '''

from flask import current_app
from FlaskRTBCTF.config import LOGGING
from FlaskRTBCTF import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

''' User Table '''

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    score = db.relationship('Score', backref='user', lazy=True, uselist=False)
    if LOGGING:
        logs = db.relationship('Logs', backref='user', lazy=True, uselist=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}'))"


''' Score Table '''

class Score(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False, primary_key=True)
    userHash = db.Column(db.Boolean, default=False)
    rootHash = db.Column(db.Boolean, default=False)
    points = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"Score('{self.user_id}', '{self.points}')"


''' Notifications Table '''

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    body = db.Column(db.String(250), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Notif('{self.title}', '{self.body}')"


''' Logging Table '''

if LOGGING:
    class Logs(db.Model):
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
        accountCreationTime = db.Column(db.DateTime, nullable=False)
        visitedMachine = db.Column(db.Boolean, default=False)
        machineVisitTime = db.Column(db.DateTime, nullable=True)
        userSubmissionTime = db.Column(db.DateTime, nullable=True)
        rootSubmissionTime = db.Column(db.DateTime, nullable=True)
        userOwnTime = db.Column(db.String, nullable=True)
        rootOwnTime = db.Column(db.String, nullable=True)
        userSubmissionIP = db.Column(db.String, nullable=True)
        rootSubmissionIP = db.Column(db.String, nullable=True)

        def __repr__(self):
            return f"Logs('{self.user_id}','{self.machineVisitTime}','{self.userSubmissionTime}'," \
                f"'{self.rootSubmissionTime}','{self.userOwnTime}','{self.rootOwnTime}','{self.userSubmissionIP}," \
                f" '{self.rootSubmissionIP}'"
