from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import verify_jwt_in_request, \
    set_access_cookies, get_jwt_identity, create_refresh_token
from flask_jwt_extended.exceptions import NoAuthorizationError
from webapp.queries import *
import json

blueprint = Blueprint('poll', __name__, url_prefix='/polls')


@blueprint.route('/mypolls', methods=['GET', 'POST', 'OPTIONS'])
def mypolls():
    try:
        verify_jwt_in_request(locations=['headers', 'cookies'])
    except NoAuthorizationError:
        return jsonify({'msg': 'Login please!'}), 401

    if request.method == 'GET':
        polls_list = get_polls_list(session['username'])
        return jsonify({'msg': polls_list}), 200

    if request.method == 'POST':
        polls_name = request.json['Poll_name']

        polls_id = get_polls_id(polls_name)

        return jsonify({'polls_id': polls_id})

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allowed GET, POST methods'}), 200

    return jsonify({'msg': 'Method not allowed'}), 405


@blueprint.route('/mypolls/newpoll', methods=['GET', 'POST', 'OPTIONS'])
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


@blueprint.route('/mypolls/<polls_id>', methods=['GET', 'POST', 'DELETE', 'OPTIONS'])
def get_poll(polls_id):
    try:
        verify_jwt_in_request(locations=['headers', 'cookies'])
    except NoAuthorizationError:
        return jsonify({'msg': 'Login please!'}), 401

    if request.method == 'GET':
        full_poll = get_poll_for_changing(polls_id)
        return jsonify({"Polls_name": full_poll[0],
                        "Questions": full_poll[1],
                        "Access_level": full_poll[2],
                        "Access_granted": full_poll[3]
                        })

    if request.method == 'POST':
        polls_name = request.json['Polls_name']
        question = request.json['Questions']
        question_in_json = json.dumps(question)
        access_level = request.json['Access_level']

        if access_level == 'Private':
            access_granted = request.json['Access_granted']

        else:
            access_granted = 'All users'

        db_session.query(Poll).filter(Poll.id == polls_id).update({'polls_name': polls_name,
                                                                   'question': question_in_json,
                                                                   'access_level': access_level,
                                                                   'access_granted': access_granted},
                                                                  synchronize_session='fetch')

        db_session.commit()
        return jsonify({'msg': 'The Polls successfully was updated'}), 200

    if request.method == 'DELETE':
        db_session.query(Poll).filter(Poll.id == polls_id).delete(synchronize_session='fetch')
        db_session.commit()
        return jsonify({'msg': 'The Poll was successfully deleted'}), 200

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow GET, POST, DELETE methods'}), 200

    else:
        return jsonify({"method not allowed"}), 405


@blueprint.route('/<polls_id>', methods=['GET', 'POST', 'OPTIONS'])
def answer_to_poll(polls_id):

    if request.method == 'GET':
        access = get_access_level_by_polls_id(polls_id)

        access_result = get_email_from_access_granted(session['username'], polls_id)

        if access == 'Private' and access_result == "Access granted":
            try:
                verify_jwt_in_request(locations=['headers', 'cookies'])
            except NoAuthorizationError:
                return jsonify({'msg': 'Login please!'}), 401

            return jsonify({'Questions': json.loads(get_questions_by_poll_id(polls_id))})

        elif access == 'Private' and access_result != 'Access Granted':
            return jsonify({"msg": "You haven't access to this poll"})

        elif access == 'Public':
            return jsonify({'Questions': json.loads(get_questions_by_poll_id(polls_id))})

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

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow GET, POST, methods'}), 200

    else:
        return jsonify({"method not allowed"}), 405