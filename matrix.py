from math import radians, cos, sin
from numpy import array


def rotMat(anglex,angley,anglez):
    anglex = radians(anglex)
    angley = radians(angley)
    anglez = radians(anglez)

    rot_matx = array([
        [1,      0,                 0],
        [0, cos(anglex), -sin(anglex)],
        [0, sin(anglex), cos(anglex)]])

    rot_maty = array([
        [cos(angley), 0, -sin(angley)],
        [0,            1,           0],
        [sin(angley), 0, cos(angley)]])

    rot_matz = array([
        [cos(anglez), -sin(anglez), 0],
        [sin(anglez), cos(anglez),  0],
        [0,               0,        1]])

    return rot_matx@rot_maty@rot_matz