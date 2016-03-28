import time
import numpy as np
from math import sin, cos, atan2, asin, pi
from coords import Coords, EqCoords

K = 1.002737908             # solar-to-sidereal time ratio
SEC2RAD = 2*pi/(24*60*60)   # seconds (time) to radians factor


def eq_cosine(coords):
    """ Get the direction cosine of an object given its equatorial coords """
    return np.array([[cos(coords[1])*cos(coords[0])],
                     [cos(coords[1])*sin(coords[0])],
                     [sin(coords[1])]])

def cosine_to_coords(v):
    return atan2(v[1], v[0]), asin(v[2])


def orthonormal(u, v):
    """ Obtain a unit vector orthogonal to two given vectors """
    w = np.cross(u.T, v.T)
    w /= np.linalg.norm(w)
    return w.T


class PointingModel(object):
    """ Implementation of Toshimi Taki's "Equations for Pointing a Telescope":
    http://www.geocities.jp/toshimi_taki/aim/aim.htm
    """

    def __init__(self, t=0, z1=.0, z2=.0, z3=.0):
        self.z1, self.z2, self.z3 = z1, z2, z3  # mount errors
        self.t0 = t or time.time()  # reference timestamp
        self.T = np.eye(3)          # transformation matrix
        self.Tinv = np.eye(3)       # inverse of T

        # coords of reference stars (equatorial)
        self.eq_refs = [EqCoords(0, 0), EqCoords(pi/2, 0)]
        # coords of reference stars (instrumental)
        self.inst_refs = [EqCoords(0, 0), EqCoords(pi/2, 0)]
        # timestamp of observation of reference stars
        self.t_refs = [0, 0]
        self.__ref_count = 0
        self.__computed = False

    def app_to_real_cosine(self, coords):
        """ Calculate the real direction cosine of an object given the apparent
        instrumental coordinates """
        a, b = coords[0], coords[1] + self.z3
        z1, z2 = self.z1, self.z2
        return np.array([[cos(b)*cos(a) - z2*sin(a) + z1*sin(b)*sin(a)],
                         [cos(b)*sin(a) + z2*cos(a) - z1*sin(b)*cos(a)],
                         [sin(b)]])

    def app_to_real_coords(self, coords):
        """ Calculate the real instrumental coordinates of an object given
        the apparent ones """
        return Coords(*cosine_to_coords(self.app_to_real_cosine(coords)))

    def real_to_app_coords(self, coords):
        """ Calculate the apparent instrumental coordinates of an object given
        the real ones """
        a, b = coords
        z1, z2 = self.z1, self.z2
        v2 = np.array([[cos(b)*cos(a) + z2*sin(a) - z1*sin(b)*sin(a)],
                       [cos(b)*sin(a) - z2*cos(a) + z1*sin(b)*cos(a)],
                       [sin(b)]])
        c, d =  cosine_to_coords(v2)
        return Coords(c, d - self.z3)

    def __local_eq(self, eq, t):
        return EqCoords(eq[0] - K*SEC2RAD*(t - self.t0), eq[1])

    def __global_eq(self, eq, t):
        return EqCoords(eq[0] + K*SEC2RAD*(t - self.t0), eq[1])

    def __compute_matrix(self):
        # direction cosine of reference stars in instrumental coord. system
        if self.inst_refs[0] == self.inst_refs[1]:
            raise ValueError("Invalid reference stars: "
                             "Instrument coordinates must be different!")
        if self.eq_refs[0] == self.eq_refs[1]:
            raise ValueError("Invalid reference stars: "
                             "Equatorial coordinates must be different!")

        u1 = self.app_to_real_cosine(self.inst_refs[0])
        u2 = self.app_to_real_cosine(self.inst_refs[1])
        u3 = orthonormal(u1, u2)

        # direction cosine of reference stars in equatorial coord. system
        v1 = eq_cosine(self.__local_eq(self.eq_refs[0], self.t_refs[0]))
        v2 = eq_cosine(self.__local_eq(self.eq_refs[1], self.t_refs[1]))

        v3 = orthonormal(v1, v2)

        # calculate the transformation matrix T
        U = np.hstack((u1, u2, u3))
        V = np.hstack((v1, v2, v3))
        self.T = U.dot(np.linalg.inv(V))
        self.Tinv = np.linalg.inv(self.T)
        self.__computed = True

    def _set_ref_n(self, n, eq, inst, t=0):
        self.t_refs[n] = t or time.time()
        self.eq_refs[n] = EqCoords(eq[0], eq[1])
        self.inst_refs[n] = Coords(inst[0], inst[1])

    def set_ref(self, eq, inst, t=0):
        """ Add a new reference star """
        self._set_ref_n(self.__ref_count % 2, eq, inst, t)
        # if there are two reference stars, compute the T matrix
        if self.__ref_count:
            self.__compute_matrix()
        self.__ref_count += 1

    def get_nrefs(self):
        return self.__ref_count

    def eq_to_inst(self, eq, t=0):
        """ Convert equatorial to instrumental coordinates"""
        if not self.__computed:
            raise ValueError("Instrument coordinates not aligned!")

        v = self.T.dot(eq_cosine(self.__local_eq(eq, t or time.time())))
        # obtain phi and theta from direction cosine
        real = cosine_to_coords(v/np.linalg.norm(v))
        return self.real_to_app_coords(real)

    def inst_to_eq(self, inst, t=0):
        """ Convert instrumental to equatorial coordinates"""
        #if not self.__computed:
            #raise ValueError("Instrument coordinates not aligned!")

        v = self.Tinv.dot(self.app_to_real_cosine(inst))
        # obtain AR and dec from direction cosine
        eq = cosine_to_coords(v/np.linalg.norm(v))
        return self.__global_eq(eq, t or time.time())


if __name__ == '__main__':
    # usage example
    pm = PointingModel(t=75600)
    pm.set_ref([0.034470, 0.506809], [1.732239, 1.463808], t=77276)
    pm.set_ref([0.618501, 1.557218], [5.427625, 0.611563], t=77780.75)

    # target star
    tgt = EqCoords(0.188132, -0.314822)
    itgt = pm.eq_to_inst(tgt, t=78732)

    print "Target star"
    print "Equatorial:  ", tgt
    print "Instrumental:", itgt
    print "Eq from inst:", pm.inst_to_eq(itgt, t=78732)
    print

    pm = PointingModel(t=75600, z1=0.001, z2=0.002, z3=0.003)
    pm.set_ref([0.034470, 0.506809], [1.732239, 1.463808], t=77276)
    pm.set_ref([0.618501, 1.557218], [5.427625, 0.611563], t=77780.75)

    # target star
    tgt = Coords(0.188132, -0.314822)
    real = pm.app_to_real_coords(tgt)

    print "Real:", real
    print "App1:", tgt
    print "App2:", pm.real_to_app_coords(real)
    print
