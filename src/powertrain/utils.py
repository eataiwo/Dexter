#from powertrain.speed_converter import percent_to_stepdelay
#from powertrain.speed_converter import stepdelay_to_percent

MIN_STEPDELAY = 0.003  # Highest speed
MAX_STEPDELAY = 0.02  # Slowest speed


def stepdelay_check(stepdelay):
    if stepdelay > MAX_STEPDELAY:
        return MAX_STEPDELAY
    elif stepdelay < MIN_STEPDELAY:
        return MIN_STEPDELAY
    else:
        return stepdelay


def speed_check(speed):
    stepdelay = percent_to_stepdelay(speed)
    checked_stepdelay = stepdelay_check(stepdelay)
    return stepdelay_to_percent(checked_stepdelay)
