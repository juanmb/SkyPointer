import sys
import argparse
from math import sqrt, pi, cos
from scipy.optimize import fmin
from sky_pointer.pointing_model import PointingModel

# List of observed stars for calibration.
# Colums: time(hours), RA, dec, horiz. angle, elevation
# The two first rows are the reference stars
TEST_STARS = [
    (1446993838.0, 0.034470, 0.506809, 1.732178, 1.489255),
    (1446994384.0, 0.618501, 1.557218, 5.427621, 0.636993),
    (1446993307.0, 5.415320, 0.789709, 0.169081, 0.873450),
    (1446993102.0, 4.872159, 0.676751, 0.182230, 0.469371),
    (1446995696.0, 5.688537, 0.171601, 1.037047, 0.730508),
    (1446993422.0, 5.700754,-0.282220, 1.574360, 0.520544),
    (1446994289.0, 6.008878,-0.517892, 1.916293, 0.414673),
    (1446995294.0, 0.188132,-0.314822, 2.276999, 0.682878),
    (1446996864.0, 0.793179, 0.070738, 3.094256, 0.905198),
    (1446995417.0, 0.552542, 0.408721, 3.374184, 1.242221),
    (1446994972.0, 1.201514, 0.287805, 3.806290, 0.635230),
    (1446994859.0, 1.378737, 0.802642, 4.475106, 0.681115),
    (1446995200.0, 0.888518, 0.869663, 4.565295, 1.023426),
    (1446995558.0, 0.037815, 1.031437, 5.647428, 1.146943),
]


def calc_errors(params, stars):
    z1, z2, z3 = params
    t0 = stars[0][0]
    pm = PointingModel(t0, z1, z2, z3)

    for i, s in enumerate(stars[:2]):
        pm.set_ref(s[1:3], s[3:5], t=s[0])

    phi_err = []
    theta_err = []
    for s in stars:
        phi1, theta1 = s[3], s[4]
        phi1 = phi1 if abs(phi1) <= pi else phi1-2*pi

        phi2, theta2 = pm.eq_to_inst(s[1:3], t=s[0])

        phi_err.append((phi2-phi1)*cos(theta2)*180/pi)
        theta_err.append((theta2-theta1)*180/pi)

    return phi_err, theta_err


def func(params, stars):
    phi_err, theta_err = calc_errors(params, stars)
    # return chi-square
    return sum(sqrt(pe**2 + te**2) for pe, te in zip(phi_err, theta_err))

def read_file(filename):
    lines = open(filename, 'r').readlines()
    observations = []
    for line in lines:
        if not line.startswith('#'):
            observations.append([float(w) for w in line.split()])
    return observations


def main():
    parser = argparse.ArgumentParser(description=
            'Calculate mechanical errors from a collection of observations')
    parser.add_argument('file')
    args = parser.parse_args()

    #Initial guess.
    z = (.0, .0, .0)

    observations = read_file(args.file)
    if not observations:
        print "Invalid or empty observations file!"
        return

    # Apply downhill Simplex algorithm.
    z = fmin(func, z, args=(observations,), full_output=0, xtol=2e-6)
    print
    print "Mount errors (rad):", z
    print "Mount errors (deg):", z*180/pi

    try:
        import pylab
    except ImportError:
        pass
    else:
        pe, te = calc_errors(z, observations)
        pylab.plot(pe, te, 'ro')
        pylab.xlim([-.5, .5])
        pylab.ylim([-.5, .5])
        pylab.grid(True)
        pylab.xlabel("Phi error")
        pylab.ylabel("Theta error")
        pylab.show()


if __name__ == '__main__':
    main()
