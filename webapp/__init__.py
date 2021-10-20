from flask import Flask, jsonify, request, session
from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request, \
    set_access_cookies, get_jwt_identity, create_refresh_token
from flask_jwt_extended.exceptions import NoAuthorizationError
from webapp.config import *
from webapp.db import db_session
from webapp.forms import RegisterForm
from webapp.models import *
from webapp.queries import *
from webapp.user.views import blueprint as user_blueprint
from webapp.poll.views import blueprint as poll_blueprint
from webapp.admin.views import blueprint as admin_blueprint
import hashlib
import json
import bcrypt


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY

    app.config['JWT_TOKEN_LOCATION'] = JWT_TOKEN_LOCATION
    app.config["JWT_COOKIE_SECURE"] = JWT_COOKIE_SECURE
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["JWT_COOKIE_CSRF_PROTECT"] = JWT_COOKIE_CSRF_PROTECT

    app.register_blueprint(user_blueprint)
    app.register_blueprint(poll_blueprint)
    app.register_blueprint(admin_blueprint)
    jwt = JWTManager(app)


    user_schema = UserSchema()


    #TODO: Расставь коды

    @app.route('/')
    @app.route('/index')
    def index():
        return jsonify({'msg': 'Gello'})



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


    @app.route('/adminpage/users/<user_id>', methods=['DELETE'])
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


    @app.route('/adminpage/polls/<polls_id>', methods=['DELETE'])
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


    @app.route('/stat', methods=['GET', 'OPTIONS'])
    def get_stat():
        try:
            verify_jwt_in_request(locations=['headers', 'cookies'])
        except NoAuthorizationError:
            return jsonify({'msg': 'Login please!'}), 401

        if request.method == 'GET':
            polls = get_polls_list(session['username'])
            return jsonify({'Polls': polls})


    @app.route('/stat/<polls_id>', methods=['GET', 'POST'])
    def get_polls_stat(polls_id):
        try:
            verify_jwt_in_request(locations=['headers', 'cookies'])
        except NoAuthorizationError:
            return jsonify({'msg': 'Login please!'}), 401

        if request.method == 'GET':
            counter = get_counter(polls_id)
            users_amount = len(get_answered_users(polls_id))
            return jsonify({'Questions': json.loads(counter), 'Users_amount': users_amount})


    return app
