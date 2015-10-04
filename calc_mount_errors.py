from scipy.optimize import fmin
import pylab
from sky_pointer.pointing_model import PointingModel
from math import sqrt, pi, cos

# List of observed stars for calibration.
# Colums: time(hours), RA, dec, horiz. angle, elevation
# The two first rows are the reference stars
TEST_STARS = [
    (21.465556, 0.034470, 0.506809, 1.732178, 1.489255),
    (21.617222, 0.618501, 1.557218, 5.427621, 0.636993),
    (21.318056, 5.415320, 0.789709, 0.169081, 0.873450),
    (21.261111, 4.872159, 0.676751, 0.182230, 0.469371),
    (21.981667, 5.688537, 0.171601, 1.037047, 0.730508),
    (21.350000, 5.700754,-0.282220, 1.574360, 0.520544),
    (21.590833, 6.008878,-0.517892, 1.916293, 0.414673),
    (21.870000, 0.188132,-0.314822, 2.276999, 0.682878),
    (22.306111, 0.793179, 0.070738, 3.094256, 0.905198),
    (21.904167, 0.552542, 0.408721, 3.374184, 1.242221),
    (21.780556, 1.201514, 0.287805, 3.806290, 0.635230),
    (21.749167, 1.378737, 0.802642, 4.475106, 0.681115),
    (21.843889, 0.888518, 0.869663, 4.565295, 1.023426),
    (21.943333, 0.037815, 1.031437, 5.647428, 1.146943),
]


def calc_errors(params, stars):
    z1, z2, z3 = params
    t0 = stars[0][0]*3600
    pm = PointingModel(t0, z1, z2, z3)

    for i, s in enumerate(stars[:2]):
        pm.set_ref(s[1:3], s[3:5], t=s[0]*3600)

    phi_err = []
    theta_err = []
    for s in stars:
        phi1, theta1 = s[3], s[4]
        phi1 = phi1 if abs(phi1) <= pi else phi1-2*pi

        phi2, theta2 = pm.eq_to_inst(s[1:3], t=s[0]*3600)

        phi_err.append((phi2-phi1)*cos(theta2)*180/pi)
        theta_err.append((theta2-theta1)*180/pi)

    return phi_err, theta_err


def func(params, stars):
    phi_err, theta_err = calc_errors(params, stars)
    # return chi-square
    return sum(sqrt(pe**2 + te**2) for pe, te in zip(phi_err, theta_err))


#Initial guess.
z = (.0, .0, .0)

# Apply downhill Simplex algorithm.
z = fmin(func, z, args=(TEST_STARS,), full_output=0, xtol=2e-6)
print "Mount errors (rad):", z
print "Mount errors (deg):", z*180/pi

pe, te = calc_errors(z, TEST_STARS)
pylab.plot(pe, te, 'ro')
pylab.xlim([-.5, .5])
pylab.ylim([-.5, .5])
pylab.grid(True)
pylab.xlabel("Phi error")
pylab.ylabel("Theta error")
pylab.show()
