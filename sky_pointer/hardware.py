#!/usr/bin/env python

import serial
import threading
from coords import Coords

STEPS = 3200


class Hardware:
    def __init__(self, device='/dev/ttyUSB0', baud=115200):
        self.__lock = threading.Lock()
        self.__ser = serial.Serial(device, baud)

    def __send_command(self, cmd, ret_len=3, ret_ok='OK'):
        self.__lock.acquire()
        try:
            self.__ser.flushInput()
            self.__ser.write(cmd+'\r')
            ret = self.__ser.read(ret_len)
        finally:
            self.__lock.release()

        if not ret.startswith(ret_ok):
            raise IOError('Serial command "%s" returned "%s"' % (cmd, ret))

        return ret

    def enable_laser(self, enable):
        self.__send_command('L %d' % int(enable))

    def goto(self, az, alt):
        self.__send_command('G %d %d' % (az, alt))

    def move(self, az, alt):
        self.__send_command('M %d %d' % (az, alt))

    def stop(self):
        self.__send_command('S')

    def get_pos(self):
        ret = self.__send_command('P', ret_len=12, ret_ok='P ')
        az, alt = ret.strip().split()[1:3]
        return int(az), int(alt)
