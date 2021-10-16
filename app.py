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


#TODO: Расставь коды

@app.route('/')
@app.route('/index')
def index():
    return jsonify({'msg': 'Gello'})


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



@app.route('/mypolls', methods=['GET', 'POST', 'OPTIONS'])
def mypolls():
    try:
        verify_jwt_in_request(locations=['headers', 'cookies'])
    except NoAuthorizationError:
        return jsonify({'msg': 'Login please!'}), 401

    if request.method == 'GET':
        raw_polls_list = get_polls_list(session['username'])
        # polls_list_in_json = json.dumps(raw_polls_list)

        return jsonify({'msg': raw_polls_list}), 200

    if request.method == 'POST':
        polls_name = request.json['Poll_name']

        polls_id = get_polls_id(polls_name)

        return jsonify({'polls_id': polls_id})

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allowed GET, POST methods'}), 200

    return jsonify({'msg': 'Method not allowed'}), 405


@app.route('/mypolls/newpoll', methods=['GET', 'POST', 'OPTIONS'])
def newpoll():
    try:
        verify_jwt_in_request(locations=['headers', 'cookies'])
    except NoAuthorizationError:
        return jsonify({'msg': 'Login please!'}), 401


    if request.method == 'POST':
        poll_name = request.json['Poll_name']
        question = request.json['Questions']
        question_in_json = json.dumps(question)
        access_level = request.json['Access_level']

        if access_level == 'Private':
            access_granted = request.json['Access_granted']

        else:
            access_granted = 'All users'

        if not is_polls_name_exists(poll_name):
            user_id = get_user_id(session['username'])

            counter_dict = json.loads(question_in_json)

            for q in counter_dict.values():
                for ans in q:
                    q[ans] = 0

            counter_in_json = json.dumps(counter_dict)

            poll = Poll(user_id, poll_name, question_in_json, counter_in_json, access_level, access_granted)
            db_session.add(poll)
            db_session.commit()

            return jsonify({'msg': 'The poll was successfully created'}), 200

        return jsonify({'msg': 'Such poll name has already existed'}), 201

    if request.method == 'GET':
        return jsonify({'msg': 'New Poll page'}), 200

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow GET, POST methods'}), 200

    else:
        return jsonify({"method not allowed"}), 405


@app.route('/mypolls/<polls_id>', methods=['GET', 'POST', 'OPTIONS'])
def get_poll(polls_id):
    try:
        verify_jwt_in_request(locations=['headers', 'cookies'])
    except NoAuthorizationError:
        return jsonify({'msg': 'Login please!'}), 401

    if request.method == 'GET':
        full_poll = get_poll_for_changing(polls_id)
        return jsonify({"Polls_name": full_poll[0], "Questions": full_poll[1], "Access_level": full_poll[2], "Access_granted": full_poll[3]})


    if request.method == 'POST':
        poll_name = request.json['Poll_name']
        question = request.json['Questions']
        question_in_json = json.dumps(question)
        access_level = request.json['Access_level']

        if access_level == 'Private':
            access_granted = request.json['Access_granted']

        else:
            access_granted = 'All users'

        #TODO: POST-method. To add access level to GET-method

@app.route('/polls/<polls_id>', methods=['GET', 'POST', 'OPTIONS'])
def answer_to_poll(polls_id):

    if request.method == 'GET':
        access = get_access_level_by_polls_id(polls_id)

        access_result = get_email_from_access_granted(session['username'], polls_id)

        if access == 'Private' and access_result == "Access granted":
            try:
                verify_jwt_in_request(locations=['headers', 'cookies'])
            except NoAuthorizationError:
                return jsonify({'msg': 'Login please!'}), 401

            return jsonify({'Questions': get_questions_by_poll_id(polls_id)})

        elif access == 'Private' and access_result != 'Access Granted':
            return jsonify({"msg": "You haven't access to this poll"})

        elif access == 'Public':
            return jsonify({'Questions': get_questions_by_poll_id(polls_id)})

    if request.method == 'POST':
        user_id = get_user_id(session['username'])
        
        if not is_answer_exists(user_id, polls_id):

            answers = request.json['Answers']
            answers_in_json = json.dumps(answers)

            answers_to_db = Users_answers(user_id, polls_id, answers_in_json)
            db_session.add(answers_to_db)

            counter = get_counter(polls_id)
            counter_in_dict = json.loads(counter)

            list_of_answers = json.loads(answers_in_json)

            for q in list_of_answers.keys():
                counter_in_dict[q][list_of_answers[q]] += 1

            counter_in_json = json.dumps(counter_in_dict)

            db_session.query(Poll).filter(Poll.id == polls_id).update({'counter': counter_in_json}, synchronize_session='fetch')
            db_session.commit()
            return jsonify({"msg": "Answer accepted"})

        return jsonify({"msg": "You've already answered on this poll"})
        


@app.route('/adminpage/<user_id>', methods=['GET', 'POST', 'OPTIONS'])
def adminpage():
    try:
        verify_jwt_in_request(locations=['headers', 'cookies'])
    except NoAuthorizationError:
        return jsonify({'msg': 'Login please!'}), 401

    if session['username'] != "admin@mail.ru":
        return jsonify({'msg': 'You have not access'})

    if request.method == 'GET':
        return jsonify({'msg': 'Welcome home, Admin'})

    if request.method == 'POST':
        username = request.json['Username']

        user_id = get_user_id(username)

        return jsonify({'User_name': username, 'User_id': user_id})

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow GET, POST methods'}), 200

    else:
        return jsonify({"method not allowed"}), 405


@app.route('/adminpage/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        verify_jwt_in_request(locations=['headers', 'cookies'])
    except NoAuthorizationError:
        return jsonify({'msg': 'Login please!'}), 401

    if session['username'] != "admin@mail.ru":
        return jsonify({'msg': 'You have not access'})

    if request.method == 'DELETE':
        db_session.query(User).filter(User.id == user_id).delete(synchronize_session='fetch')
        db_session.commit()
        return jsonify({'msg': 'The user was deleted'})

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow DELETE method'}), 200

    else:
        return jsonify({"method not allowed"}), 405



@app.route('/adminpage/delete_poll/<polls_id>', methods=['DELETE'])
def delete_poll(polls_id):
    try:
        verify_jwt_in_request(locations=['headers', 'cookies'])
    except NoAuthorizationError:
        return jsonify({'msg': 'Login please!'}), 401

    if session['username'] != "admin@mail.ru":
        return jsonify({'msg': 'You have not access'})

    if request.method == 'DELETE':
        db_session.query(Poll).filter(Poll.id == polls_id).delete(synchronize_session='fetch')
        db_session.commit()
        return jsonify({'msg': 'The poll was deleted'})

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow DELETE method'}), 200

    else:
        return jsonify({"method not allowed"}), 405


if __name__ == '__main__':
    app.run(debug=True)
