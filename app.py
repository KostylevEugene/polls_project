from db import db_session
from flask import Flask, jsonify, request
from forms import RegisterForm
from models import *
from queries import signed_in_user

app = Flask(__name__)

user_schema = UserSchema()


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
            new_user = User(name, email, password, role)

            db_session.add(new_user)
            db_session.commit()

            return user_schema.dump(new_user)

    if request.method == 'GET':
        return jsonify({'msg': 'Registration page'}), 201

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow GET, POST methods'}), 200

    else:
        jsonify({"method not allowed"}), 405

@app.route('/users/<id>', methods=['GET'])
def get_all_users(id):
    user = User.query.get(id)
    return user_schema.dump(user)



if __name__ == '__main__':
    app.run(debug=True)
