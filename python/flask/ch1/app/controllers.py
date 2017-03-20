# -*- coding: utf-8 -*-
from app.database import init_db, db_session
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from app.models import User, Post
# 이 경우 app.을 붙여줘야 경로를 인식함
from app import app


# 메인페이지
@app.route('/')
@app.route('/index')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


# 프로필
@app.route('/profile/<int:userId>')
def profile(userId):
    # 사용자 정보
    user = User.query.filter_by(id=userId).first()
    # app.logger.debug(user.image)

    # 컨텐츠 리스트
    posts = Post.query.filter(Post.userid == User.id).order_by(Post.id.desc()).all();
    # app.logger.debug(len(posts))

    return render_template('profile.html', user=user, posts=posts, userId=userId)


# 로그인 화면
@app.route('/login-form')
def loginForm():
    return render_template('login.html')


# 로그인
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).filter_by(password=password).first()
        # app.logger.debug(request.form['email'])
        # app.logger.debug(user.name)
        if (user):
            session['logged_in'] = True
            session['id'] = user.id
            session['email'] = user.email
            session['name'] = user.name
            session['image'] = user.image
            return redirect("/profile/" + str(user.id))
        else:
            return '로그인 정보가 맞지 않습니다.'

    else:
        return '잘못된 접근'


# 로그아웃
@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('index'))


# 컨텐츠 등록
@app.route('/add/<int:userId>', methods=['POST'])
def add(userId):
    if request.method == 'POST':
        if (session['logged_in']):
            # app.logger.debug(request.form['contents'])
            # app.logger.debug(request.form['userId'])
            post = Post(request.form['contents'], userId, session['id'])
            db_session.add(post)
            db_session.commit()
            return redirect("/profile/" + str(userId))
        else:
            return '로그인해주세요'
    else:
        return '잘못된 접근'


# 컨텐츠 삭제
@app.route('/delete/<int:userId>/<int:postId>')
def delete(userId, postId):
    if (session['logged_in']):
        Post.query.filter_by(id=postId).delete()
        return redirect("/profile/" + str(userId))
    else:
        return '잘못된 접근'