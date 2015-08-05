#!/usr/bin/env python
import struct
import time
import serial
import threading

STEPS = 3200
HALF = STEPS/2 -1

DEVICE = '/dev/input/by-id/usb-Gasia_Co._Ltd_PS_R__Gamepad-joystick'
#DEVICE = '/dev/input/event3'

def trim(a):
    if not a:
        return 0
    return 1 if a > 0 else -1


class Pointer:
    def __init__(self):
        self.__run = False
        self.ser = serial.Serial('/dev/ttyUSB0', 115200)

    def goto(self, az, alt):
        self.ser.write('G %d %d\r' % (az, alt))

    def move(self, az, alt):
        print 'M %d %d\r' % (az, alt)
        self.ser.write('M %d %d\r' % (az, alt))

    def move2(self, az, alt):
        def move_fast(x, y):
            time.sleep(0.5)
            if self.__run:
                print 'move_fast'
                self.move(x, y)

        self.move(trim(az), trim(alt)) # move one step
        threading.Thread(target=move_fast, args=(az, alt)).start()
        self.__run = True

    def enable_laser(self, enable):
        self.ser.write('L %d\r' % int(enable))

    def get_pos(self):
        self.ser.flushInput()
        self.ser.write('P\r')
        return self.ser.read(12)

    def stop(self):
        self.__run = False
        self.ser.write('S\r')


pipe = open(DEVICE, 'r')
pt = Pointer()

while True:
    t, value, _type, number = struct.unpack('IhBB', pipe.read(8))

    if _type == 1:
        print "Button %d %s" % (number, 'pressed' if value else 'released')
        if number == 0:
            pt.enable_laser(value)
        elif number == 2:
            print pt.get_pos()
        elif number == 3:
            pt.stop()

    elif _type == 2:
        print "Joystick %d. Value: %d" % (number, value)
        if value:
            if number == 4:
                #pt.run_az(value > 0)
                steps = HALF if value > 0 else -HALF
                pt.move2(steps, 0)
            elif number == 5:
                steps = HALF if value > 0 else -HALF
                pt.move2(0, steps)
        else:
            pt.stop()

    else:
        print "Key %d. Value: %d" % (number, value)

ser.close()
