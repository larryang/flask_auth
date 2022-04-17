"""Logger Classes and Methods """
import logging
from flask import request, has_request_context

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
            record.args = dict(request.args)
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)
