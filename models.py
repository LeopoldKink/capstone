import json
from json import JSONEncoder
import dateutil.parser
import babel
import flask
import datetime
from datetime import datetime, date, timedelta
from flask import Flask, render_template, jsonify, request, Response, flash, redirect, url_for, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import desc



db = SQLAlchemy()
migrate = Migrate()

class Exercice(db.Model):  
    __tablename__ = 'exercice'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    difficulty = db.Column(db.Integer)
    muscles = db.Column(db.String())
    requirements = db.Column(db.String())
    likes = db.Column(db.Integer, default=0)
    video_path = db.Column(db.String())

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'difficulty': self.difficulty,
        'muscles': self.muscles,
        'requirements': self.requirements,
        'likes': self.likes,
        'video_path': self.video_path
        }



class Instructor(db.Model):  
    __tablename__ = 'instructor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    profile_pic_path = db.Column(db.String())


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'profile_pic_path': self.profile_pic_path
        }