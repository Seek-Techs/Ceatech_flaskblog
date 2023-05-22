from datetime import datetime
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from itsdangerous.url_safe import URLSafeSerializer as Serializer
# from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import TimedSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app


# flaskblog package to import db or login_manager\n
# variable named define
from flaskblog import db, login_manager
from flask_login import UserMixin

# this define user id by getting each of the
# user id and also used as a decorator
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)
    

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # modified user_id = s.loads(token)['user_id']
            user_id = s.loads(token)['user_id']
            # if s.is_expired(user_id):
            #     return None
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"