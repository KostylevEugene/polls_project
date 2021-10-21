from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from webapp.queries import *

import json

blueprint = Blueprint('stat', __name__, url_prefix='/stats')


@blueprint.route('/', methods=['GET', 'OPTIONS'])
def get_stat():
    try:
        verify_jwt_in_request(locations=['headers', 'cookies'])
    except NoAuthorizationError:
        return jsonify({'msg': 'Login please!'}), 401

    if request.method == 'GET':
        polls = get_polls_list(session['username'])
        return jsonify({'Polls': polls})


@blueprint.route('/<polls_id>', methods=['GET', 'POST'])
def get_polls_stat(polls_id):
    try:
        verify_jwt_in_request(locations=['headers', 'cookies'])
    except NoAuthorizationError:
        return jsonify({'msg': 'Login please!'}), 401

    if request.method == 'GET':
        counter = get_counter(polls_id)
        users_amount = len(get_answered_users(polls_id))
        return jsonify({'Questions': json.loads(counter), 'Users_amount': users_amount})
