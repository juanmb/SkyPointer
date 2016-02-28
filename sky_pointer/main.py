#!/usr/bin/env python

import logging
import argparse
import threading
from server import Server
from pointer import Pointer
from gamepad import Gamepad
from rcfile import rcfile

SERIAL_PORT = '/dev/ttyUSB0'
JOYSTICK_DEV = '/dev/js0'


def main():
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    # read options from rc file
    cfg = rcfile('sky-pointer')
    port = int(cfg.get('port', 10001))
    iface = cfg.get('iface', '0.0.0.0')
    serial = cfg.get('serial', SERIAL_PORT)
    joystick = cfg.get('joystick', JOYSTICK_DEV)

    # override some options with command line arguments
    parser = argparse.ArgumentParser(
        description='Sky-pointing laser controller')
    parser.add_argument('--port', '-p', type=int, default=port,
                        help='Listenging TCP port (default: %d)' % port)
    parser.add_argument('--iface', '-i', default=iface,
                        help='Listenging network interface (default: %s)' % iface)
    parser.add_argument('--serial', '-s', default=serial,
                        help='Serial port (default: %s)' % serial)
    parser.add_argument('--joystick', '-j', default=joystick,
                        help='Joystick device (default: %s)' % joystick)
    args = parser.parse_args()

    ptr = Pointer(args.serial)
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
