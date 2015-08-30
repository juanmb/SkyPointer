#!/usr/bin/env python
import struct
import time
import serial
import threading
import logging
from Queue import Queue

STEPS = 3200
HALF = STEPS/2 -1

LASER_ON = 1
LASER_OFF = 2
MOVE_UP = 3
MOVE_DOWN = 4
MOVE_LEFT = 5
MOVE_RIGHT = 6
STEP_UP = 7
STEP_DOWN = 8
STEP_LEFT = 9
STEP_RIGHT = 10
STOP = 11


DEVICE = '/dev/input/by-id/usb-Gasia_Co._Ltd_PS_R__Gamepad-joystick'
#DEVICE = '/dev/input/event3'

logging.basicConfig(level=logging.DEBUG)


def trim(a):
    if not a:
        return 0
    return 1 if a > 0 else -1


class Pointer:
    def __init__(self):
        self.__run = False
        self.ser = serial.Serial('/dev/ttyUSB0', 115200)

    def goto(self, az, alt):
        logging.debug('G %d %d' % (az, alt))
        self.ser.write('G %d %d\r' % (az, alt))

    def move(self, az, alt):
        logging.debug('M %d %d' % (az, alt))
        self.ser.write('M %d %d\r' % (az, alt))

    def move2(self, az, alt):
        def move_fast(x, y):
            time.sleep(0.5)
            if self.__run:
                self.move(x, y)

        self.move(trim(az), trim(alt)) # move one step
        threading.Thread(target=move_fast, args=(az, alt)).start()
        self.__run = True

    def enable_laser(self, enable):
        self.ser.write('L %d\r' % int(enable))

    def get_pos(self):
        self.ser.flushInput()
        logging.debug('P')
        self.ser.write('P\r')
        return self.ser.read(12)

    def stop(self):
        self.__run = False
        logging.debug('S')
        self.ser.write('S\r')


pipe = open(DEVICE, 'r')
queue = Queue()
pt = Pointer()

def worker():
    while True:
        item = queue.get()
        if item == LASER_ON:
            pt.enable_laser(True)
        elif item == LASER_OFF:
            pt.enable_laser(False)
        elif item == STEP_UP:
            pt.move(0, 1)
        elif item == STEP_DOWN:
            pt.move(0, -1)
        elif item == STEP_RIGHT:
            pt.move(-1, 0)
        elif item == STEP_LEFT:
            pt.move(1, 0)
        elif item == MOVE_UP:
            pt.move(0, HALF)
        elif item == MOVE_DOWN:
            pt.move(0, -HALF)
        elif item == MOVE_RIGHT:
            pt.move(-HALF, 0)
        elif item == MOVE_LEFT:
            pt.move(HALF, 0)
        elif item == STOP:
            pt.stop()
        queue.task_done()

worker_thread = threading.Thread(target=worker)
worker_thread.daemon = True
worker_thread.start()

stop_t = time.time()

def send_after(delay, cmd):
    def thread():
        time.sleep(delay)
        queue.put(cmd)
    threading.Thread(target=thread).start()

def move_after(delay, cmd):
    def thread():
        time.sleep(delay)
        if time.time() - stop_t > delay:
            queue.put(cmd)
    threading.Thread(target=thread).start()


while True:
    t, value, _type, number = struct.unpack('IhBB', pipe.read(8))

    if _type == 1:
        #logging.debug("Button %d %s" % (number, 'pressed' if value else 'released'))
        if number == 0:
            queue.put(LASER_ON if value else LASER_OFF)

    elif _type == 2:
        #logging.debug("Joystick %d. Value: %d" % (number, value))
        if value:
            if number == 4:
                queue.put(LASER_ON)
                queue.put(STEP_LEFT if value > 0 else STEP_RIGHT)
                move_after(0.5, MOVE_LEFT if value > 0 else MOVE_RIGHT)
                send_after(4, LASER_OFF)
            elif number == 5:
                queue.put(LASER_ON)
                queue.put(STEP_UP if value > 0 else STEP_DOWN)
                move_after(0.5, MOVE_UP if value > 0 else MOVE_DOWN)
                send_after(4, LASER_OFF)
        else:
            queue.put(STOP)
            stop_t = time.time()
    else:
        pass
        #logging.debug("Key %d. Value: %d" % (number, value))

ser.close()
