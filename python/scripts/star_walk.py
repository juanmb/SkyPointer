import socket
import time
from pandas import read_csv
from sky_pointer.server import encode_goto_packet

HOST = 'localhost'
PORT = 10000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

stars = read_csv('ursa_maior.txt', sep=' ', header=None, names=['t', 'ra', 'dec', 'axis1', 'axis2'])

while True:
    for i in range(6):
        for _, star in stars.iterrows():
            data = encode_goto_packet([star.ra, star.dec])
            print star.ra, star.dec
            s.send(data)
            time.sleep(2)
    time.sleep(20)
