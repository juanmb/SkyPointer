import time
import numpy as np
from math import sin, cos, atan2, asin, pi, modf
from coords import Coords, EqCoords

K = 1.002737908             # solar-to-sidereal time ratio
SEC2RAD = 2*pi/(24*60*60)   # seconds (time) to radians factor


def cosine(coords):
    """ Get the direction cosine of an object """
    return np.array([[cos(coords[1])*cos(coords[0])],
                     [cos(coords[1])*sin(coords[0])],
                     [sin(coords[1])]])

def orthonormal(u, v):
    """ Obtain a unit vector orthogonal to two given vectors """
    w = np.cross(u.T, v.T)
    w /= np.linalg.norm(w)
    return w.T


class PointingModel(object):
    """ Implementation of Toshimi Taki's "Equations for Pointing a Telescope":
    http://www.geocities.jp/toshimi_taki/aim/aim.htm
    """

    def __init__(self, t=0):
        self.t0 = t or time.time() # reference timestamp
        self.T = np.eye(3)  # transformation matrix (defaults to identity)

        # coords of reference stars (equatorial)
        self.eq_refs = [EqCoords(0, 0), EqCoords(pi/2,0)]
        # coords of reference stars (instrumental)
        self.inst_refs = [EqCoords(0,0), EqCoords(pi/2,0)]
        # timestamp of observation of reference stars
        self.t_refs = [0, 0]
        self.__ref_count = 0

    def __local_eq(self, eq, t):
        return EqCoords(eq[0] - K*SEC2RAD*(t - self.t0), eq[1])

    def __compute_matrix(self):
        # direction cosine of reference stars in instrumental coord. system
        if self.inst_refs[0] == self.inst_refs[1]:
            raise ValueError("Invalid reference stars. "
                             "Instrument coordinates must be different")
        if self.eq_refs[0] == self.eq_refs[1]:
            raise ValueError("Invalid reference stars. "
                             "Equatorial coordinates must be different")

        u1 = cosine(self.inst_refs[0])
        u2 = cosine(self.inst_refs[1])
        u3 = orthonormal(u1, u2)

        # direction cosine of reference stars in equatorial coord. system
        v1 = cosine(self.__local_eq(self.eq_refs[0], self.t_refs[0]))
        v2 = cosine(self.__local_eq(self.eq_refs[1], self.t_refs[1]))
        v3 = orthonormal(v1, v2)

        # generate matrices
        U = np.hstack((u1, np.hstack((u2, u3))))
        V = np.hstack((v1, np.hstack((v2, v3))))

        # calculate the transformation matrix T
        self.T = U.dot(np.linalg.inv(V))

    def _set_ref_n(self, n, eq, inst, t=0):
        self.t_refs[n] = t or time.time()
        self.eq_refs[n] = EqCoords(eq[0], eq[1])
        self.inst_refs[n] = Coords(inst[0], inst[1])

    def set_ref(self, eq, inst, t=0):
        self._set_ref_n(self.__ref_count % 2, eq, inst, t)
        # if there are two reference stars, compute the T matrix
        if self.__ref_count:
            self.__compute_matrix()
        self.__ref_count += 1

    def eq_to_inst(self, eq, t=0):
        t = t or time.time()
        # direction cosine in instrumental coordinate system
        v = self.T.dot(cosine(self.__local_eq(eq, t)))
        return Coords(atan2(v[1], v[0]), asin(v[2]))    # phi, theta


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
