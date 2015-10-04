from math import pi
from pointing_model import PointingModel
from hardware import Hardware, STEPS
from coords import Coords, EqCoords


def _steps2rad(steps):
    p = 2.*(steps % STEPS)/STEPS
    return pi*(p if p <= 1 else p-2)

def _rad2steps(angle):
    a = (angle/2.) % pi
    return STEPS*(a if a <= pi else pi-a)/pi

def steps2rad(a, b):
    return _steps2rad(a), _steps2rad(b)

def rad2steps(a, b):
    return _rad2steps(a), _rad2steps(b)


class Pointer:
    def __init__(self, device='/dev/ttyUSB0', baud=115200):
        self.__pm = PointingModel()
        self.__hw = Hardware(device, baud)
        self.target = EqCoords(0, 0)
        self.hid = self.get_id()

    def get_id(self):
        return self.__hw.get_id()

    def set_ref(self):
        self.__pm.set_ref(self.target, self.get_coords())

    def get_refs(self):
        return self.__pm.inst_refs

    def steps(self, ha, el):
        self.__hw.move(ha, el)

    def run(self, ha_dir, el_dir):
        if not -1 <= ha_dir <= 1:
            raise ValueError("ha_dir must be between -1 and 1")
        if not -1 <= el_dir <= 1:
            raise ValueError("el_dir must be between -1 and 1")
        half = STEPS/2 - 1
        self.__hw.move(ha_dir*half, el_dir*half)

    def stop(self):
        self.__hw.stop()

    def enable_laser(self, enable):
        self.__hw.enable_laser(enable)

    def get_coords(self):
        return __pm.inst_to_eq(steps2rad(self.__hw.get_pos()))

    def goto(self, eq):
        self.target = eq
        self.__hw.goto(*rad2step(self.__pm.eq_to_inst(eq)))
