#!/usr/bin/env python

import logging
import argparse
import threading
from server import Server
from pointer import Pointer
from gamepad import Gamepad

JOYSTICK_DEV = '/dev/input/by-id/usb-Gasia_Co._Ltd_PS_R__Gamepad-joystick'


def main():
    parser = argparse.ArgumentParser(
        description='Sky-pointing laser controller')
    parser.add_argument('--port', '-p', type=int, default=10001,
                        help='Listenging TCP port (default: 10001)')
    parser.add_argument('--iface', '-i', default='0.0.0.0',
                        help='Listenging network interface (default: 0.0.0.0)')
    parser.add_argument('--joystick', '-j', default=JOYSTICK_DEV,
                        help='Joystick device (default: %s)' % JOYSTICK_DEV)
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    ptr = Pointer()
    pad = Gamepad(ptr, args.joystick)

    server = Server(ptr, args.iface, args.port)
    logging.info("Server listening on port %d" % args.port)

    pad_thread = threading.Thread(target=pad.loop)
    pad_thread.daemon = True
    pad_thread.start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Closing")


if __name__ == "__main__":
    main()
