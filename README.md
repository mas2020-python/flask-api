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

IMPORTANT: using Postgres you need to have installed the library:

```shell
pip install psycopg2
```

## Configuration files

There are three main configuration files located in config folder:

- **api-server.toml**: it is the main configuration file for the API Application. All the variables are commented out.

- **logging.conf**: configuration file for the logging of the entire application.
  
- **uwsgi.ini**: configuration file for the uwsgi server.
  
## Launch the application

The application can be executed in two ways:

- in test environment with Flask integrated server and debug
- in production environment with [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/index.html)

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

### Run in a docker container

To build the container to the last version:
```shell
docker build -t flask-api:dev -f deployments/Dockerfile_dev .
```

To execute the container type in foreground type:
```
docker run -ti --name flask-api -p 8080:8080 --rm -v $PWD/log:/usr/src/flask-api/log flask-api:dev
```
or, to execute in background type:
```
docker run -d --name flask-api -p 8080:8080 --rm -v l-v $PWD/log:/usr/src/flask-api/log flask-api:dev
```


### Run in production (local) environment

To run in a local `PRODUCTION` environment (always for test purpose) use:

```shell
<path-to-uwsgi-bin>/uwsgi --http-socket :8080 --module app:app --uid <user> --gid <user> --master --process 2 --threads 2 --env=APISRV_ENV=prod

```

for example:

```shell
flask-env/bin/uwsgi --http-socket :8080 --module app:app --uid andrea --gid andrea --master --ini code/config/uwsgi.ini --env=APISRV_ENV=prod
```

or, if you use the uwsgi.ini file you can use:

```shell
flask-env/bin/uwsgi \
--uid andrea --gid andrea \
--master --ini code/config/uwsgi.ini \
--env=APISRV_ENV=prod
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
