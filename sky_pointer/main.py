#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import struct
import logging
from math import pi
import socket
import select
import ephem
import argparse


def decode_packet(data):
    """Decode Stellarium client-server protocol packet"""
    fields = struct.unpack('<HHQIi', data)
    return ephem.Equatorial(fields[3]*pi/0x80000000, fields[4]*pi/0x80000000)


def encode_packet(coords):
    """Encode Stellarium client-server protocol packet"""
    fields = struct.unpack('<HHQIi', data)
    ra = long(coords.ra/pi*0x80000000)
    dec = long(coords.dec/pi*0x80000000)
    return struct.pack('<HHQIii', 24, 0, time.time()*1e6, ra, dec, 0)


class TelescopeServer(object):
    def __init__(self, host, port, observer):
        self.observer = observer

        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5)
        self.listening_socket = sock

        # List of socket objects that are currently open
        self.sockets = [sock]
        self.pos = ephem.Equatorial(0, pi/2)

    def __compute_local(self, coords):
        body = ephem.FixedBody()
        body._ra = coords.ra
        body._dec = coords.dec
        self.observer.date = ephem.now()
        body.compute(self.observer)
        return body

    def __hour_angle(self, coords):
        self.observer.date = ephem.now()
        return ephem.hours(self.observer.sidereal_time() - coords.ra)

    def serve_forever(self):
        while True:
            # Waits for I/O being available for reading from any socket object.
            rlist, _, _ = select.select(self.sockets, [], [], 0.5)
            for conn in rlist:
                if conn is self.listening_socket:
                    new_socket, addr = self.listening_socket.accept()
                    self.sockets.append(new_socket)
                    logging.debug("Connected client [%s, %d]" % addr)
                else:
                    try:
                        data = conn.recv(1024)
                    except socket.error:
                        continue
                    if data:
                        target = decode_packet(data)
                        self.pos = target

                        #body = self.__compute_local(target)
                        logging.info(
                            "Target: RA %s  dec %s  " % (target.ra, target.dec) +
                            "HA %s" % self.__hour_angle(target)
                            #"Az %s  Alt %s  " % (body.az, body.alt)
                        )
                    else:
                        self.sockets.remove(conn)
                        logging.debug("Client disconnected")

            for s in self.sockets[1:]:
                s.send(encode_packet(self.pos))


def main():
    parser = argparse.ArgumentParser(description='Sky-pointing laser controller')
    parser.add_argument('--port', '-p', type=int, default=10001,
                        help='Listenging TCP port (default: 10001)')
    parser.add_argument('--iface', '-i', default='0.0.0.0',
                        help='Listenging network interface (default: 0.0.0.0)')
    parser.add_argument('--lat', '-l', default='43:31:48.0', help="Observer's latitude")
    parser.add_argument('--long', '-L', default='-5:40:12.0', help="Observer's longitude")
    args = parser.parse_args()

    obs = ephem.Observer()
    #obs.epoch = ephem.now()
    obs.lat = args.lat
    obs.long = args.long

    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    logging.info("Latitude:  %s" % obs.lat)
    logging.info("Longitude: %s" % obs.long)
    #logging.info("Elevation: %s" % obs.elev)
    logging.info("Epoch:     %s" % obs.epoch)
    logging.info("---")

    server = TelescopeServer(args.iface, args.port, obs)
    logging.info("Server listening on port %d" % PORT)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Closing")


if __name__ == "__main__":
    main()
