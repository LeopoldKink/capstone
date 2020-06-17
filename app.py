import json
import os
from json import JSONEncoder
import dateutil.parser
import babel
import flask
import datetime
from flask import Flask, render_template, jsonify, request, Response, flash, redirect, url_for, send_from_directory, session, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_cors import CORS
from flask_wtf import Form
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import desc
import sys
from datetime import datetime, date, timedelta
from jinja2 import Template
import paypalrestsdk
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from flask_login import current_user
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, IntegerField, RadioField
import os
import smtplib
import imghdr
from email.message import EmailMessage
import urllib
import ssl
import flask.sessions
from werkzeug.utils import secure_filename

from auth.auth import AuthError, requires_auth, verify_decode_jwt
from models import db, migrate, Instructor, Exercice


def create_app(test_config=None):

    app = Flask(__name__)
    oauth = OAuth(app)
    db.init_app (app)
    migrate.init_app (app, db)
    CORS(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.config['SECRET_KEY'] = '5791628bb0b13cefhri3j0c676dtrfefeefde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    ###app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:haha@localhost:5432/fitness_api"

    # ACTIVE SETTING
    def getJSON(filePathAndName):
        with open(filePathAndName, 'r') as fp:
            return json.load(fp)

    setting_list = getJSON("./settings.json")
    active_setting_JSON = getJSON("./active_setting.json")
    active_setting = active_setting_JSON["setting"]

    for setting in setting_list:
        if setting["setting"] == active_setting:
            env = setting

    #Auth0

    auth0 = oauth.register(
        'auth0',
        client_id=env["auth0"]["client_id"],
        client_secret=env["auth0"]["client_secret"],
        api_base_url='https://hnc.auth0.com',
        access_token_url='https://hnc.auth0.com/oauth/token',
        authorize_url='https://hnc.auth0.com/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    @app.route('/callback')
    def callback_handling():
        # Handles response from token endpoint
        try:
            auth0.authorize_access_token()
            resp = auth0.get('userinfo')
            userinfo = resp.json()
            access_token = auth0.token['access_token']
            accessinfo = verify_decode_jwt(access_token)

            # Store the user information in flask session.
            session['accessinfo'] = accessinfo
            session['isLogged'] = True
            return redirect('/exercices')
        except:
            print(sys.exc_info())
            abort(404)

    @app.route('/login')
    def login():
        try:
            s = auth0.authorize_redirect(redirect_uri=env["auth0"]["redirect_uri"], audience='fitnessapi')
            return auth0.authorize_redirect(redirect_uri=env["auth0"]["redirect_uri"], audience='fitnessapi')
        except:
            print(sys.exc_info())
            abort(404)

    @app.route('/logout')
    def logout():
        try:
            # Clear session stored data
            session.clear()
            # Redirect user to logout endpoint
            params = {'returnTo': url_for(
                'index', _external=True), 'client_id': env["auth0"]["client_id"]}
            return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
        except:
            print(sys.exc_info())
            abort(404)


    #########################################################   GET  #########################################################   GET  ########################################### 


    @app.route('/exercices', methods=['GET'])
    def index():
        selection = Exercice.query.all()
        exercices = [Exercice.format() for Exercice in selection]
        
        return jsonify({'exercices' : exercices})


    @app.route('/instructors', methods=['GET'])
    def instructors():
        selection = Instructor.query.all()
        instructors = [Instructor.format() for Instructor in selection]
        
        return jsonify({'instructors' : instructors})


    @app.route('/instructors/<int:inst_id>', methods=['GET'])
    @requires_auth('get:instructor')
    def show_instructor(inst_id):
        success = False
        try:
            instructor = Instructor.query.filter(Instructor.id == inst_id).one_or_none()
            instructor_json = instructor.format()
            success = True
        except:
            print(sys.exc_info())
            abort(404)
        return jsonify({
            'instructor' : instructor_json,
            'success' : success
        })





    #########################################################   POST  #########################################################   POST  ########################################### 

    @app.route('/create/exercice', methods=['POST'])
    @requires_auth('post:workout')
    def create_exercice(accessinfo):
        success = False
        try:
            body = request.get_json()
            name = body['name']
            difficulty = body['difficulty']
            muscles = body['muscles']
            requirements = body['requirements']
            video_path = body['video_path']
            new_exercice = Exercice(name=name, difficulty=difficulty, muscles=muscles, requirements=requirements, video_path=video_path)
            db.session.add(new_exercice)
            db.session.commit()
            success = True
        except:
            print(sys.exc_info())
            abort(404)
        return jsonify({
            'success' : success,
            'created' : new_exercice.id,
            'exercice name' : new_exercice.name
        })

    @app.route('/create/instructor', methods=['POST'])
    @requires_auth('post:workout')
    def create_instructor(accessinfo):
        success = False
        try:
            body = request.get_json()
            name = body['name']
            profile_pic_path = body['profile_pic_path']
            age = body['age']
            new_instructor = Instructor(name=name, profile_pic_path=profile_pic_path, age=age)
            db.session.add(new_instructor)
            db.session.commit()
            success = True
        except:
            print(sys.exc_info())
            abort(404)
        return jsonify({
            'success' : success,
            'created' : new_instructor.id,
            'exercice name' : new_instructor.name
        })



    #########################################################   DELETE  #########################################################   DELETE  ########################################### 


    @app.route('/delete/exercice/<int:ex_id>', methods=['DELETE']) 
    @requires_auth('delete:workout')
    def delete_exercice(accessinfo, ex_id):
        success = False
        try:
            exercice = Exercice.query.filter(Exercice.id == ex_id).one_or_none()
            exercice.delete()
            success = True
        except:
            print(sys.exc_info())
            abort(404)
        return jsonify({
            'success' : success,
            'deleted' : exercice.id
        })

    #########################################################   PATCH  #########################################################   PATCH  ########################################### 

    @app.route('/patch/exercice/<int:ex_id>', methods=['PATCH'])
    @requires_auth('patch:workout')
    def patch_exercice(accessinfo, ex_id):
        success = False
        try:
            exercice = Exercice.query.filter(Exercice.id == ex_id).first()
            body = request.get_json()
            exercice.name = body['name']
            exercice.difficulty = body['difficulty']
            exercice.muscles = body['muscles']
            exercice.requirements = body['requirements']
            exercice.video_path = body['video_path']
            db.session.commit()
            success = True
        except:
            print(sys.exc_info())
            abort(404)
        return jsonify({
            'success' : success,
            'updated' : exercice.id,
            'exercice name' : exercice.name
        })


    #########################################################   ERRORS  #########################################################   ERRORS  ########################################### 


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404


    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized!"
        }), 401


    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405


    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden"
        }), 403

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized!"
        }), 401

    @app.errorhandler(500)
    def handle_500(e):
        '''
        original = getattr(e, "orig", None)

        if original is None:
            # direct 500 error, such as abort(500)
            return render_template("500.html"), 500
        '''
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server error"
        }), 500

    return app

app = create_app()