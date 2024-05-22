import numpy as np
import datetime


def standard_angle(angle: float) -> float:
    """
    Takes an angle in radians and returns it in the interval 0, 2*pi

    :param angle: Angle to be standardised, in radians.
    :return: An equivalent angle in the interval 0, 2*pi
    """
    if (angle > 2 * np.pi) or (angle < 0):
        return angle % (2 * np.pi)
    else:
        return angle


def mjd_to_datetime(mjd: float) -> datetime.datetime:
    """
    Converts a Modified Julian Date to a datetime object

    :param mjd: Modified Julian Date
    :return: datetime.datetime object
    """
    return datetime.datetime(1858, 11, 17) + datetime.timedelta(days=mjd)


def datetime_to_mjd(date: datetime.datetime) -> float:
    """
    Converts a datetime object to a Modified Julian Date

    :param date: datetime.datetime object
    :return: Modified Julian Date
    """
    return (date - datetime.datetime(1858, 11, 17)).days
