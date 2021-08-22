from enum import unique
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user1:123abc@localhost:5432/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True)
    name = db.Column(db.String(255))
    activation_link = db.Column(db.String(255), unique = True)
    is_activated = db.Column(db.Boolean)
    reset_password_link = db.Column(db.String(255), unique = True)
    send_reset_link_date = db.Column(db.TIMESTAMP)
    is_deleted = db.Column(db.Boolean)
    is_logined = db.Column(db.Boolean)

    def __repr__(self):
        return '<user:id %d, email %s, name %s>' % (self.id, self.email, self.name)

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(255))
    link = db.Column(db.String(255))
    send_date = db.Column(db.DateTime)
    comment_count = db.Column(db.Integer)
    origin_message_id = db.Column(db.Integer, db.ForeignKey('message.id'))

    def __repr__(self):
        return '<message:id %d, user_id %d, content %s>' % (self.id, self.user_id, self.content)

class Comment(db.Model):
    __tabelname__ = 'comment'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    content = db.Column(db.String(255))
    comment_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<comment:id %d, message_id %d, content %s>' % (self.id, self.message_id, self.content)

class Follow(db.Model):
    __tablename__ = 'follow'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    follow_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    follow_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<follow:id %d, user_id %d, follow_id %d>' % (self.id, self.user_id, self.follow_id)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        include_relationships = True
        load_instance = True

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        include_relationships = True
        load_instance = True

class FollowSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Follow
        include_relationships = True
        load_instance = True

db.create_all()