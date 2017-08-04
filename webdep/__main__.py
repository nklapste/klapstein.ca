""" __main__ file that contains the starting argparse function for the
cherrypy server """
import os
import argparse

import logging
from logging import handlers

from webdep import LOGDIR, BACKUP_COUNT
from webdep.server import start_server, start_bottle_server


def main():
    """ main argparse function that grabs the initial/default config
    for the cherrpy server"""
    parser = argparse.ArgumentParser(description="Discord magic card detail "
                                                 "parser")
    parser.add_argument("-o", "--host", default="127.0.0.1",
                        help="host to bind server too default: %(default)s")
    parser.add_argument("-p", "--port", default=9092,
                        help="port to bind server too default: %(default)s")

    group = parser.add_argument_group(title="Server Logging Config")
    group.add_argument("-d", "--debug", action="store_true",
                       help="set server logging level to DEBUG")
    group.add_argument("-l", "--logdir", action="store_true", default=LOGDIR,
                       help="set directory to save log files")

    args = parser.parse_args()

    # setup logging
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    __log__ = logging.getLogger("general")
    __log__.setLevel(log_level)

    # create a rotating file handler which logs even debug messages
    os.makedirs(args.logdir, exist_ok=True)
    logpath = os.path.join(args.logdir, "general.log")
    fh = handlers.TimedRotatingFileHandler(logpath, "D",
                                           backupCount=BACKUP_COUNT)
    fh.setLevel(log_level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add the handlers to __log__
    __log__.addHandler(ch)
    __log__.addHandler(fh)

    # start the server
    # start_server(args.host, args.port, args.logdir)
    start_bottle_server(args.host, args.port, args.logdir)

if __name__ == "__main__":
    main()
