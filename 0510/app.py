from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from pymongo import MongoClient
import certifi
import gridfs
import codecs
from bson.objectid import ObjectId
import jwt
import datetime
import hashlib

client = MongoClient('mongodb+srv://kimjuhoon:base5781@cluster0.4l2nw.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.prac
app = Flask(__name__)
SECRET_KEY = '3iI3j63EmUww246bXHUVghUnYkTwQ6lm'
fs = gridfs.GridFS(db)

##으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으##

##      토큰 확인 함수 및 mainpage 경로 설정      ##

##으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으##

def check_token():
    # 현재 이용자의 컴퓨터에 저장된 cookie 에서 mytoken 을 가져옵니다.
    token_receive = request.cookies.get('token')
    # token을 decode하여 payload를 가져오고, payload 안에 담긴 유저 id를 통해 DB에서 유저의 정보를 가져옵니다.
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    return db.users.find_one({'id': payload['id']}, {"_id": False})

@app.route('/')
def home():
    try:
        user_info = check_token()
        # posts = reversed(list(db.posts.find({}))) # 최신순으로 나오게 정렬을 뒤집음.

        return render_template('mainpage.html', user=user_info)
        # return render_template('index.html', user=user_info)
        # # 만약 해당 token의 로그인 시간이 만료되었다면, 아래와 같은 코드를 실행합니다.
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        # 만약 해당 token이 올바르게 디코딩되지 않는다면, 아래와 같은 코드를 실행합니다.
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def mainpage():
    return render_template('login.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

##으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으##

##      회원가입 및 로그인 설정        ##

##으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으##

# [회원가입 API]
# id, pw을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        id = request.form['id']
        pw = request.form['pw']
        pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
        profile_img = request.files['profile_img']
        extension = profile_img.filename.split('.')[-1]
        create_date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        pfilename = f'{id}-{create_date}'  # 파일이름
        save_to = f'static/profile/{pfilename}.{extension}'  # 파일 경로
        profile_img.save(save_to)  # 파일 저장

        doc = {
            "id": id,
            "pw": pw_hash,
            "description": "",
            'profile_img': f'/post/{pfilename}.{extension}',
        }
        db.users.insert_one(doc)
        return jsonify({"result": "회원 가입 성공"})
    else:
        return render_template('regist.html')


# [아이디 중복확인 API]
# 유저 인풋으로 받은 계정을 DB에서 조회하고, 이미 존재하면 True 반환합니다.
@app.route("/register/check_id", methods=["POST"])
def check_id():
    id = request.form['id']
    duplicated_id = db.users.find_one({'id': id})

    return jsonify({"duplicated": bool(duplicated_id)})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        data = request.json  ## id는 json으로 요청하기위해서
        pw_hash = hashlib.sha256(data["pw"].encode("utf-8")).hexdigest() # PW hash: DB에 hash값으로 저장했기 때문에 다시 hash값으로 전환해 조회합니다.
        result = db.users.find_one({'id': data["id"], 'pw':pw_hash})

        # token issue: 토큰을 발행하고, ajax response에서 사용자 쿠키에 토큰을 저장합니다.
        if result is not None:
            payload = {
                "id": data["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')  ###.decode('utf-8')###

            return jsonify({"result": "success", "token": token})
        else:
            return jsonify({"msg": "회원 정보가 없습니다."})
    else:
        token = request.cookies.get('token')
        if token != None:
            return redirect(url_for('home'))
        else:
            msg = request.args.get("msg")
            return render_template('login.html', msg=msg)


##으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으##
##      포스트 GET(조회) & POST(작성)       ##
##으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으##

## 포스트 작성
@app.route('/post/create', methods=['GET', 'POST'])
def post_create():
    user_info = check_token()

    if request.method == 'POST':

        content = request.form['content']
        file = request.files['file']
        extension = file.filename.split('.')[-1]
        # create_date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        create_date = datetime.datetime.now().strftime('%Y.%m.%d.%H.%M')
        filename = f'{user_info["id"]}-{create_date}'  # 파일이름
        save_to = f'static/post/{filename}.{extension}'  # 파일 경로
        file.save(save_to)  # 파일 저장
        post_list = list(db.posts.find({}))
        count = len(post_list) + 1
        pfilename = f'{user_info["id"]}-{create_date}'  # 파일이름
        # save_to = f'static/profile/{pfilename}.{extension}'  # 파일 경로
        # profile_img.save(save_to)  # 파일 저장

        doc = {
            'num' : count,
            'content': content,
            'user': user_info['id'], #_id
            'create_time': create_date,
            'file': f'/post/{filename}.{extension}',
            'profile_img': f'/post/{pfilename}.{extension}'
        }
        db.posts.insert_one(doc)

        return jsonify({'msg': "저장 완료"})
    else:
        return render_template('create_post.html')

# 포스트 읽어오기
@app.route("/post/get", methods=["GET"])
def post_get():
    post_list = list(db.posts.find({}, {'_id':False}))
    # img_list = list(db.fs.chunk.find(),{'_id':False})
    return jsonify({'posts': post_list})


##으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으##
##      아직 못함        ##
##으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으으흐루꾸꾸루흐으##


# # # 댓글 작성
# # @app.route('/comment/create', methods=['POST'])
# # def comment_create():
# #     comment_receive = request.form['comment_give']
# #     doc = {
# #         'comment': comment_receive
# #     }
# #     db.comments.insert_one(doc)
# #     return jsonify({'msg':'댓글 등록'})
#
#
# # 댓글 작성
# @app.route('/comment/create', methods=['GET', 'POST'])
# def comment_create():
#     # 코멘트를 작성하는 유저 정보를 받습니다.
#     user = check_token()
#
#     if request.method == 'POST':
#         # post_id = request.form['post_id']
#         user_id = user['id']
#         content = request.form['content']
#         # '_id'로 받은 id값을 데이터 객체의 OjbectId(_id) 형태로 만들기 위해 ObjectId 객체로 전환합니다.
#         # object_post_id = ObjectId(post_id)
#         # print(object_post_id)
#
#         doc = {
#             'user': user_id,
#             'content': content,
#             'create_time': datetime.datetime.now(),
#         }
#         db.comments.insert_one(doc)
#         # doc 는 Comments db 에 저장
#
#         # doc_for_comment = {
#         #     'comment_id': comment_id,
#         #     'user': user_id,
#         #     'content': content,
#         #     'create_time': datetime.datetime.now(),
#         # }
#         #
#         # db.posts.update_one({'_id': object_post_id}, {'$addToSet': {'comments': doc_for_comment}})
#         # doc_for_comment 는 posts 디비에 추가 업데이트를 해준다. 어떤 포스트 디비에 해주는 조건은 post_id 값을 받아와 해당하는 포스트에 저장
#
#         return redirect(url_for('home'))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True, use_reloader=True)
