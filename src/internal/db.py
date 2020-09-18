"""
SQLAlchemy main file to map the database.
"""
from flask_sqlalchemy import SQLAlchemy, get_debug_queries
import logging
from utils.config import API_SRV

db = SQLAlchemy()

def sql_debug(response):
    logger = logging.getLogger(API_SRV.config['log']['default_logger'])
    queries = list(get_debug_queries())
    query_str = ''
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        # stmt = str(q.statement % q.parameters).replace('\n', '\n       ')
        stmt = q.statement + "\nparams: " + str(q.parameters)
        query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(q.duration * 1000, 2))

    logger.debug('=' * 80)
    logger.debug(' SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    logger.debug('=' * 80)

    logger.debug(query_str.rstrip('\n'))
    logger.debug('=' * 80 + '\n')

    return response