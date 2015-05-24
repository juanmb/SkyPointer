from math import pi, copysign


class Coords(object):
    def __init__(self, x, y):
        """x, y must be radians"""
        self.x, self.y = x, y

    def __getitem__(self, key):
        if key == 0 :
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid index: %s" % key)

    def __str__(self):
        return 'X: %3.4f deg\tY: %3.4f deg' % (180/pi*self.x, 180/pi*self.y)


class EqCoords(Coords):
    def __str__(self):
        ra_m, ra_s = divmod(abs(self.x*60*60*12/pi), 60)
        ra_h, ra_m = divmod(ra_m, 60)
        ra_h = ra_h % 24

        dec_m, dec_s = divmod(abs(self.y*60*60*180/pi), 60)
        dec_d, dec_m = divmod(dec_m, 60)
        dec_d = copysign(dec_d, self.y)

        return 'RA: %02dh %02dm %.2fs\t' % (ra_h, ra_m, ra_s) + \
               'dec: %02dd %02d\' %.1f"' % (dec_d, dec_m, dec_s)


if __name__ == '__main__':
    eq1 = EqCoords(2*pi+0.034, -pi/2+0.01)
    print eq1
    print eq1[0], eq1[1]
    print

    c1 = Coords(2*pi+0.034, -pi/2+0.01)
    print c1
    print c1[0], c1[1]
