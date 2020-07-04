# Python Flask API Template

This application is a skeleton to start create you own Flask API Server in Python.

## Installation

After you clone the repo you need:

- install python virtual env

```shell
python3 -m venv flask-env
pip install --upgrade pip
source flask-env/bin/activate
```

- (first way) install all the modules

```shell
pip3 install flask
pip3 install Flask-RESTful
pip3 install toml
pip3 install Flask-JWT
# take a look to the installed libraries
pip3 freeze
```

- (second way) install all the modules
```shell
pip3 install -r requirements.txt
```

## Configuration files

There are three main configuration files located in config folder:

- api-server.toml
It is the main configuration file for the API Application. All the variables are commented out.

- gunicorn.conf.py
It is the file for the gunicorn WSGI server configuration

- log.conf
Configuration file for the logging of the entire application

--- ***UNDER REVIEW FROM HERE***
## Launch the application

The application can be executed in two ways:

- in test mode with debugger
- in production mode trough the gunicorn server

To switch between these two envs set accordingly the ENV variable APPFALC_ENV with:

- `test`: the application starts with waitress server in local. This modality can be used in local environment or inside an IDE as PyCharm or VS Code.
- `prod`: set this value the application can start only with a WSGI server.

### Run in test environment

Examples for test:

```shell
╰─$ export APPFALC_ENV=test
╰─$ python3 app.py
Serving on http://localhost:8080
Serving on http://localhost:8080
```

if you run the same code with APPFALC_ENV set to prod you get:

```shell
╰─$ python3 app.py
2020-06-23 12:12:27,766 [INFO] sampleLogger - API Server is listening on localhost:8080
```

and the process is immediately stopped.

### Run in production environment

To run in `PRODUCTION` use:

```shell
╰─$ export APPFALC_ENV=prod
gunicorn -c config/gunicorn.conf.py app:api
```

-c option is to set the right gunicorn configuration file.
It is always possible to hide the server behind a proxy server like Ngnix or hosted in a Docker container.
