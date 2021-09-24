import datetime
import json

from config import *
from db import db_session
from flask import Flask, jsonify, request, session
from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request, \
    set_access_cookies, get_jwt_identity, create_refresh_token
from flask_jwt_extended.exceptions import NoAuthorizationError
from forms import RegisterForm
from models import *
from queries import *
import hashlib
import bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

app.config['JWT_TOKEN_LOCATION'] = JWT_TOKEN_LOCATION
app.config["JWT_COOKIE_SECURE"] = JWT_COOKIE_SECURE
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_COOKIE_CSRF_PROTECT"] = JWT_COOKIE_CSRF_PROTECT
jwt = JWTManager(app)
salt = bcrypt.gensalt()
expiration_time = 20000


user_schema = UserSchema()
# question_schema = QuestionSchema()
# poll_schema = PollSchema()

@app.route('/')
@app.route('/index')
def index():
    return jsonify({'msg': 'Gello'})

@app.route('/new_poll')
def new_poll():
    pass

@app.route('/registration', methods=['GET', 'POST'])
def registration():

    if request.method == 'POST':

        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        valid_password = request.json['valid_password']
        role = 'signed-up'

        old_user = signed_in_user(email)

        if password != valid_password:
            return jsonify({'msg': "Password are incompatible"}), 404

        if old_user:
            return jsonify({'msg': "Such user has already exists"}), 404

        else:
            hash_pass = bcrypt.hashpw(password.encode("utf8"), salt).decode("utf8")

            new_user = User(name, email, hash_pass, role)

            db_session.add(new_user)
            db_session.commit()

            return user_schema.dump(new_user)

    if request.method == 'GET':
        return jsonify({'msg': 'Registration page'}), 201

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow GET, POST methods'}), 200

    else:
        return jsonify({"method not allowed"}), 405


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
@app.route('/log', methods=['GET', 'POST'])
def log():
    session['username'] = 'guest'

    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']

        old_user = signed_in_user(email)

        if old_user != email:
            return jsonify({'msg': 'There is no such email'}), 201

        else:
            existed_password = get_password_by_email(email)
            if bcrypt.checkpw(password.encode('utf8'), existed_password.encode('utf8')):
                session['username'] = email
                refresh_token = create_refresh_token(identity=email,
                                                     expires_delta=datetime.timedelta(seconds=expiration_time))
                access_token = create_access_token(identity=email,
                                                   expires_delta=datetime.timedelta(seconds=expiration_time))
                response = jsonify({'login': True, 'JWT': access_token, 'refresh_token': refresh_token})
                app.config['JWT_COOKIE_CSRF_PROTECT'] = False
                response.status_code = 200
                return response
            else:
                jsonify({'msg': 'Wrong password'}), 407

    if request.method == 'GET':
        return jsonify({'msg': 'Login page'}), 200

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow GET, POST methods'}), 200

    else:
        return jsonify({"method not allowed"}), 405

@app.route('/users/<id>', methods=['GET'])
def get_all_users(id):
    user = User.query.get(id)
    return user_schema.dump(user)


@app.route('/newpoll', methods=['GET', 'POST', 'OPTIONS'])
def newpoll():
    try:
        verify_jwt_in_request(locations=['headers', 'cookies'])
    except NoAuthorizationError:
        return jsonify({'msg': 'Login please!'}, 401)


    if request.method == 'POST':
        poll_name = request.json['Poll_name']
        question = request.json['Questions']
        question_in_json = json.dumps(question)

        if poll_name != get_poll_name(poll_name):
            user_id = get_user_id(session['username'])

            counter_dict = json.loads(question_in_json)

            for q in counter_dict.values():
                for ans in q:
                    q[ans] = "0"

            counter_in_json = json.dumps(counter_dict)

            poll = Poll(user_id, poll_name, question_in_json, counter_in_json)
            db_session.add(poll)
            db_session.commit()

            return jsonify({'msg': 'The poll was successfully created'}), 200

        else:
            return jsonify({'msg': 'Such poll name has already existed'}), 201

    if request.method == 'GET':
        return jsonify({'msg': 'New Poll page'}), 200

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow GET, POST methods'}), 200

    else:
        return jsonify({"method not allowed"}), 405


if __name__ == '__main__':
    app.run(debug=True)
