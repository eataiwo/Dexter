
import math as m

MIN_STEPDELAY = 0.003  # Highest speed
MAX_STEPDELAY = 0.01  # Slowest speed
ANG_SPEED_STEPDELAY = 0.006
ANG_SPEED_PERCENT = 50


def stepdelay_check(stepdelay):
    if stepdelay > MAX_STEPDELAY:
        return MAX_STEPDELAY
    elif stepdelay < MIN_STEPDELAY:
        return MIN_STEPDELAY
    else:
        return stepdelay


def speed_check(speed):
    if speed > 100:
        return 100
    elif speed < 0:
        return 0
    else:
        return speed


# Speed percentage to stepdelay conversions
def stepdelay_to_percent(stepdelay, speed_type='linear'):
    """
    Converts stepper motor stepdelay into a percentage of max speed
    :param stepdelay: Delay in seconds between steps
    :type stepdelay: int, float
    :param speed_type: Type of speed. Either linear or angular
    :type speed_type: string
    :return: percentage of the stepdelay within the defined threshold
    """
    stepdelay = stepdelay_check(stepdelay)
    percent = 100 - (((stepdelay - MIN_STEPDELAY) * 100) / (MAX_STEPDELAY - MIN_STEPDELAY))
    if speed_type == 'linear':
        return percent
    elif speed_type == 'angular':
        return ANG_SPEED_PERCENT


def percent_to_stepdelay(percent, speed_type='linear'):
    """
    Converts stepper motor stepdelay into a percentage of max speed
    :param percent: Delay in seconds between steps
    :type percent: int, float
    :param speed_type: Type of speed. Either linear or angular
    :type speed_type: string
    :return: percentage of the stepdelay within the defined threshold
    """
    percent = speed_check(percent)
    stepdelay = (((100 - percent) * (MAX_STEPDELAY - MIN_STEPDELAY)) / 100) + MIN_STEPDELAY
    if speed_type == 'linear':
        return stepdelay
    elif speed_type == 'angular':
        return ANG_SPEED_STEPDELAY


STEPS_PER_REV = {'full': 200,
                 'half': 400,
                 '1/4': 800,
                 '1/8': 1600,
                 '1/16': 3200,
                 '1/32': 6400}


def steps_2_dist(steps, wheel_rad=0.048, microstep="full", ):
    """
    Converts stepper motor steps into meters
    :param steps: stepper motor steps
    :param wheel_rad: Radius of robot wheels
    :param microstep: Microstepping setting. Set on stepper driver
    :type steps: int
    :type wheel_rad: int, float
    :type microstep: str
    :return: distance in meters
    """
    wheel_circum = (2 * m.pi) * wheel_rad  # in meters
    frac = steps / STEPS_PER_REV[microstep]
    return wheel_circum * frac


def dist_2_steps(dist, wheel_rad=0.048, microstep="full", ):
    """
    Converts stepper motor steps into meters
    :param dist: distance in meters
    :param wheel_rad: Radius of robot wheels
    :param microstep: Microstepping setting. Set on stepper driver
    :type dist: int, float
    :type wheel_rad: int, float
    :type microstep: str
    :return: distance in meters
    """
    wheel_circum = (2 * m.pi) * wheel_rad  # in meters
    revs = dist / wheel_circum
    steps = round(revs * STEPS_PER_REV[microstep])
    actual_dist = steps_2_dist(steps, wheel_rad, microstep)
    error = (abs(dist - actual_dist) / dist) * 100
    return [steps, actual_dist, error]  # Steps


def steps_2_deg(steps, dexter_rad=0.25, wheel_rad=0.048, microstep="full", ):
    """
    Converts stepper motor steps into meters
    :param steps: stepper motor steps
    :param dexter_rad: Radius from CoG to the front bumper, measured in CAD.
    :param wheel_rad: Radius of robot wheels
    :param microstep: Microstepping setting. Set on stepper driver
    :type steps: int
    :type wheel_rad: int, float
    :type microstep: str
    :return: rotation angle in degrees
    """
    dexter_circum = (2 * m.pi) * dexter_rad
    wheel_circum = (2 * m.pi) * wheel_rad  # in meters
    frac = steps / STEPS_PER_REV[microstep]
    dist = wheel_circum * frac
    return (dist / dexter_circum) * 360


def deg_2_steps(deg, dexter_rad=0.25):
    """
    Converts stepper motor steps into meters
    :param deg: rotation angle in degrees
    :param dexter_rad: Radius from CoG to the front bumper, measured in CAD.
    :type deg: int, float
    :return: array: [steps, actual rotation in degrees, error]
    """

    dexter_circum = (2 * m.pi) * dexter_rad
    dist = dexter_circum * (deg / 360)
    steps = dist_2_steps(dist)[0]
    actual_deg = steps_2_deg(steps)
    error = (abs(deg - actual_deg) / deg) * 100

    return [steps, actual_deg, error]  # Steps


if __name__ == '__main__':
    # Demo for speed checks

    # Demo on speed conversions
    stepdelays = [0.02, 0.01, 0.0075, 0.005, 0.004, 0.003]
    speed_percent = []
    for i in stepdelays:
        speed_percent.append(stepdelay_to_percent(i))
        print(f'The percentage of speed for a stepdelay of {i:.3f}s is {speed_percent[-1]:.2f}%')

    for i in speed_percent:
        rev_stepdelay = percent_to_stepdelay(round(i))
        print(f'Using the inverse function the stepdelay value from a speed percentage of {round(i):.2f}% is '
              f'{rev_stepdelay:.6f}s')

    # Demo of step conversions
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
    TEST_STEPS = 1066
    DEG = steps_2_deg(TEST_STEPS)
    print(f'Going {TEST_STEPS} steps using full microstepping Dexter went '
          f'{DEG:.2f} degrees')

    print('\nTesting function deg_2_steps')
    TEST_DEG = 360
    STEPS = deg_2_steps(TEST_DEG)
    print(f'Going {TEST_DEG} degrees using full microstepping Dexter did '
          f'{STEPS[0]} steps. The actual step degree is {STEPS[1]:.5f}degrees, with an error of {STEPS[2]:.5f}%')
