"""
Functions for converting stepper motor parameter to more useful
ones and vice versa.

"""

# Define lower and upper bounds
# For a stepper motor speed is determined by the time between steps
# and is the delay between switching the step pin high to low: stepdelay variable
# These values were found empirically

upp_stepdelay = 0.003  # Highest speed
low_stepdelay = 0.02  # Slowest speed


# This type of scaling is imperfect but best I can do without any accurate speed measurements

def stepdelay_to_percent(stepdelay):
    """
    Converts stepper motor stepdelay into a percentage of max speed
    :param stepdelay: Delay in seconds between steps
    :type stepdelay: int, float
    :return: percentage of max speed
    """
    if upp_stepdelay <= stepdelay <= low_stepdelay:
        return 100 - (((stepdelay - upp_stepdelay) * 100) / (low_stepdelay - upp_stepdelay))
    else:
        return None


def percent_to_stepdelay(percent):
    """
    Converts speed percentage into a stepdelay
    :param percent: Delay in seconds between steps
    :type percent: int, float
    :return: stepdelay of steps in seconds
    """
    if 0 <= percent <= 100:
        return (((100-percent)*(low_stepdelay-upp_stepdelay))/100) + upp_stepdelay
    else:
        return None


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
