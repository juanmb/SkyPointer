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
    ra = long((coords[0] % (2*pi))/pi*0x80000000)
    dec = long(coords[1]/pi*0x80000000)
    return struct.pack('<HHQIii', 24, 0, time.time()*1e6, ra, dec, 0)


class Server(object):
    def __init__(self, pointer, host='0.0.0.0', port='10001'):
        self.ptr = pointer
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5)
        self.listening_socket = sock

        # List of socket objects that are currently open
        self.sockets = [sock]

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
                        tgt = coords.EqCoords(*decode_packet(data))
                        try:
                            self.ptr.goto(tgt)
                        except ValueError as e:
                            logging.debug(e)

                        logging.info("New target: %s" % tgt)
                    else:
                        self.sockets.remove(conn)
                        logging.debug("Client disconnected")

            for s in self.sockets[1:]:
                try:
                    s.send(encode_packet(self.ptr.get_coords()))
                except IOError as e:
                    logging.error(e)
