import numpy as np

def standard_angle(angle: float) -> float:
    """
    Takes an angle in radians and returns it in the interval 0, 2*pi

    :param angle: Angle to be standardised, in radians.
    :return: An equivalent angle in the interval 0, 2*pi
    """
    if (angle > 2*np.pi) or (angle < 0):
        return angle%(2*np.pi)
    else:
        return angle