from flask import Flask, jsonify, request
import models

app = Flask(__name__)



@app.route('/')
@app.route('/index')
def index():
    return jsonify({'msg': 'Gello'})

@app.route('/new_poll')
def new_poll():
    pass

@app.route('/registration')
def registration():
    pass

if __name__ == '__main__':
    app.run(debug=True)
