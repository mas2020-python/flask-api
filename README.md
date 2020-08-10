# Python Flask API Template

This application is a skeleton to start create you own Flask API Server in Python.

## Open points

This a list of open points to deal with:

- import flask-jwt-extended package to manage creation and access to the JWT [token](https://flask-jwt-extended.readthedocs.io/en/stable/)
- go in deep into SQLALchemy as a possible ORM to use

## Installation

After you clone the repo you need:

- install python virtual env

```shell
python3 -m venv flask-env
source flask-env/bin/activate
pip3 install --upgrade pip
```

- (first way) install all the modules

```shell
pip3 install flask
pip3 install Flask-RESTful
pip3 install toml
pip3 install Flask-JWT-Extended
pip3 install Flask-SQLAlchemy
pip3 install uswgi
# take a look to the installed libraries
pip3 freeze
```

- (second way) install all the modules

```shell
pip3 install -r requirements.txt
```

- in case of testing with sqlite3 to install DB type:

```shell
python3 code/tmpdb.py
```

- in case of using Postgres you need to have a valid Postgres installion to refer to and you need to create the following table:

```shell
CREATE TABLE items
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  price REAL);


```

IMPORTANT: using Postgres you need to have installed the library:

```shell
pip install psycopg2
```

## Configuration files

There are three main configuration files located in config folder:

- **api-server.toml**: it is the main configuration file for the API Application. All the variables are commented out.

- **log.conf**: configuration file for the logging of the entire application.

## Launch the application

The application can be executed in two ways:

- in test mode with Flask integrated server and debug
- in production mode with [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/index.html)

To switch between these two envs set accordingly the ENV variable APISRV_ENV with:

- `test`: the application starts with included server in local. This modality can be used in local environment or inside an IDE as PyCharm or VS Code.
- `prod`: set this value the application can start only with a WSGI server.

**IMPORTANT**: if APISRV_ENV is not set an error will be occurred.

### Run in test environment

Examples for test:

```shell
╰─$ export APISRV_ENV=test
╰─$ cd code
╰─$ python3 app.py
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

### Run in production (local) environment

To run in a local `PRODUCTION` environment (always for test purpose) use:

```shell
<path-to-uwsgi-bin>/uwsgi --http-socket :8080 --module app:app --uid <user> --gid <user> --master --process 2 --threads 2 --env=APISRV_ENV=prod

```

for instance:

```shell
flask-env/bin/uwsgi --http-socket :8080 --module app:app --uid andrea --gid andrea --master --ini code/config/uwsgi.ini --env=APISRV_ENV=prod
```

if you use the uwsgi.ini file you can use:

```shell
<path-to-uwsgi-bin>/uwsgi --http-socket :8080 --module app:app --uid <user> --gid <user> --master --ini <path-to-ini-file> --env=APISRV_ENV=prod
```
to run with **emperor**:
```shell

```

### Run in production environment (TODO)

To run in production it might be a good solution to run uwsgi server behind a HTTP proxy server as Nginx.
This paragraph will be updated with major informartion as soon as they become available.
