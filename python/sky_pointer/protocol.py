#!/usr/bin/env python

import time
import serial
import struct
import threading

STEPS = 3200    # Number of microsteps per revolution of the motors
NRETRIES = 3    # Number of retries when sending a serial command


class Protocol:
    """Serial communication with SkyPointer board."""

    def __init__(self, device='/dev/ttyUSB0', baud=115200):
        self.__lock = threading.Lock()
        self.__ser = serial.Serial(device, baud, timeout=1)
        self.__ser.flushInput()
        time.sleep(1.7)     # wait until Arduino bootloader exits

    def __send_command(self, cmd, ret_len=3, ret_ok='OK'):
        """Send a serial command and check the response."""
        with self.__lock:
            for i in range(NRETRIES):
                self.__ser.write(cmd + '\r')
                ret = self.__ser.read(ret_len)

                if ret.startswith(ret_ok):
                    return ret
                print "Command failed (%s). retrying" % cmd
                self.__ser.flushInput()

        raise IOError('Serial command "%s" returned "%s"' % (cmd, ret.strip()))

    def get_id(self):
        return self.__send_command('I', ret_len=15, ret_ok='SkyPointer')

    def enable_laser(self, enable):
        self.__send_command('L %d' % int(enable))

    def goto(self, ha, el):
        self.__send_command('G %d %d' % (ha, el))

    def move(self, ha, el):
        self.__send_command('M %d %d' % (ha, el))

    def home(self):
        self.__send_command('H')

    def stop(self):
        self.__send_command('S')

    def quit(self):
        self.__send_command('Q')

    def get_pos(self):
        ret = self.__send_command('P', ret_len=12, ret_ok='P ')
        ha, el = ret.strip().split()[1:3]
        return int(ha), int(el)

    def get_calib(self, n):
        ret = self.__send_command('R %d' % n, ret_len=11, ret_ok='R ')
        v = int(ret.strip().split()[1], 16)
        cal = struct.unpack('!f', struct.pack('!I', v))[0]
        return cal if abs(cal) < 1. else 0.0

    def set_calib(self, n, val):
        v = struct.unpack('!I', struct.pack('!f', val))[0]
        self.__send_command('W %d %x' % (n, v))

    def close(self):
        self.quit()
        self.__ser.close()
