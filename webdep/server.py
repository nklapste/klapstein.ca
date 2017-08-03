""" server module that defines the cherrypy server deployment add your
options mainly here """

import os

import logging
from logging import handlers
import cherrypy
from jinja2 import Environment, FileSystemLoader

from webdep import PUBDIR, WEBDIR, LOGDIR, BACKUP_COUNT

TEMPLATE_ENV = Environment(loader=FileSystemLoader(WEBDIR))
INDEX_TEMPLATE = TEMPLATE_ENV.get_template("index.html")
ERROR_TEMPLATE = TEMPLATE_ENV.get_template("error.html")

# get instance of general server log
__log__ = logging.getLogger("general")


def error_page(status, message, traceback, version):
    """ custom error with jinja templating capability for the cherrypy server"""
    error_vars = {
        "status": status,
        "message": message,
        "traceback": traceback,
        "version": version
    }
    return ERROR_TEMPLATE.render(error_vars)


class Root(object):

    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        return INDEX_TEMPLATE.render()


def setup_logging():
    """ setup cherrypy logging to be more advanced having a
    rotating file handler and logging to an internal directory """
    log = cherrypy.log

    # Remove the default FileHandlers if present.
    log.error_file = ""
    log.access_file = ""

    # Make a new RotatingFileHandler for the error log.
    logpath = os.path.join(LOGDIR, "error.log")
    h = handlers.TimedRotatingFileHandler(logpath, "D",
                                          backupCount=BACKUP_COUNT)
    h.setLevel(logging.DEBUG)
    h.setFormatter(cherrypy._cplogging.logfmt)
    log.error_log.addHandler(h)

    # Make a new RotatingFileHandler for the access log.
    logpath = os.path.join(LOGDIR, "access.log")
    h = handlers.TimedRotatingFileHandler(logpath, "D",
                                          backupCount=BACKUP_COUNT)
    h.setLevel(logging.DEBUG)
    h.setFormatter(cherrypy._cplogging.logfmt)
    log.access_log.addHandler(h)


def start_server(host="127.0.0.1", port=9091):
    """ start the cherrypy server """
    config = {
        "global": {
            "server.socket_host": host,
            "server.socket_port": port,
            "error_page.default": error_page,
        },
        "/": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": PUBDIR,
            "tools.sessions.on": True,
        }
    }

    __log__.info("server startup with config: {}".format(config))

    # setup cherrypy logging in detail (adding rotating file handler logging)
    setup_logging()

    # start cherrypy server
    cherrypy.quickstart(
        Root(),
        "/",
        config=config
    )


if __name__ == "__main__":
    start_server()
