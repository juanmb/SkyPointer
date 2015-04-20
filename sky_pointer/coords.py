import math


class Coords(object):
    def __init__(self, ra, dec):
        """ra, dec must be radians"""
        self.ra, self.dec = ra, dec

    def __str__(self):
        ra_m, ra_s = divmod(abs(self.ra*60*60*12/math.pi), 60)
        ra_h, ra_m = divmod(ra_m, 60)
        ra_h = ra_h % 24

        dec_m, dec_s = divmod(abs(self.dec*60*60*180/math.pi), 60)
        dec_d, dec_m = divmod(dec_m, 60)
        dec_d = math.copysign(dec_d, self.dec)

        return 'RA: %02dh %02dm %.2fs\t' % (ra_h, ra_m, ra_s) + \
               'dec: %02dd %02d\' %.1f"' % (dec_d, dec_m, dec_s)


if __name__ == '__main__':
    print Coords(math.pi, math.pi/2)
    print Coords(2*math.pi+0.034, -math.pi/2+0.01)
