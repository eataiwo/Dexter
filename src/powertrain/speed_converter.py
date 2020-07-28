"""
Functions for converting stepper motor parameter to more useful
ones and vice versa.

"""

from src.powertrain.utils import speed_check, stepdelay_check

# Define lower and upper bounds
# For a stepper motor speed is determined by the time between steps
# and is the delay between switching the step pin high to low: stepdelay variable
# These values were found empirically

MIN_STEPDELAY = 0.003  # Highest speed
MAX_STEPDELAY = 0.02  # Slowest speed
ANG_SPEED_FACTOR = 2  # Conversion factor for going from linear speed to angular speed.


# This type of scaling is imperfect but best I can do without any accurate speed measurements

def stepdelay_to_percent(stepdelay, speed_type='linear'):
    """
    Converts stepper motor stepdelay into a percentage of max speed
    :param stepdelay: Delay in seconds between steps
    :type stepdelay: int, float
    :param speed_type: Type of speed. Either linear or angular
    :type speed_type: string
    :return: percentage of the stepdelay within the defined threshold
    """
    if MIN_STEPDELAY <= stepdelay <= MAX_STEPDELAY:
        percent = 100 - (((stepdelay - MIN_STEPDELAY) * 100) / (MAX_STEPDELAY - MIN_STEPDELAY))
        if speed_type == 'linear':
            return percent
        elif speed_type == 'angular':
            return percent * ANG_SPEED_FACTOR
    else:
        return None


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
        return stepdelay / ANG_SPEED_FACTOR


if __name__ == '__main__':
    stepdelays = [0.02, 0.01, 0.0075, 0.005, 0.004, 0.003]
    speed_percent = []
    for i in stepdelays:
        speed_percent.append(stepdelay_to_percent(i))
        print(f'The percentage of speed for a stepdelay of {i:.3f}s is {speed_percent[-1]:.2f}%')

    for i in speed_percent:
        rev_stepdelay = percent_to_stepdelay(round(i))
        print(f'Using the inverse function the stepdelay value from a speed percentage of {round(i):.2f}% is '
              f'{rev_stepdelay:.6f}s')
