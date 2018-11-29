#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import sys
from flask import Flask
from flask import jsonify
from flask_swagger import swagger
from api.utils.responses import response_with
import api.utils.responses as resp
from api.routes.routes_employee import route_employee
import os
from api.utils.database import db

from functools import wraps
import json
from os import environ as env

from dotenv import load_dotenv, find_dotenv
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode

import constants

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)
if AUTH0_AUDIENCE is '':
    AUTH0_AUDIENCE = AUTH0_BASE_URL + '/userinfo'

def create_app(config):
    app = Flask(__name__,static_url_path='/public', static_folder='./public')
    app.secret_key = constants.SECRET_KEY
    app.config.from_object(config)
    app.register_blueprint(route_employee, url_prefix="")

    # START GLOBAL HTTP CONFIGURATIONS
    @app.after_request
    def add_header(response):
        return response

    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(resp.BAD_REQUEST_400)

    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp.NOT_FOUND_HANDLER_404)

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=AUTH0_BASE_URL,
        access_token_url=AUTH0_BASE_URL + '/oauth/token',
        authorize_url=AUTH0_BASE_URL + '/authorize',
        client_kwargs={
            'scope': 'openid profile',
        },
    )

    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if constants.PROFILE_KEY not in session:
                return redirect('/login')
            return f(*args, **kwargs)

        return decorated

    # Controllers API
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/callback')
    def callback_handling():
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()

        session[constants.JWT_PAYLOAD] = userinfo
        session[constants.PROFILE_KEY] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        return redirect('/dashboard')

    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)

    @app.route('/logout')
    def logout():
        session.clear()
        params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

    @app.route('/dashboard')
    @requires_auth
    def dashboard():
        return render_template('dashboard.html',
                               userinfo=session[constants.PROFILE_KEY],
                               userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD], indent=4))

    # END GLOBAL HTTP CONFIGURATIONS

    @app.route("/api/v1.0/spec")
    def spec():
        swag = swagger(app, prefix='/api/v1.0')
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "Flask Starter API"
        return jsonify(swag)

    if os.environ.get('WORK_ENV') == 'PROD':
        db.init_app(app)
        with app.app_context():
            # from api.models import *
            db.create_all()

        logging.basicConfig(stream=sys.stdout,
                            format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',
                            level=logging.DEBUG)
    return app
