from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from WebApp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

access = db.Table('access',
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                  db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                  )

#class User(db.Model):
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    rights = db.relationship('Role', secondary=access, backref=db.backref('members', lazy='dynamic'))
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


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


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Role('{self.group}')"
    
class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    linkname = db.Column(db.String(100), unique=True, nullable=False)
    url = db.Column(db.String(255), unique=True, nullable=False)
    group = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Link('{self.linkname}', '{self.group}')"



