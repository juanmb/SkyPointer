#!/usr/bin/env python

import logging
import struct
from threading import Timer
from pointer import Pointer


def sign(val):
    return 1 if val > 0 else -1


class Gamepad:
    def __init__(self, pointer, device='/dev/input/js0'):
        self.__pipe = open(device, 'r')
        self.ptr = pointer

    def loop(self):
        run_tmr = off_tmr = Timer(0, None)

        while True:
            t, value, _type, n = struct.unpack('IhBB', self.__pipe.read(8))

            if _type == 1:
                #logging.debug("Button %d %s" % (n, 'pressed' if value else 'released'))
                if n == 0:
                    off_tmr.cancel()
                    self.ptr.enable_laser(value)
                elif n == 1:
                    if value:
                        tgt = self.ptr.target
                        try:
                            mot = self.ptr.get_coords()
                        except ValueError as e:
                            logging.error(e)
                        else:
                            logging.info("Target: %f, %f\tMotors: %f, %f" %
                                         (tgt[0], tgt[1], mot[0], mot[1]))
                elif n in (4, 5):
                    if value:
                        index = n - 4
                        self.ptr.enable_laser(1)
                        off_tmr.cancel()
                        off_tmr = Timer(4, self.ptr.enable_laser, (0,))
                        off_tmr.start()
                        refs = self.ptr.get_refs()
                        if len(refs) > index:
                            tgt = refs[index]
                            logging.debug("Going to target %d: %s" %
                                          (index + 1, tgt))
                            try:
                                self.ptr.goto(tgt)
                            except ValueError as e:
                                logging.error(e)
                elif n == 8:
                    if value:
                        logging.debug("Setting reference star: %s" %
                                      self.ptr.target)
                        try:
                            self.ptr.set_ref()
                        except ValueError as e:
                            logging.error(e)

            elif _type == 2:
                #logging.debug("Joystick %d. Value: %d" % (n, value))
                if value:
                    if n in (4, 5):
                        off_tmr.cancel()
                        self.ptr.enable_laser(1)
                        run_tmr.cancel()
                        _dir = sign(-value)
                        if n == 4:
                            self.ptr.steps(_dir, 0)
                            run_tmr = Timer(.5, self.ptr.run, (_dir, 0))
                        else:
                            self.ptr.steps(0, _dir)
                            run_tmr = Timer(.5, self.ptr.run, (0, _dir))
                        run_tmr.start()
                else:
                    off_tmr.cancel()
                    off_tmr = Timer(4, self.ptr.enable_laser, (0,))
                    off_tmr.start()
                    run_tmr.cancel()
                    self.ptr.stop()
            else:
                pass
                #logging.debug("Key %d. Value: %d" % (n, value))


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    dev = '/dev/input/by-id/usb-Gasia_Co._Ltd_PS_R__Gamepad-joystick'

    ptr = Pointer()
    pad = Gamepad(ptr, dev)
    logging.info("Hardware:", ptr.hid)

    try:
        pad.loop()
    except KeyboardInterrupt:
        logging.info("Close")
