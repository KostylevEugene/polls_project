from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import create_access_token, verify_jwt_in_request, \
    set_access_cookies, get_jwt_identity, create_refresh_token
from flask_jwt_extended.exceptions import NoAuthorizationError
from webapp.queries import *

blueprint = Blueprint('admin', __name__, url_prefix='/adminpage')


@blueprint.route('/', methods=['GET'])
def get_adminpage():
    try:
        verify_jwt_in_request(locations=['headers', 'cookies'])
    except NoAuthorizationError:
        return jsonify({'msg': 'Login please!'}), 401

    if session['username'] != "admin@mail.ru":
        return jsonify({'msg': 'You have not access'})

    if request.method == 'GET':
        return jsonify({'msg': 'This is AdminPage. Choose what you want to edit/delete - users or polls' })



@blueprint.route('/users/<user_id>', methods=['GET', 'POST', 'OPTIONS'])
def manage_users(user_id):
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

    if request.method == 'DELETE':
        db_session.query(User).filter(User.id == user_id).delete(synchronize_session='fetch')
        db_session.commit()
        return jsonify({'msg': 'The user was deleted'})

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow GET, POST, DELETE methods'}), 200

    else:
        return jsonify({"method not allowed"}), 405


@blueprint.route('/polls/<polls_id>', methods=['DELETE'])
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
