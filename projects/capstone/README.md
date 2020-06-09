# Full Stack Nano Degree Capstone

## Casting Agency

This webapp allows a user to match actors with movies.

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
