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
from webapp.stat.views import blueprint as stat_blueprint
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
    app.register_blueprint(stat_blueprint)
    jwt = JWTManager(app)

    user_schema = UserSchema()

    #TODO: Расставь коды

    @app.route('/')
    @app.route('/index')
    def index():
        return jsonify({'msg': 'Gello'})

    return app
