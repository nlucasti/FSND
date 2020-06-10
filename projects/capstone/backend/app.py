from dateutil.parser import parse
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime
from auth.auth import AuthError, requires_auth
from database.models import setup_db, Movies, Actors, Casts
from database.models import db_drop_and_create_all


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"*": {"origins": "*"}})
    db = SQLAlchemy()
    '''
     Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actors.query.all()
        result = {"success": "True", "actors": [a.format() for a in actors]}
        return jsonify(result)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:delete_actors')
    def delete_actors(jwt, id):
        actor = Actors.query.filter(Actors.id == id).one_or_none()

        if actor:
            actor.delete()
            result = {"success": "True", "actors": actor.format()}
        else:
            abort(404)
        return jsonify(result)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:create_actors')
    def create_actors(jwt):
        name = request.get_json()['name']
        age = request.get_json()['age']
        gender = request.get_json()['gender']

        actor = Actors(
            name=name,
            age=age,
            gender=gender)
        if actor:
            actor.insert()
            result = {"success": "True", "actors": actor.format()}
            return jsonify(result)
        else:
            abort(404)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:edit_actors')
    def edit_actors(jwt, id):
        actor = Actors.query.filter(Actors.id == id).one_or_none()
        if actor:
            try:
                actor.name = request.get_json()['name']
            except KeyError:
                actor.name = actor.name
            try:
                actor.age = request.get_json()['age']
            except KeyError:
                actor.age = actor.age
            try:
                actor.gender = request.get_json()['gender']
            except KeyError:
                actor.gender
            actor.update()
            result = {"success": "True", "actors": actor.format()}
        else:
            abort(404)
        return jsonify(result)
#####
#####
    @app.route('/casts', methods=['GET'])
    @requires_auth('get:casts')
    def get_casts(jwt):
        try:
            casts = db.session.query(Casts.actor_id,
                                     Casts.id,
                                     Casts.movie_id,
                                     Actors.name,
                                     Actors.age,
                                     Actors.gender).join(Actors).all()
            # do something with the session
        except SQLAlchemyError:
            db.session.rollback()
        else:
            db.session.commit()
            records = []
            for x in casts:
                data = {
                    "actor_id": x.actor_id,
                    "id": x.id,
                    "movie_id": x.movie_id,
                    'name': x.name,
                    'age': x.age,
                    'gender': x.gender
                }
                records.append(data)

            result = {"success": "True", "casts": records}
            return jsonify(result)
        result = {"success": "False", "casts": []}
        return jsonify(result)

    @app.route('/casts/<int:id>', methods=['DELETE'])
    @requires_auth('delete:delete_casts')
    def delete_casts(jwt, id):
        cast = Casts.query.filter(Casts.id == id).one_or_none()

        if cast:
            cast.delete()
            result = {"success": "True", "casts": cast.format()}
        else:
            abort(404)
        return jsonify(result)

    @app.route('/casts', methods=['POST'])
    @requires_auth('post:create_casts')
    def create_casts(jwt):
        movie_id = request.get_json()['movie_id']
        actor_id = request.get_json()['actor_id']
        records = []
        for m in movie_id:
            cast = Casts(movie_id=m, actor_id=actor_id)
            if cast:
                cast.insert()
            else:
                abort(404)
            records.append(cast)
        result = {"success": "True",
                  "casts": [cast.format() for cast in records]}
        return jsonify(result)

    @app.route('/casts/<int:id>', methods=['PATCH'])
    @requires_auth('patch:edit_casts')
    def edit_casts(jwt, id):
        cast = Casts.query.filter(Casts.id == id).one_or_none()
        if cast:
            try:
                cast.movie_id = request.get_json()['movie_id']
            except KeyError:
                pass
            try:
                cast.actor_id = request.get_json()['actor_id']
            except KeyError:
                pass
            cast.update()
            result = {"success": "True", "casts": cast.format()}
        else:
            abort(404)
        return jsonify(result)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        movies = Movies.query.all()
        result = {"success": "True", "movies": [m.format() for m in movies]}
        return jsonify(result)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:delete_movies')
    def delete_movies(jwt, id):
        movie = Movies.query.filter(Movies.id == id).one_or_none()

        if movie:
            movie.delete()
            result = {"success": "True", "movies": movie.format()}
        else:
            abort(404)
        return jsonify(result)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:create_movies')
    def create_movies(jwt):
        title = request.get_json()['title']
        release_date = request.get_json()['release_date']
        img_link = request.get_json()['img_link']
        movie = Movies(
            title=title,
            release_date=parse(release_date),
            img_link=img_link)
        if movie:
            movie.insert()
            result = {"success": "True", "movies": movie.format()}
            return jsonify(result)
        else:
            abort(404)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:edit_movies')
    def edit_movies(jwt, id):
        movie = Movies.query.filter(Movies.id == id).one_or_none()
        if movie:
            try:
                movie.title = request.get_json()['title']
            except KeyError:
                pass
            try:
                movie.release_date = parse(request.get_json()['release_date'])
            except KeyError:
                pass
            try:
                movie.img_link = request.get_json()['img_link']
            except KeyError:
                pass
            movie.update()
            result = {"success": "True", "movies": movie.format()}
            print(result)
        else:
            abort(404)
        return jsonify(result)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(AuthError)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400
    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
