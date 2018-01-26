"""Main module that contains the starting argparse function for the
cherrypy server"""

import os
import argparse

import logging
from logging import handlers

from klapstein_webdep import LOGDIR, BACKUP_COUNT
from klapstein_webdep.server import start_server, start_bottle_server


def main():
    """Main argparse function that grabs the initial/default config
    for the cherrpy server"""
    parser = argparse.ArgumentParser(description="Basic python server "
                                                 "framework for klapstein.ca")
    parser.add_argument("-o", "--host", default="127.0.0.1",
                        help="Host to bind server too default: %(default)s")
    parser.add_argument("-p", "--port", default=9092, type=int,
                        help="Port to bind server too default: %(default)s")

    group = parser.add_argument_group(title="Server Logging Config")
    group.add_argument("-d", "--debug", action="store_true",
                       help="Set server logging level to DEBUG")
    group.add_argument("-l", "--log-dir", dest="log_dir", action="store_true",
                       default=LOGDIR, help="Set directory to save log files")

    group = parser.add_argument_group(title="SSL Config")
    group.add_argument("-c", "-ssl-cert", dest="cert",
                       help="Path to your ssl certificate")
    group.add_argument("-k", "--ssl-key", dest="key",
                       help="Path to your ssl certificate's private key")
    group.add_argument("-b", "--ssl-bundle", dest="bundle",
                       help="Path to your ssl certificate's bundle chain")
    group.add_argument("--no-ssl", dest="no_ssl", action="store_true",
                       help="Disable SSL for this server instance")

    args = parser.parse_args()

    if not args.no_ssl and (args.cert is None or args.key is None):
        raise ValueError("Missing required SSL configs")

    # setup logging
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    __log__ = logging.getLogger("general")
    __log__.setLevel(log_level)

    # create a rotating file handler which logs even debug messages
    os.makedirs(args.log_dir, exist_ok=True)
    logpath = os.path.join(args.log_dir, "general.log")
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
    start_server(args.host, args.port, args.log_dir, cert=args.cert, key=args.key, bundle=args.bundle)
    # start_bottle_server(args.host, args.port, args.logdir)


if __name__ == "__main__":
    main()
