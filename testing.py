import sys
import RPi.GPIO as GPIO
from utils.step_converter import *
from time import sleep

"""
Numbering/Naming convention for wheels on Dexter
[1 , 2] [FL , FR]
[3 , 4] [RL , RR] 
"""

# Setting up GPIO pins for stepper motors
direction_pin = (27, 23, 19, 20)
step_pin = (22, 24, 26, 21)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Individual wheel direction depending on global direction. Clockwise = false, counterclockwise = true
# Relative to if you are looking from the motor casing towards the end of the shaft.

# TODO: Add diagonal directions
# Turning is relative to if you were looking down onto the robot from above
directions = {'forward': (0, 1, 0, 1), 'backwards': (1, 0, 1, 0),
              'left': (1, 1, 0, 0), 'right': (0, 0, 1, 1),
              'tots_cw': (1, 1, 1, 1), 'tots_ccw': (0, 0, 0, 0)}


# Modified function from RpiMotorLib -
def degree_calc(steps, steptype='Full'):
    """ calculate and returns size of turn in degree
    , passed number of steps and steptype"""
    degree_value = {'Full': 1.8,
                    'Half': 0.9,
                    '1/4': .45,
                    '1/8': .225,
                    '1/16': 0.1125,
                    '1/32': 0.05625}
    degree_value = (steps * degree_value[steptype])
    return degree_value


def dexter_go(direction='forward', steps=100, stepdelay=.1, verbose=False, initdelay=.05):
    GPIO.setup(direction_pin, GPIO.OUT)
    GPIO.setup(step_pin, GPIO.OUT)
    GPIO.output(direction_pin, directions[direction])
    try:
        sleep(initdelay)
        for i in range(steps):
            GPIO.output(step_pin, True)
            sleep(stepdelay)
            GPIO.output(step_pin, False)
            sleep(stepdelay)
            if verbose:
                print("Steps count {}".format(i))

    except KeyboardInterrupt:
        print("User Keyboard Interrupt : RpiMotorLib:")
    except Exception as motor_error:
        print(sys.exc_info()[0])
        print(motor_error)
        print("RpiMotorLib  : Unexpected error:")
    else:
        # print report status
        if verbose:
            print("\nMotor Run finished, Details:.\n")
            print(f"Direction = {direction}")
            print(f"Number of steps = {steps}")
            print(f"Step Delay = {stepdelay}")
            print(f"Initial delay = {initdelay}")
            print(f"Rotation of wheels in degrees = {degree_calc(steps)}")
            print(f"Total distance travelled = {steps_2_dist_wheel(steps)}m ")
    finally:
        # cleanup
        GPIO.output(step_pin, False)
        GPIO.output(direction_pin, False)


if __name__ == '__main__':
    dexter_go('forward', 100, 0.1, True)
