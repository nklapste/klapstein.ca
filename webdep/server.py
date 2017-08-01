""" server module that defines the cherrypy server deployment add your options mainly here """
import logging
import os

import cherrypy
from jinja2 import Environment, FileSystemLoader

from webdep import PUBDIR, WEBDIR, LOGDIR

TEMPLATE_ENV = Environment(loader=FileSystemLoader(WEBDIR))
INDEX_TEMPLATE = TEMPLATE_ENV.get_template('index.html')
ERROR_TEMPLATE = TEMPLATE_ENV.get_template('error.html')

__log__ = logging.getLogger('basic_server_log')


def error_page(status, message, traceback, version):
    """ custom error with jinja templating capability for the cherrypy server"""
    error_vars = {
        'status': status,
        'message': message,
        'traceback': traceback,
        'version': version
    }
    return ERROR_TEMPLATE.render(error_vars)


class Root(object):

    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        return INDEX_TEMPLATE.render()


def start_server(host='127.0.0.1', port=9091):
    """ start the cherrypy server """
    config = {
        'global': {
            'server.socket_host': host,
            'server.socket_port': port,
            'error_page.default': error_page,
            'log.access_file': os.path.join(LOGDIR, 'access.log'),
            'log.error_file': os.path.join(LOGDIR, 'error.log')
        },
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': PUBDIR,
            "tools.sessions.on": True,
        }
    }

    __log__.info('server startup with config: {}'.format(config))

    cherrypy.quickstart(
        Root(),
        '/',
        config=config
    )


if __name__ == "__main__":
    start_server()