""" logging configuration file """
import logging
import os
import json
from logging.config import dictConfig

import flask
from flask import request, current_app

from app.logging_config.log_formatters import RequestFormatter

log_con = flask.Blueprint('log_con', __name__)

@log_con.before_app_request
def before_request_logging():
    """ log before request """

    # log to request.log
    log = logging.getLogger("request")
    log.info("Before Request")

    # log to myapp.log
    log = logging.getLogger("myApp")
    log.info("My App Logger")


@log_con.after_app_request
def after_request_logging(response):
    """ log after request to request.log and myapp.log """
    
    # skip logging for below 
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response
    elif request.path.startswith('/bootstrap'):
        return response

    # log to request.log
    log = logging.getLogger("request")
    log.info("After Request")

    log = logging.getLogger("myApp")
    log.info("My App Logger")
    return response


@log_con.before_app_first_request
def configure_logging():
    """ before app startup logging config """
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, 'logging_config.json')
    with open(filepath, encoding="utf-8") as file:
        logging_config = json.load(file)
    logging.config.dictConfig(logging_config)

    # log to logfile misc_debug.log
    log = logging.getLogger("misc_debug")
    log.debug("Just configured logging from LOGGING_CONFIG")

    # log to logfile myapp.log
    log = logging.getLogger("myApp")
    log.info("Before app first request")

    # log to logfile errors.log
    log = logging.getLogger("myerrors")
    log.info("Before app first request")
