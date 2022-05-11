
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename
# from datetime import datetime, timedelta
import certifi
import gridfs
import codecs
from bson.objectid import ObjectId

app = Flask(__name__)
# app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb+srv://kimjuhoon:base5781@cluster0.4l2nw.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.dbsparta_insta


#########################################################################################
# 로그인 상태 페이지
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})

        return render_template('login.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# 로그인/회원가입 페이지
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


# 메인 페이지
@app.route('/mainpage')
def mainpage():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        users = list(db.users.find({}, {'_id': False}))
        id = []
        for user in users:
            if user['username'] != user_info['username']:
                id.append(user['username'])
        return render_template('mainpage.html', ids=id, user_info=user_info)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# 마이 페이지
@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


# myownpage
@app.route('/myownpage')
def myownpage():
    return render_template('myownpage.html')


#######################################################################################
#### API 역할을 하는 부분 ####

# 김성호
# 로그인 API
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 회원가입
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,
        "password": password_hash,
        "profile_name": username_receive,
        "profile_pic": "static/image/profile.png",
        "profile_pic_real": "static/인스타로고.png",
        "profile_info": ""
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# 회원가입시 중복체크
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    # print(value_receive, type_receive, exists)
    return jsonify({'result': 'success', 'exists': exists})


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route('/api/nick', methods=['GET'])
def api_valid():
    user_info = check_token()
    token_receive = request.cookies.get('mytoken')
    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.users.find_one({'username': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'user_id': userinfo['username']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


def check_token():
    # 현재 이용자의 컴퓨터에 저장된 cookie 에서 mytoken 을 가져옵니다.
    token_receive = request.cookies.get('mytoken')
    # token을 decode하여 payload를 가져오고, payload 안에 담긴 유저 id를 통해 DB에서 유저의 정보를 가져옵니다.
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    return db.users.find_one({'username': payload['id']}, {"_id": False})


#################################################################################
# 김주훈
# 포스트 작성
@app.route('/post/create', methods=['GET', 'POST'])
def post_create():
    user_info3 = check_token()

    if request.method == 'POST':

        content = request.form['content']
        file = request.files['file']
        extension = file.filename.split('.')[-1]
        create_date = datetime.datetime.now().strftime('%Y.%m.%d.%H:%M')
        filename = f'{user_info3["username"]}-{create_date}'  # 파일이름
        save_to = f'static/post/{filename}.{extension}'  # 파일 경로
        file.save(save_to)  # 파일 저장
        post_list = list(db.posts.find({}))
        count = len(post_list) + 1

        doc = {
            'num' : count,
            'content': content,
            'user': user_info3['username'],
            'create_time': create_date,
            'file': f'/post/{filename}.{extension}',
            # 'profile_img': f'/post/{pfilename}.{extension}'
        }
        db.posts.insert_one(doc)

        return jsonify({'msg': "저장 완료"})
    else:
        return render_template('create_post.html')


# 포스트 읽어오기
@app.route("/post/get", methods=["GET"])
def post_get():
    post_list = list(db.posts.find({}, {'_id': False}))
    return jsonify({'posts': post_list})

# 댓글 작성
@app.route('/comment/create', methods=['GET', 'POST'])
def comment_create():
    user_info3 = check_token()

    if request.method == 'POST':
        comment = request.form['comment']
        create_date = datetime.datetime.now().strftime('%Y.%m.%d.%H:%M')
        comment_list = list(db.comments.find({}))
        count = len(comment_list) + 1

        doc = {
            'num' : count,
            'comment': comment,
            'user': user_info3['username'],
            'create_time': create_date,
        }
        db.comments.insert_one(doc)

        return jsonify({'msg': "저장 완료"})
    else:
        return render_template('/')

# 댓글 읽어오기
@app.route("/comment/get", methods=["GET"])
def comment_get():
    comment_list = list(db.comments.find({}, {'_id': False}))
    return jsonify({'posts': comment_list})


###########################################################################################
# 박진우
# 마이 페이지 활동 GET
@app.route('/api/activity', methods=['GET'])
def activity_view():
    user_info = check_token()
    comments = list(db.comments.find({}, {'_id': False}))
    follower = list(db.follower.find({}, {'_id': False}))
    likes = list(db.likes.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'comments': comments,
                    'follower': follower, 'likes': likes,
                    'username': user_info})


# 마이 페이지 하단 피드img GET
@app.route('/api/feeds', methods=['GET'])
def feed_view():
    user_info = check_token()
    posts = list(db.posts.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'posts': posts, 'username': user_info})


# 소개글 등록 POST
@app.route('/api/introduce', methods=['POST'])
def introduce_save():
    user_id_receive = check_token()
    introduce_receive = request.form['introduce_give']

    doc = {
        'user_id': user_id_receive['username'],
        'introduce': introduce_receive
    }
    db.introduce.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '소개 등록 완료'})


# 등록된 소개글 보여주기 GET
@app.route('/api/introduce', methods=['GET'])
def introduce_view():
    user_info = check_token()
    introduce = list(db.introduce.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'introduce': introduce, 'username': user_info})

###########################################################################################
# 최희원

# 팔로우 => POST
@app.route('/api/follow', methods=['POST'])
def test_post():
    userid_receive = request.form['userid_give']
    followid_receive = request.form['followid_give']
    # 만약 user_id와 follow_id가 같다면 안된다고 alert
    # userid의 팔로우 DB 안 follow키 리스트에 팔로우 id 추가
    doc = {
        'user_id': userid_receive,
        'follow_id': followid_receive
    }
    user = list(db.follower.find({'user_id': userid_receive, 'follow_id': followid_receive}))
    status = (userid_receive != followid_receive)
    if len(user) == 0 & status:
        db.follower.insert_one(doc)
        return jsonify({'result': 'success', 'msg': '팔로우했다'})
    elif len(user) != 0:
        return jsonify({'result': 'dup', 'msg': '이미 팔로우 했습니다'})
    elif not status:
        return jsonify({'result': 'myself', 'msg': '자신에게 팔로우 할 수 없습니다.'})
    # 팔로우한 id 팔로우DB에 팔로잉 id 추가


# 팔로우 취소 => POST
@app.route('/api/unfollow', methods=['POST'])
def test_cancel():
    userid_receive = request.form['userid_give']
    unfollowid_receive = request.form['unfollowid_give']
    db.follower.delete_one({'user_id': userid_receive, 'follow_id': unfollowid_receive})
    return jsonify({'result': 'success', 'msg': '언팔로우 했따'})


# 팔로워 수 조회 => GET
@app.route('/api/following', methods=['GET'])
def test_get():
    nickname_receive = request.args.get('nickname_give')
    follower = list(db.follower.find({'follow_id': nickname_receive}, {'_id': False}))
    print('follower : ', follower)
    return jsonify({'follower': len(follower)})


# 팔로잉 수 조회 => GET
@app.route('/api/following2', methods=['GET'])
def test_get2():
    nickname_receive = request.args.get('nickname_give')
    follower = list(db.follower.find({'user_id': nickname_receive}, {'_id': False}))
    print(follower)
    return jsonify({'follower': len(follower)})


# 유저페이지 만들기
@app.route('/user')
def user_test():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_id = request.args.get('user_id')
    status = (user_id == payload["id"])
    print(status)
    # url_for 하고 user_id='test' 라고 했던 부분의 그 user_id 를 통해서 test 라는 값을 가져오는 겁니다! 즉, test 라는 값이 할당되겠죠?
    user_info = db.users.find_one({"username": user_id})
    # test 라는 id 를 가진 유저를 찾고, 그 유저의 정보를 user_info 에 저장합니다.
    return render_template("mypage.html", user_info=user_info, status=status)
    # 뒤쪽으로 왼쪽이 html 에서 쓸 변수명, 오른쪽이 현재 app.py 에서 넘겨주고자 하는 변수명입니다!


@app.route('/me')
def user_own():
    # user_info = check_token()
    user_id = request.args.get('user_id')
    # url_for 하고 user_id='test' 라고 했던 부분의 그 user_id 를 통해서 test 라는 값을 가져오는 겁니다! 즉, test 라는 값이 할당되겠죠?
    user_info2 = db.users.find_one({"username": user_id})
    # test 라는 id 를 가진 유저를 찾고, 그 유저의 정보를 user_info 에 저장합니다.
    return render_template("myownpage.html", user_info=user_info2)
    # 뒤쪽으로 왼쪽이 html 에서 쓸 변수명, 오른쪽이 현재 app.py 에서 넘겨주고자 하는 변수명입니다!


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
