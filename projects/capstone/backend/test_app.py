import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Movies, Actors

headers = {'Authorization': 'Bearer ' + os.environ['AUTH_TOKEN']}
headers_casting = {'Authorization': 'Bearer ' + os.environ['AUTH_TOKEN_CAST']}

movie_id = -1
actor_id = -1
class AppTestCase(unittest.TestCase):
    """This class represents the application test case"""



    # @app.before_request
    # def before_request(request):
    #     request.headers.add(
    #     'Authorization': 'Bearer ' + os.environ['AUTH_TOKEN']
    #     )
    #     return request

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        @self.app.after_request
        def after_request(response):
            response.headers.add(
                'Access-Control-Allow-Headers',
                'Content-Type, Authorization')
            response.headers.add(
                'Access-Control-Allow-Methods',
                'GET, POST, PATCH, DELETE, OPTIONS')
            return response
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """

    def test_get_movies(self):
        res = self.client().get('/movies', headers=headers)
        data = json.loads(res.data)
        print('Get Movies')
        print('*'*40)
        print(data)

        self.assertEqual(res.status_code, 200)
        print('*'*40)

    def test_get_actors(self):
        res = self.client().get('/actors', headers=headers)
        data = json.loads(res.data)
        print('Get Actors')
        print('*'*40)
        print(data)

        self.assertEqual(res.status_code, 200)
        print('*'*40)

    def test_delete_actors(self):
        res = self.client().delete('/actors/'+str(actor_id), headers=headers)
        data = json.loads(res.data)
        print('Delete Actors')
        print('*'*40)
        print(data)

        self.assertEqual(res.status_code, 200)
        print('*'*40)

    def test_delete_movies(self):
        res = self.client().delete('/movies/'+str(movie_id), headers=headers)
        print(movie_id)
        data = json.loads(res.data)
        print('Delete Movies')
        print('*'*40)
        print(data)
        self.assertEqual(res.status_code, 200)
        print('*'*40)

    def test_create_new_movie(self):
        global movie_id
        res = self.client().post(
            '/movies',
            json={
                "img_link": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Bg-easter-eggs.jpg/1200px-Bg-easter-eggs.jpg",
                "release_date": "2008-02-20",
                "title": "Easter Egg"}, headers=headers)
        data = json.loads(res.data)
        print('Create New Movie')
        print('*'*40)
        print(data)
        print(data["movies"]["id"])
        movie_id = data["movies"]["id"]

        self.assertEqual(res.status_code, 200)
        print('*'*40)

    def test_create_new_actor(self):
        global actor_id
        res = self.client().post(
            '/actors',
            json={
                "age": "22",
                "gender": "M",
                "name": "Adam Sandler"}, headers=headers)
        data = json.loads(res.data)
        print('Create New Actor')
        print('*'*40)
        print(data)

        actor_id = data["actors"]["id"]
        self.assertEqual(res.status_code, 200)
        print('*'*40)

    def test_create_patch_actor(self):
        res = self.client().patch(
            '/actors/'+str(actor_id),
            json={
                "age": "57"}, headers=headers)
        data = json.loads(res.data)
        print('Patch Actor')
        print('*'*40)
        print(data)
        self.assertEqual(res.status_code, 200)
        print('*'*40)

    def test_create_patch_movie(self):
        res = self.client().patch(
            '/movies/'+str(movie_id),
            json={
                "release_date": "2020-02-20"}, headers=headers)
        data = json.loads(res.data)
        print('Patch Movie')
        print('*'*40)
        print(data)
        self.assertEqual(res.status_code, 200)
        print('*'*40)

    def test_RBAC_exec(self):
        res = self.client().patch(
            '/movies/1',
            json={
                "release_date": "2020-02-21"}, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_RBAC_cast(self):
        res = self.client().patch(
            '/movies/1',
            json={
                "release_date": "2020-02-21"}, headers=headers_casting)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_404(self):
        res = self.client().patch('/movies/5000', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_405(self):
        res = self.client().get('/movies/5', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)

    def test_401(self):
        res = self.client().post(
            '/movies',
            json={
                "img_link": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Bg-easter-eggs.jpg/1200px-Bg-easter-eggs.jpg",
                "release_date": "2008-02-20",
                "title": "Easter Egg"}, headers={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpTQzR0bVlkYjVVUFBIaUltU2swUSJ9.eyJpc3MiOiJodHRwczovL25sLWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYjMxNzNlNmI2OWJjMGMxMmZjNzQxMCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1OTEzMTgzMjQsImV4cCI6MTU5MTQwNDcyMywiYXpwIjoiaVhCSGJNS1JYT3M4S3JrM1RmaW9KUThXT2NrY0RIMGUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkZWxldGVfYWN0b3JzIiwiZGVsZXRlOmRlbGV0ZV9jYXN0cyIsImRlbGV0ZTpkZWxldGVfbW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDpjYXN0cyIsImdldDptb3ZpZXMiLCJwYXRjaDplZGl0X2FjdG9ycyIsInBhdGNoOmVkaXRfY2FzdHMiLCJwYXRjaDplZGl0X21vdmllcyIsInBvc3Q6Y3JlYXRlX2FjdG9ycyIsInBvc3Q6Y3JlYXRlX2Nhc3RzIiwicG9zdDpjcmVhdGVfbW92aWVzIl19.km2h7blQUaQi_U8B08ONV2AbGAS40a4dmhUvGtRUUTHl2qtLmLa-PcbmrKs7o6n1cwsVokC725gKKyvXhkFYbcyjN-hm8AYC0GUq-ws-0Ct0DVOOjXIVQ7ZxS47I6QsuAo_ACFhYZ1gh2kg7X6j2yob4ePZ0fV2OTOzu5zZJtrFEZ6df-APQ0Ag8k5cziH6obfwtrecZBK3zLM3DSTQB_drVdqp4g-Q6B_rD5RAgF6rQUmM93cGWSSHNsEnwdDmvoFKGnVHxxuEtxlPwtTU9t2DdK9cRCwEAihAd4NxtsBuIig1LGS8Qh_7HEPLSgY6BiJi37yBo4oI1MKAH1Zj8LQ'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_500(self):
        res = self.client().post(
            '/movies',
            json={
                "img_link": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Bg-easter-eggs.jpg/1200px-Bg-easter-eggs.jpg",
                "release_date": "2008-02-20",
                "test": 11}, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)

    # def test_400(self):
    #     res = self.client().post('/movies/search', json= {"test":"1"})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
