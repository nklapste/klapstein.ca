import argparse
import logging
import os

from webdep import LOGDIR
from webdep.server import start_server


def main():
    parser = argparse.ArgumentParser(description='Discord magic card detail parser')

    parser.add_argument('-o', '--host', default="127.0.0.1",
                        help='host to bind server too default: %(default)s')
    parser.add_argument('-p', '--port', default=9092,
                        help="port to bind server too default: %(default)s")

    group = parser.add_argument_group(title="Server Logging Config")
    group.add_argument("-d", "--debug", action="store_true",
                        help="set server logging level to DEBUG")

    args = parser.parse_args()

    # setup logging
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    __log__ = logging.getLogger('basic_server_log')
    __log__.setLevel(log_level)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(os.path.join(LOGDIR, 'general.log'))
    fh.setLevel(log_level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add the handlers to __log__
    __log__.addHandler(ch)
    __log__.addHandler(fh)

    # start the server
    start_server(
        args.host,
        args.port
    )

if __name__ == "__main__":
    main()