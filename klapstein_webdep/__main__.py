#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""Main module that contains the starting argparse function for the
cherrypy server"""

import os
import argparse
import logging
from logging import handlers, Formatter

import cherrypy

from klapstein_webdep import LOG_DIR, BACKUP_COUNT
from klapstein_webdep.server import start_server


def main():
    """Main argparse function that grabs the initial/default config
    for the cherrypy server"""
    parser = argparse.ArgumentParser(description="Basic python server "
                                                 "framework for klapstein.ca")
    parser.add_argument("-o", "--host", default="127.0.0.1",
                        help="Host to bind server too default: %(default)s")
    parser.add_argument("-p", "--port", default=9092, type=int,
                        help="Port to bind server too default: %(default)s")

    group = parser.add_argument_group(title="SSL Config")
    group.add_argument("-c", "-ssl-cert", dest="cert",
                       help="Path to your ssl certificate")
    group.add_argument("-k", "--ssl-key", dest="key",
                       help="Path to your ssl certificate's private key")
    group.add_argument("-b", "--ssl-bundle", dest="bundle",
                       help="Path to your ssl certificate's bundle chain")
    group.add_argument("--no-ssl", dest="no_ssl", action="store_true",
                       help="Disable SSL for this server instance")

    group = parser.add_argument_group(title="Logging config")
    group.add_argument("-v", "--verbose", action="store_true",
                       help="Enable verbose logging")
    group.add_argument("-f", "--log-dir", dest="log_dir", default=LOG_DIR,
                       help="Enable time rotating file logging at "
                            "the path specified")
    group.add_argument("-d", "--debug", action="store_true",
                       help="Enable DEBUG logging level")

    args = parser.parse_args()

    if not args.no_ssl and (args.cert is None or args.key is None):
        raise ValueError("Missing required SSL configs")

    # initialize logging
    handlers_ = list()

    if args.log_dir is not None:
        os.makedirs(args.log_dir, exist_ok=True)
        log_path = os.path.join(args.log_dir, "general.log")
        handlers_.append(
            logging.handlers.TimedRotatingFileHandler(
                log_path,
                when="D",
                interval=1,
                backupCount=BACKUP_COUNT
            )
        )

    if args.verbose:
        handlers_.append(logging.StreamHandler())
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(
        level=log_level,
        format="[%(asctime)s] - %(levelname)s - %(name)s - %(message)s",
        handlers=handlers_,
    )

    # setup cherrypy logging in detail (adding rotating file handler logging)
    setup_logging(args.log_dir, log_level)

    # start the server
    start_server(
        args.host,
        args.port,
        cert=args.cert,
        key=args.key,
        bundle=args.bundle
    )


def setup_logging(log_dir, log_level):
    """Setup cherrypy logging to be more advanced having a
    rotating file handler and logging to an internal directory"""
    log = cherrypy.log

    # Remove the default FileHandlers if present.
    log.error_file = ""
    log.access_file = ""

    # Make a new RotatingFileHandler for the error log.
    log_path = os.path.join(log_dir, "error.log")
    h = handlers.TimedRotatingFileHandler(log_path, "D",
                                          backupCount=BACKUP_COUNT)
    h.setLevel(log_level)
    h.setFormatter(Formatter(" %(message)s"))
    log.error_log.addHandler(h)
    log.error_log.propagate = False

    # Make a new RotatingFileHandler for the access log.
    log_path = os.path.join(log_dir, "access.log")
    h = handlers.TimedRotatingFileHandler(log_path, "D",
                                          backupCount=BACKUP_COUNT)
    h.setLevel(log_level)
    h.setFormatter(Formatter("%(message)s"))
    log.access_log.addHandler(h)
    log.access_log.propagate = False


if __name__ == "__main__":
    main()
