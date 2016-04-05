from math import pi, copysign, modf, floor


class Coords(object):
    def __init__(self, x, y):
        """x, y must be radians"""
        self.x, self.y = x, y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid index: %s" % key)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __str__(self):
        return 'X: %3.4f deg\tY: %3.4f deg' % (180/pi*self.x, 180/pi*self.y)


class EqCoords(Coords):
    def fields(self):
        hfrac, ra_h = modf(abs(self.x*12/pi))
        mfrac, ra_m = modf(hfrac*60.)
        ra_s = floor(mfrac*60)

        dfrac, dec_d = modf(abs(self.y*180/pi))
        mfrac, dec_m = modf(dfrac*60.)
        dec_s = floor(mfrac*60)

        return ra_h % 24, ra_m, ra_s, copysign(dec_d, self.y), dec_m, dec_s

    def __str__(self):
        return 'RA: %02d:%02d:%02.0f\tdec: %02d:%02d:%02.0f' % self.fields()

    @staticmethod
    def from_fields(ra_h, ra_m, ra_s, dec_d, dec_m, dec_s):
        ra = copysign(abs(ra_h) + ra_m/60. + ra_s/3600., ra_h)
        dec = copysign(abs(dec_d) + dec_m/60. + dec_s/3600., dec_d)
        return EqCoords(ra*pi/12, dec*pi/180)


if __name__ == '__main__':
    eq1 = EqCoords(-pi - pi/12./60, pi/2 + pi/180./60*2)
    print eq1
    print eq1[0], eq1[1]
    print

    c1 = Coords(2*pi+0.034, -pi/2+0.01)
    print c1
    print c1[0], c1[1]

    print Coords(1, 2) == Coords(1, 2)

    print EqCoords(pi/12, -1*pi/180)
