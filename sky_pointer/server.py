#!/usr/bin/env python

import time
import struct
import logging
from math import pi
import socket
import select
import coords


def decode_packet(data):
    """Decode Stellarium client-server protocol packet"""
    fields = struct.unpack('<HHQIi', data)
    return coords.EqCoords(fields[3]*pi/0x80000000, fields[4]*pi/0x80000000)


def encode_packet(coords):
    """Encode Stellarium client-server protocol packet"""
    ra = long(coords.ra/pi*0x80000000)
    dec = long(coords.dec/pi*0x80000000)
    return struct.pack('<HHQIii', 24, 0, time.time()*1e6, ra, dec, 0)


class Server(object):
    def __init__(self, host, port):
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5)
        self.listening_socket = sock

        # List of socket objects that are currently open
        self.sockets = [sock]
        self.pos = coords.EqCoords(0, 0)

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

                        logging.info("Target: %s" % target)
                    else:
                        self.sockets.remove(conn)
                        logging.debug("Client disconnected")

            for s in self.sockets[1:]:
                s.send(encode_packet(self.pos))
