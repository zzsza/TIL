# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from app.database import Base
# 이 경우 경로를 위해 app.을 붙여줘야합니다

# users 테이블에 맵핑
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    password = Column(String(50), unique=False, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    image = Column(String(200), unique=False)
    company = Column(String(100), unique=False)
    gender = Column(String(50), unique=False)
    location = Column(String(100), unique=False)
    tel = Column(String(100), unique=False)
    description = Column(String(500), unique=False)

    posts = relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, name=None, password=None, email=None, image=None,
                 company=None, gender=None, location=None, tel=None, description=None):
        self.name = name
        self.password = password
        self.email = email
        self.image = image
        self.company = company
        self.gender = gender
        self.location = location
        self.tel = tel
        self.description = description

    # Representation
    def __repr__(self):
        return '<User %r>' % (self.name)


# posts 테이블에 맵핑
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    contents = Column(Text, unique=False)
    userid = Column(Integer, nullable=False)
    writer = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow, unique=False)  # 자동으로 들어간다.

    users = relationship('User', backref='post', lazy='joined')

    def __init__(self, contents=None, userid=None, writer=None):
        self.contents = contents
        self.userid = userid
        self.writer = writer

    def __repr__(self):
        return '<Contents %r %r>' % (self.contents, self.userid)