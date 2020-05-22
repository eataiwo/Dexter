"""
Functions for converting steps to other useful information and vice-versa
"""
import math as m

STEPS_PER_REV = {'full': 200,
                 'half': 400,
                 '1/4': 800,
                 '1/8': 1600,
                 '1/16': 3200,
                 '1/32': 6400}


def steps_2_dist(steps, wheel_rad=0.048, microstep="full", ):
    """

    :param steps:
    :param wheel_rad:
    :param microstep:
    :return:
    """

    wheel_circum = (2 * m.pi) * wheel_rad  # in meters
    frac = steps / STEPS_PER_REV[microstep]
    return wheel_circum * frac


def dist_2_steps(dist, wheel_rad=0.048, microstep="full", ):
    """

    :param dist:
    :param wheel_rad:
    :param microstep:
    :return:
    """
    wheel_circum = (2 * m.pi) * wheel_rad  # in meters
    revs = dist / wheel_circum
    steps = round(revs * STEPS_PER_REV[microstep])
    actual_dist = steps_2_dist(steps, wheel_rad, microstep)
    error = (abs(dist - actual_dist) / dist) * 100
    return [steps, actual_dist, error]  # Steps


def steps_2_deg(steps, wheel_rad=0.048, microstep="full", ):
    """

    :param steps:
    :param wheel_rad:
    :param microstep:
    :return:
    """

    dexter_rad = 0.19055427
    dexter_circum = (2 * m.pi) * dexter_rad

    wheel_circum = (2 * m.pi) * wheel_rad  # in meters
    frac = steps / STEPS_PER_REV[microstep]
    dist = wheel_circum * frac
    return (dist / dexter_circum) * 360


def deg_2_steps(deg):
    """
    :param deg:
    :param wheel_rad:
    :param microstep:
    :return:
    """
    dexter_rad = 0.19055427  # Radius from CoG to the centreline of front left wheel, measured in CAD.
    dexter_circum = (2 * m.pi) * dexter_rad
    dist = dexter_circum * (deg / 360)
    steps = dist_2_steps(dist)[0]
    actual_deg = steps_2_deg(steps)
    error = (abs(deg - actual_deg) / deg) * 100

    return [steps, actual_deg, error]  # Steps


# Testing function outputs
if __name__ == '__main__':
    print('Testing function steps_2_dist')
    TEST_STEPS = 6400
    DIST = steps_2_dist(TEST_STEPS)
    print(f'Going {TEST_STEPS} steps using full microstepping Dexter went '
          f'{DIST:.2f}m')

    print('\nTesting function dist_2_steps')
    TEST_DIST = 1
    STEPS = dist_2_steps(TEST_DIST)
    print(f'Going {TEST_DIST}m using full microstepping Dexter did '
          f'{STEPS[0]} steps. The actual step distance is {STEPS[1]:.5f}m, with an error of {STEPS[2]:.5f}%')

    print('\nTesting function steps_2_deg')
    TEST_STEPS = 1000
    DEG = steps_2_deg(TEST_STEPS)
    print(f'Going {TEST_STEPS} steps using full microstepping Dexter went '
          f'{DEG:.2f} degrees')

    print('\nTesting function deg_2_steps')
    TEST_DEG = 360
    STEPS = deg_2_steps(TEST_DEG)
    print(f'Going {TEST_DEG} degrees using full microstepping Dexter did '
          f'{STEPS[0]} steps. The actual step degree is {STEPS[1]:.5f}degrees, with an error of {STEPS[2]:.5f}%')

# TODO: Fill out all the string docs, units and comment
