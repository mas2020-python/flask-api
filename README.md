# Python Flask API Template

This application is a skeleton to start create you own Flask API Server in Python.
Documentation can be found here:

- for Flask-SQLAlchemy take a look [here](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- for Flask-JWT-Extended take a look [here](https://flask-jwt-extended.readthedocs.io/en/stable/)
- for Flask-RESTful take a look [here](https://flask-restful.readthedocs.io/en/latest/)

## Open points

This a list of open points to deal with:

- go in deep into SQLALchemy as a possible ORM to use

## Installation

After you clone the repo you need:

- install python virtual env

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
```

- install all the modules

```shell
pip3 install -r deploy/requirements.txt
```

- in case of testing with sqlite3 to create DB type:

```shell
python3 src/create_sqlite_test.py
```

## Configuration files

There are three main configuration files located in config folder:

- **api-server.toml**: it is the main configuration file for the API Application. All the variables are commented out.
  
- **uwsgi.ini**: configuration file for the uwsgi server.

## ENV variables
To execute the API server config accordingly these variables:
- DB_CONNECTION: the connection string for SQL Alchemy, e.g. "postgresql+psycopg2://postgres:mysecretpassword@db/postgres"

## Run the application

The application can be executed in two ways:

- in `test` environment with Flask integrated server and debug
- in `production` environment with [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/index.html)

You can find major information in the following chapters.

### Run in test environment

Examples for test using sqlite:

```shell
export DB_CONNECTION=sqlite:///data.db
python3 src/app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
2020-07-28 12:53:02,869 [INFO] werkzeug -  * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
2020-07-28 12:53:02,870 [INFO] werkzeug -  * Restarting with stat
2020-07-28 12:53:03,223 [INFO] sampleLogger - Application is starting in TEST environment (version: 0.1.0)
2020-07-28 12:53:03,230 [WARNING] werkzeug -  * Debugger is active!
```

### Run in a docker container

To build the container to the last version:
```shell
cd <project-folder>/flask_api
docker build -t flask-api:dev -f deploy/Dockerfile.dev .
```

To `run` the container in foreground type (using sqlite for test):

```shell
docker run -ti --rm --name flask-api \
-p 8080:8080 \
-v $PWD:/usr/src/flask-api \
-e DB_CONNECTION=sqlite:///data.db \
flask-api:dev
```

or, to execute in background type:

```shell
docker run -ti --rm -d --name flask-api \
-p 8080:8080 \
-v $PWD:/usr/src/flask-api \
-e DB_CONNECTION=sqlite:///data.db \
flask-api:dev
```

to start the entire solution (with postgresql) with the `docker compose` type:
```
docker-compose -f $PWD/deploy/docker-compose.yaml up
```

to start only a single service with the `docker compose` type:
```
docker-compose -f $PWD/deploy/docker-compose.yaml up <service-name>
```

e.g. to start only using sqlite3 (comment sections regarding postgresql):
```
docker-compose -f $PWD/deploy/docker-compose.yaml up flask-api
```

### Test with Postgres using a Docker container

This use case refers to:
- use Postgres in a docker container
- use the application outside a container
To test with Postgresql in a Docker container, create first a folder on the host to save the cluster data, for instance suppose you have set ~/postgresql/data, type:
```shell
docker run -d \
--name some-postgres \
-e POSTGRES_PASSWORD=mysecretpassword \
-e PGDATA=/var/lib/postgresql/data/pgdata \
-v ~/postgresql/data:/var/lib/postgresql/data \
-p 5432:5432 \
postgres
```
to connect through the console type:
```shell
docker exec -ti some-postgres psql -h localhost -U postgres
```
as connection string for SQL Alchemy use:
```
db_connection="postgresql+psycopg2://postgres:mysecretpassword@localhost/postgres"
```

### Run in production (local) environment

####`------- TESTING FROM HERE -----`
To run in a local `PRODUCTION` environment (always for testing) use:

```shell
<path-to-uwsgi-bin>/uwsgi --http-socket :8080 --module app:app --uid <user> --gid <user> --master --process 2 --threads 2 --env=APISRV_ENV=prod
```

for example:

```shell
flask-env/bin/uwsgi --http-socket :8080 --module app:app --uid andrea --gid andrea --master --ini code/config/uwsgi.ini --env=APISRV_ENV=prod
```

or, if you use the uwsgi.ini file you can use:

```shell
venv/bin/uwsgi \
--master --ini src/config/uwsgi.ini
```

to run with **emperor**:

```shell
flask-env/bin/uwsgi \
--uid andrea --gid andrea \
--master --die-on-term --emperor code/config/uwsgi.ini \
--env=APISRV_ENV=prod --logto code/log/emperor.log
```

create under code/config/uwsgi.ini the config file:

```ini
[uwsgi]
base = /Users/andrea.genovesi/development/python/projects/flask-api
app = app
module = %(app)
callable = app

# change dir to the python main folder that contains app.py
chdir=%(base)/code

#socket = %(base)/socket.sock
http-socket = :8080

# processes configuration
processes = 3
threads = 3
harakiri = 15

logto = %(base)/code/log/%n.log
```

### Run in production environment (TODO)

To run in production it might be a good solution to run uwsgi server behind a HTTP proxy server as Nginx.
This paragraph will be updated with major informartion as soon as they become available.
