"""Logger Classes and Methods """
import logging
import os
import time
import datetime

from rfc3339 import rfc3339
from flask import request, has_request_context

# TODO unit test classes and methods

class RequestLoggerFormatter(logging.Formatter):
    """ derived implement Formmatter """
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.request_method = request.method
            record.request_path = request.path
            record.request_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            record.host = request.host.split(':', 1)[0]
            record.request_id = request.headers.get('X-Request-ID')
            record.args = dict(request.args)
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


class LoggingHandler():
    """ factory to create handler """

    @staticmethod
    def create(logdir, filename):
        """ method to create handler to log to log_file """

        # make a directory if it doesn't exist
        if not os.path.exists(logdir):
            os.mkdir(logdir)

        # set name of the log file
        log_file = os.path.join(logdir, filename)

        handler = logging.FileHandler(log_file)

        formatter = RequestLoggerFormatter(
            '%(levelname)s,"%(asctime)s",%(module)s,"%(message)s",%(remote_addr)s,"%(url)s"\n'
            '\t%(request_path)s,%(request_ip)s,%(host)s,"%(args)s"'
        )

        # set the formatter for the log entry
        handler.setFormatter(formatter)
        # Set the logging level of the file handler object so that it logs INFO and up
        handler.setLevel(logging.INFO)

        return handler


class TimeCalc():
    """ get current time and calculate duration """

    @staticmethod
    def calc(previous_time):
        """ give current time and delta with previous time """
        now = time.time()
        datetime_ts = datetime.datetime.fromtimestamp(now)

        return rfc3339(datetime_ts, utc=True), round(now - previous_time, 2)


class LogFormat():
    """ log formatting helpers """

    @staticmethod
    def print_log_params(log_params):
        """ format list of params and values suitable for printing """
        parts = []
        for name, value in log_params:
            part = name + ': ' + str(value) + ' '
            parts.append(part)

        return " ".join(parts).rstrip()
        