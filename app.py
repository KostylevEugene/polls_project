from flask import Flask, jsonify, request
from forms import RegisterForm
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

@app.route('/registration', methods=['GET', 'POST'])
def registration():

    form = RegisterForm()

    if request.method == 'POST':

        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        valid_password = request.json['valid_password']
        role = 'signed-up'

        if form.name:
            new_user = User(name, email, password, role)

            db_session.add(new_user)
            db_session.commit()

            return user_schema.dump(new_user)

@app.route('/users/<id>', methods=['GET'])
def get_all_users(id):
    user = User.query.get(id)
    return user_schema.dump(user)



if __name__ == '__main__':
    app.run(debug=True)
