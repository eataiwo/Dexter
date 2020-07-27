from src.powertrain.speed_converter import percent_to_stepdelay
from src.powertrain.speed_converter import stepdelay_to_percent

MIN_STEPDELAY = 0.003  # Highest speed
MAX_STEPDELAY = 0.02  # Slowest speed


def stepdelay_check(stepdelay):
    if stepdelay > max_stepdelay:
        return max_stepdelay
    elif stepdelay < min_stepdelay:
        return min_stepdelay
    else:
        return stepdelay


def speed_check(speed):
    stepdelay = percent_to_stepdelay(speed)
    checked_stepdelay = stepdelay_check(stepdelay)
    return stepdelay_to_percent(checked_stepdelay)
