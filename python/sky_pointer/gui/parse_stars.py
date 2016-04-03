from sky_pointer.coords import EqCoords
from math import pi

lines = open('bright_stars.txt', 'r').readlines()

print "bright_stars = ["

for line in lines:
    name1, name2, ar, dec = line.split(',')[0:4]
    name1 = name1.strip()
    name2 = name2.strip()
    ra_h, ra_min = [int(f) for f in ar.strip().split()]
    dec = float(dec.strip())
    ra_rad = (ra_h + ra_min/60.)*pi/12
    dec_rad = dec*pi/180

    print "    ('%s', '%s', %.5f, %.5f)," % (name1, name2, ra_rad, dec_rad)

print "]"
