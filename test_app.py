import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from app import create_app
from models import Exercice, Instructor
from dotenv import load_dotenv
from flask import session, request
import requests

from auth.auth import AuthError, requires_auth, verify_decode_jwt
from app import create_app


load_dotenv('.env')

admin_token = "Bearer {}".format(os.environ.get('admin_token'))
instructor_token = "Bearer {}".format(os.environ.get('instructor_token'))




class FitnessTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.admin = {
            "Content-Type": "application/json",         
            "Authorization": admin_token        #JWT
        }

        self.patch_admin = {
            "Content-Type": "application/json",         
            "Authorization": instructor_token        #JWT
        }

        self.new_exercice = {
            "name": "push ups",
            "difficulty": 1,
            "muscles":  "chest",
            "requirements": "nothing",
            "video_path": "https://youtube.com"
        }


    def tearDown(self):
        pass


##### GET

    def test_get_exercices(self):
        res = self.client().get('/exercices')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['exercices'])

    def test_get_instructors(self):
        res = self.client().get('instructors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['instructors'])

#POST

    def test_post_exercice(self):
        res = self.client().post('/create/exercice', json=self.new_exercice, headers={"Authorization": "Bearer {}".format(os.environ.get('admin_token'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['exercice name'], 'push ups')

    def test_post_exercice_not_allowed(self):
        res = self.client().post('/create/exercice', json=self.new_exercice)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

#DELETE

    def test_delete_exercice(self):
        res = self.client().delete('/delete/exercice/11', headers={"Authorization": "Bearer {}".format(os.environ.get('admin_token'))}) #IMPORTANT /delete/exercice/ last Value + 1 for next test
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_exercice_not_found(self):
        res = self.client().delete('/delete/exercice/999', headers={"Authorization": "Bearer {}".format(os.environ.get('admin_token'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')


#PATCH

    def test_patch_exercice(self):
        res = self.client().patch('/patch/exercice/3', json=self.new_exercice, headers={"Authorization": "Bearer {}".format(os.environ.get('admin_token'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_exercice_not_found(self):
        res = self.client().patch('/patch/exercice/999', json=self.new_exercice, headers={"Authorization": "Bearer {}".format(os.environ.get('admin_token'))})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

if __name__ == "__main__":
    unittest.main()