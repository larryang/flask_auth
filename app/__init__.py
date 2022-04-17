"""A simple flask web app"""
import os
import time
import flask_login

from flask import g, request
from flask import render_template, Flask
from flask.logging import default_handler
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect
from app.auth import auth
from app.cli import create_database
from app.context_processors import utility_text_processors
from app.db import db
from app.db.models import User
from app.exceptions import http_exceptions
from app.simple_pages import simple_pages
from applog import LogFormat, LoggingHandler, TimeCalc


login_manager = flask_login.LoginManager()


def page_not_found(e): # pylint: disable=unused-argument,invalid-name
    """ implement 404 error handler """
    return render_template("404.html"), 404


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.secret_key = 'This is an INSECURE secret!! DO NOT use this in production!!'
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf = CSRFProtect(app) # pylint: disable=unused-variable
    bootstrap = Bootstrap5(app) # pylint: disable=unused-variable
    app.register_blueprint(simple_pages)
    app.register_blueprint(auth)
    app.context_processor(utility_text_processors)
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'Simplex'
    app.register_error_handler(404, page_not_found)
    # app.add_url_rule("/", endpoint="index")
    db_dir = "database/db.sqlite"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath(db_dir)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    # add command function to cli commands
    app.cli.add_command(create_database)

    # Deactivate the default flask logger so that log messages don't get duplicated
    app.logger.removeHandler(default_handler) # pylint: disable=no-member

    # construct path to logging directory
    logdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

    # create logger handler and configure it
    handler = LoggingHandler.create(logdir, 'info.log')

    # Add the handler for the log entry
    app.logger.addHandler(handler) # pylint: disable=no-member

    @app.before_request
    def start_timer():
        g.start = time.time()

    @app.after_request
    def log_request(response):
        if request.path == '/favicon.ico':
            return response
        elif request.path.startswith('/static'):
            return response
        elif request.path.startswith('/bootstrap'):
            return response

        timestamp, duration = TimeCalc.calc(g.start)

        # use log handler and add extra parameters
        log_params = [
            ('status', response.status_code),
            ('duration', duration),
            ('time', timestamp),
        ]
        line = LogFormat.print_log_params(log_params)
        app.logger.info(line) # pylint: disable=no-member

        return response

    return app


@login_manager.user_loader
def user_loader(user_id):
    """ get user info from model """
    try:
        return User.query.get(int(user_id))
    except: # pylint: disable=bare-except
        return None
