#!/usr/bin/env python

import logging
import argparse
from server import Server


def main():
    parser = argparse.ArgumentParser(description='Sky-pointing laser controller')
    parser.add_argument('--port', '-p', type=int, default=10001,
                        help='Listenging TCP port (default: 10001)')
    parser.add_argument('--iface', '-i', default='0.0.0.0',
                        help='Listenging network interface (default: 0.0.0.0)')
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    server = Server(args.iface, args.port)
    logging.info("Server listening on port %d" % args.port)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Closing")


if __name__ == "__main__":
    main()
