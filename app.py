from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return jsonify({'msg': 'Gello'})

if __name__ == '__main__':
    app.run(debug=True)