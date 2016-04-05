#!/usr/bin/env python

import time
import struct
import logging
import threading
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


class StellariumServer(object):
    """A TCP server that implements the Stellarium client-server protocol
    goto: callback function that will be called every time a new 'goto' command
    is received
    """
    def __init__(self, host='0.0.0.0', port=10000, goto=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5)
        self.listening_socket = sock
        self.goto = goto
        self.pos = (0, 0)

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
                    logging.debug("New client [%s, %d]" % addr)
                else:
                    try:
                        data = conn.recv(1024)
                    except socket.error:
                        continue
                    if data:
                        try:
                            tgt = coords.EqCoords(*decode_packet(data))
                        except struct.error as e:
                            logging.error(e)
                            continue

                        logging.info("New target: %s" % tgt)
                        if callable(self.goto):
                            try:
                                self.goto(tgt)
                            except ValueError as e:
                                logging.debug(e)
                    else:
                        self.sockets.remove(conn)
                        logging.debug("Client disconnected")

            """Send the current position to all connected clients"""
            for s in self.sockets[1:]:
                try:
                    s.send(encode_packet(self.pos))
                except IOError as e:
                    logging.error(e)

    def set_pos(self, pos):
        """Set the current position"""
        self.pos = pos


class StellariumServerThread(threading.Thread):
    def __init__(self, host='0.0.0.0', port=10000, goto=None):
        threading.Thread.__init__(self)
        self.daemon = True
        self.server = StellariumServer(host, port, goto)

    def run(self):
        self.server.serve_forever()

    def stop(self):
        pass

    def set_pos(self, pos):
        self.server.set_pos(pos)


if __name__ == '__main__':
    from time import sleep

    def goto(pos):
        print "Going to", pos

    server = StellariumServerThread(host='127.0.0.1', goto=goto)
    server.start()

    for i in range(10):
        server.set_pos((i/100., i/100.))
        sleep(1)
