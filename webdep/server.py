import logging

import cherrypy
from jinja2 import Environment, FileSystemLoader

from webdep import PUBDIR, WEBDIR

TEMPLATE_ENV = Environment(loader=FileSystemLoader(WEBDIR))
INDEX_TEMPLATE = TEMPLATE_ENV.get_template('index.html')
ERROR_TEMPLATE = TEMPLATE_ENV.get_template('error.html')

__log__ = logging.getLogger('basic_server_log')


def error_page(status, message, traceback, version):
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
    config = {
        'global': {
            'server.socket_host': host,
            'server.socket_port': port,
            'error_page.default': error_page,
        },
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': PUBDIR,
            "tools.sessions.on": True,
        }
    }
    cherrypy.quickstart(
        Root(),
        '/',
        config=config
    )


if __name__ == "__main__":
    start_server()