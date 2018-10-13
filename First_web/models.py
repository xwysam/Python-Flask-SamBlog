#encoding: utf-8

from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),nullable=False )


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.TEXT,nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    time = db.Column(db.DateTime,default=datetime.now)

    author = db.relationship('User',backref = db.backref('articles'))

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.TEXT, nullable=False)
    comment_id = db.Column(db.Integer,db.ForeignKey('article.id'))
    time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    article = db.relationship('Article', backref=db.backref('comments', order_by= time.desc()))
    author = db.relationship('User', backref=db.backref('comments'))






