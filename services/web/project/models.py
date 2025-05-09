from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.Text,    nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tweets = db.relationship('Tweet', backref='user', lazy=True)

class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Url(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'), nullable=False)
    url = db.Column(db.Text, nullable=False)
    expanded_url = db.Column(db.Text, nullable=False)
