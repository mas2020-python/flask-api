# file gunicorn.conf.py
# coding=utf-8
# Reference: https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
import os
import multiprocessing

_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..'))
_VAR = os.path.join(_ROOT, 'var')
_ETC = os.path.join(_ROOT, 'etc')

errorlog = 'log/api-server.log'
loglevel = 'info'
# accesslog = '-'
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# bind = 'unix:%s' % os.path.join(_VAR, 'run/gunicorn.sock')
bind = 'localhost:8080'
workers = 1
#workers = multiprocessing.cpu_count() * 2 + 1

timeout = 3 * 60  # 3 minutes
keepalive = 24 * 60 * 60  # 1 day

capture_output = True