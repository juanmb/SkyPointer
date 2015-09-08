#!/usr/bin/env python

import struct
from threading import Timer
from pointer import Pointer


def sign(val):
    return 1 if val > 0 else -1


class Gamepad:
    def __init__(self, pointer, device='/dev/input/js0'):
        self.__pipe = open(device, 'r')
        self.pt = pointer

    def loop(self):
        run_tmr = off_tmr = Timer(0, None)

        while True:
            t, value, _type, n = struct.unpack('IhBB', self.__pipe.read(8))

            if _type == 1:
                print "Button %d %s" % (n, 'pressed' if value else 'released')
                if n == 0:
                    off_tmr.cancel()
                    self.pt.enable_laser(value)
                elif n == 1:
                    if value:
                        print self.pt.get_coords()
                elif n == 4:
                    if value:
                        print "goto target1"
                        off_tmr.cancel()
                        off_tmr = Timer(4, self.pt.enable_laser, (0,))
                        off_tmr.start()
                        refs = self.pt.get_refs()
                        if len(refs) > 0:
                            self.pt.goto(refs[0])
                elif n == 5:
                    if value:
                        off_tmr.cancel()
                        off_tmr = Timer(4, self.pt.enable_laser, (0,))
                        off_tmr.start()
                        print "goto target2"
                        refs = self.pt.get_refs()
                        if len(refs) > 1:
                            self.pt.goto(refs[1])
                elif n == 8:
                    if value:
                        print "set ref"
                        self.pt.set_ref()

            elif _type == 2:
                print "Joystick %d. Value: %d" % (n, value)
                if value:
                    if n in (4, 5):
                        off_tmr.cancel()
                        self.pt.enable_laser(value)
                        run_tmr.cancel()
                        if n == 4:
                            self.pt.steps(sign(value), 0)
                            run_tmr = Timer(.5, self.pt.run, (sign(value), 0))
                        else:
                            self.pt.steps(0, sign(value))
                            run_tmr = Timer(.5, self.pt.run, (0, sign(value)))
                        run_tmr.start()
                else:
                    off_tmr.cancel()
                    off_tmr = Timer(4, self.pt.enable_laser, (0,))
                    off_tmr.start()
                    run_tmr.cancel()
                    self.pt.stop()
            else:
                pass
                #print "Key %d. Value: %d" % (n, value)


if __name__ == '__main__':
    dev = '/dev/input/by-id/usb-Gasia_Co._Ltd_PS_R__Gamepad-joystick'

    ptr = Pointer()
    pad = Gamepad(ptr, dev)
    try:
        pad.loop()
    except KeyboardInterrupt:
        print "Close"
