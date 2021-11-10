from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import create_access_token, verify_jwt_in_request, \
    set_access_cookies, get_jwt_identity, create_refresh_token
from webapp.models import *
from webapp.queries import *
import bcrypt
import datetime

blueprint = Blueprint('user', __name__, url_prefix='/users')

salt = bcrypt.gensalt()
expiration_time = 20000

user_schema = UserSchema()


@blueprint.route('/registration', methods=['GET', 'POST'])
def to_sign_up():

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

            return jsonify({'msg': 'Registration success'})

    if request.method == 'GET':
        return jsonify({'msg': 'Registration page'}), 201

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow GET, POST methods'}), 200

    else:
        return jsonify({'msg':"method not allowed"}), 405


@blueprint.route('/log', methods=['GET', 'POST'])
def to_sign_in():
    session['username'] = 'guest'       # the email will be the username

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
                response = jsonify({"login": True, "JWT": access_token, "refresh_token": refresh_token})
                # app.config['JWT_COOKIE_CSRF_PROTECT'] = False
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