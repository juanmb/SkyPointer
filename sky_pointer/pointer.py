from math import pi
from pointing_model import PointingModel
from hardware import Hardware, STEPS
from coords import Coords


class Pointer:
    def __init__(self, device='/dev/ttyUSB0', baud=115200):
        self.__pm = PointingModel()
        self.__hw = Hardware(device, baud)
        self.target = Coords(0, 0)
        self.hid = self.get_id()

    def get_id(self):
        return self.__hw.get_id()

    def set_ref(self):
        self.target = self.get_coords()
        self.__pm.set_ref(self.target, self.get_coords())

    def get_refs(self):
        return self.__pm.inst_refs

    def steps(self, az, alt):
        self.__hw.move(az, alt)

    def run(self, az_dir, alt_dir):
        if not -1 <= az_dir <= 1:
            raise ValueError("az_dir must be between -1 and 1")
        if not -1 <= alt_dir <= 1:
            raise ValueError("alt_dir must be between -1 and 1")
        half = STEPS/2 - 1
        self.__hw.move(az_dir*half, alt_dir*half)

    def stop(self):
        self.__hw.stop()

    def enable_laser(self, enable):
        self.__hw.enable_laser(enable)

    def get_coords(self):
        az, alt = self.__hw.get_pos()
        return Coords(2*pi*az/STEPS, 2*pi*alt/STEPS)

    def goto(self, eq):
        self.target = eq
        inst = self.__pm.eq_to_inst(eq)
        self.__hw.goto(inst[0]*STEPS/2/pi, inst[1]*STEPS/2/pi)
