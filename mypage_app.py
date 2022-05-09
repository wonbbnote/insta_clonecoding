import express as express
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pymongo import MongoClient

import certifi

client = MongoClient('URL', tlsCAFile=certifi.where())
db = client.insta

app = Flask(__name__)


# 마이 페이지 링크
@app.route('/')
def mypage():
    return render_template('mypage.html')


# 마이 페이지 활동 GET
@app.route('/api/activity', methods=['GET'])
def activity_view():
    comments = list(db.comments.find({}, {'_id': False}))
    follower = list(db.follower.find({}, {'_id': False}))
    likes = list(db.likes.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'comments': comments, 'follower': follower, 'likes': likes})


# 마이 페이지 하단 피드img GET
@app.route('/api/feeds', methods=['GET'])
def feed_view():
    posts = list(db.posts.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'posts': posts})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
