# Full Stack Nano Degree Capstone

## Casting Agency

This webapp allows a user to match actors with movies. The motivation for this work was to demonstrate a pythonic backend, relational databases, REST, and frontend web development using AngularJS-based frameworks.

The frontend provides a single page web app powered by the ionic framework and angularjs. This allows it to be both interactive and portable to mobile devices.

The backend api has three models: Actors, Movies, and Cast. Each of these models has separate permissions and authentication. Authentication is done using Auth0. Auth0 creates three unique roles: executive producer, casting director, and casting assistant.
The permissions are as shown below:

-Casting Assistant
  -Can view actors and movies
-Casting Director
  -Can view actors and movies
  -Add or delete an actor from the database
  -Modify actors or movies
Executive Producer
  -Can view actors and movies
  -Add or delete an actor from the database
  -Modify actors or movies
  -Add or delete a movie from the database

The backend maintains data on a Postgres instance.

Both the backend and frontend are hosted on the Heroku platform.
Frontend:https://fsnd-casting-frontend.herokuapp.com/
Backend: https://fsnd-casting-app.herokuapp.com/

## About the Stack

### Backend

The `./backend` directory contains a completed Flask and SQLAlchemy server. The workhorse is mainly `app.py` while `models.py` creates the models. The db is also setup for DB migrations so that it does not become out of sync with the latest iteration.

If hosting locally, install the required dependencies using:

```bash
pip install -r requirements.txt
```

To start the server, run the following command:

```bash
python app.py
```
The endpoints are as shown below:

`GET \movies`
This endpoint gets all the movies from the db.

`GET \actors`
This endpoint gets all the actors from the db.

`GET \casts`
This endpoint gets all the casts from the db.

`POST \movies`
```
request:
{
    "title": [TITLE],
    "release_date": [RELEASE_DATE],
    "img_link": [IMG_LINK]
}
```

This endpoint posts a new movie to the db.

`POST \actors`
```
request:
{
    "name": [NAME],
    "age": [AGE],
    "gender": [GENDER]
}
```

This endpoint posts a new actor to the db.

`POST \casts`
```
request:
{
    "movie_id": [MOVIE_ID],
    "actor_id": [ACTOR_ID]
}
```

This endpoint posts a new cast to the db.

`PATCH \movies\<movie id>`
```
request:
{
    "title": [TITLE],
    "release_date": [RELEASE_DATE],
    "img_link": [IMG_LINK]
}
```

This endpoint patches a movie in the db.

`PATCH \actors\<actor id>`
```
request:
{
    "name": [NAME],
    "age": [AGE],
    "gender": [GENDER]
}
```

This endpoint patches an actor in the db.

`PATCH \casts\<cast id>`
```
request:
{
    "movie_id": [MOVIE_ID],
    "actor_id": [ACTOR_ID]
}
```

This endpoint patches a cast in the db.

`DELETE \movies\<movie id>`

This endpoint deletes a movie from the db.

`DELETE \actors\<actor id>`

This endpoint deletes an actor from the db.

`DELETE \casts\<cast id>`

This endpoint deletes a cast from the db.

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. Ionic is a framework that is built on top of AngularJS.

If hosting locally, install the required dependencies using:

```bash
ionic install
```

To start the server, run the following command:

```bash
ionic start
```


### Heroku

The application is hosted on Heroku. The links are as follows:

Frontend:https://fsnd-casting-frontend.herokuapp.com/
Backend: https://fsnd-casting-app.herokuapp.com/

To test the program on Heroku, you can use the provided Postman collection, or test the endpoints using curl, which I will not explore here.

A program `test_app.py` was written to provide unittests for each endpoint and error behavior. It can either be run locally, or run on the Heroku server by using the following command:

```bash
heroku run python test_app.py --app fsnd-casting-app
```

It must be noted that a valid Heroku login with app permissions is required to run the program in this manner.
