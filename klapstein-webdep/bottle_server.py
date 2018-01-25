""" module that defines a bottle routing app that can grafted onto cherrypy """
import logging

from functools import wraps
from datetime import datetime

from bottle import Bottle, request, response, static_file

from webdep import PUBDIR
from webdep.templates import INDEX_TEMPLATE, ERROR_TEMPLATE


# get instance of general server log
__log__ = logging.getLogger("general")


def log_to_logger(fn):
    """
    Wrap a Bottle request so that a log line is emitted after it's handled.
    (This decorator can be extended to take the desired logger as a param.)
    """
    @wraps(fn)
    def _log_to_logger(*args, **kwargs):
        request_time = datetime.now()
        actual_response = fn(*args, **kwargs)
        # modify this to log exactly what you need:
        __log__.info("{} {} {} {} {}".format(
                request.remote_addr,
                request_time,
                request.method,
                request.url,
                response.status
            )
        )
        return actual_response
    return _log_to_logger


BOTTLE_APP = Bottle()
BOTTLE_APP.install(log_to_logger)


def log_bottle_error(request, response):
    """ log a bottle error event"""
    request_time = datetime.now()
    __log__.error("{} {} {} {} {}".format(
        request.remote_addr,
        request_time,
        request.method,
        request.url,
        response.status
        )
    )


@BOTTLE_APP.error(404)
def error404_page(error):
    """ custom error with jinja templating capability for the bottle app """
    log_bottle_error(request, response)
    error_vars = {
        "status": error.status,
        "message": error.body,
        "traceback": error.traceback,
        "version": None
    }

    return ERROR_TEMPLATE.render(error_vars)


@BOTTLE_APP.error(500)
def error500_page(error):
    """ custom error with jinja templating capability for the bottle app """
    log_bottle_error(request, response)
    error_vars = {
        "status": error.status,
        "message": error.body,
        "traceback": error.traceback,
        "version": None
    }
    return ERROR_TEMPLATE.render(error_vars)


@BOTTLE_APP.route('/<filepath:path>')
def server_static(filepath):
    """ server content that is requested from the public directory """
    return static_file(filepath, root=PUBDIR)


@BOTTLE_APP.route("/", method="GET")
def index():
    """ home page """
    return INDEX_TEMPLATE.render()