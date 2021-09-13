from flask import Flask, jsonify, request
from models import *
from db import db_session

app = Flask(__name__)

user_schema = UserSchema()
@app.route('/')
@app.route('/index')
def index():
    return jsonify({'msg': 'Gello'})

@app.route('/new_poll')
def new_poll():
    pass

@app.route('/registration', methods=['POST'])
def registration():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    role = request.json['role']

    new_user = User(name, email, password, role)

    db_session.add(new_user)
    db_session.commit()

    return user_schema.dump(new_user)

@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    result = user_schema.dump(all_users)
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)
