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
pip3 install Flask-JWT
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

***UNDER REVISION FOR UWSGI: change with uwsgi***
- in production mode with [gunicorn](https://docs.gunicorn.org/en/stable/run.html)

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

### Run in production environment

To run in `PRODUCTION` use:

```shell
╰─$ export APPFALC_ENV=prod
gunicorn -b localhost:8080 app:app
```

- -c option is to set the right gunicorn configuration file.
It is always possible to hide the server behind a proxy server like Ngnix or hosted in a Docker container. For more specific information check the official documentation.
To read the config file type:

```shell
gunicorn -c config/gunicorn.conf.py
```

Major info on gunicorn installation and run can be found [here](https://medium.com/@thucnc/deploy-a-python-flask-restful-api-app-with-gunicorn-supervisor-and-nginx-62b20d62691f).