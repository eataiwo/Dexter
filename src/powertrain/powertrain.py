"""
Numbering/Naming convention for wheels on Dexter
[1 , 2] [FL , FR]
[3 , 4] [RL , RR]
"""

import sys
import RPi.GPIO as GPIO
from utils.step_converter import dist_2_steps_wheel
from utils.step_converter import steps_2_dist_wheel
from utils.speed_converter import percentage_to_step_delay
from time import sleep
from utils.Motor import degree_calc

# Turning is relative to if you were looking down onto the robot from above
directions = {'forward': (0, 1, 0, 1), 'backward': (1, 0, 1, 0),
              'left': (1, 1, 0, 0), 'right': (0, 0, 1, 1),
              'tots_cw': (0, 0, 0, 0), 'tots_ccw': (1, 1, 1, 1),  # In the following key value pairs only two wheels
              'diag_fl': (' ', 1, 0, ' '), 'diag_fr': (1, ' ', ' ', 0),
              # will be driven. Undriven wills will use placeholder
              'diag_rl': (0, ' ', ' ', 1), 'diag_rr': (' ', 0, 1, ' '),
              # values of 0 for motor direction. Alternative is to
              'cor_right_cw:': (0, ' ', 0, ' '), 'cor_right_ccw': (1, ' ', 1, ' '),  # to use None.
              'cor_left_cw:': (' ', 1, ' ', 1), 'cor_left_ccw': (' ', 0, ' ', 0),
              'tur_rear_ax_cw': (0, 0, ' ', ' '), 'tur_rear_ax_ccw': (1, 1, ' ', ' '),
              'tur_front_ax_cw': (' ', ' ', 0, 0), 'tur_front_ax_ccw': (' ', ' ', 1, 1)}


class Powertrain:
    def __init__(self, direction_pins, step_pins):
        self.direction_pins = direction_pins
        self.step_pins = step_pins
        self.directions = directions

    def go(self, direction='forward', distance=0.1, speed=30, initdelay=.05, verbose=False):
        steps = dist_2_steps_wheel(distance)[0]
        stepdelay = percentage_to_step_delay(speed)
        #       print(f' calc steps is {steps} and calc stepdelay is {stepdelay}')

        if 'diag' in direction or 'cor' in direction or 'tur' in direction:
            mod_step_pins = []
            print("Not sure how to handle this direction yet")
            for i, val in enumerate(directions[direction]):
                if val != ' ':
                    mod_step_pins.append(self.step_pins[i])

        try:
            sleep(initdelay)
            for i in range(steps):
                if 'diag' in direction or 'cor' in direction or 'tur' in direction:
                    mod_step_pins = []
                    print("Not sure how to handle this direction yet")
                    for j, val in enumerate(directions[direction]):
                        if val != ' ':
                            mod_step_pins.append(self.step_pins[j])
                    #                print('Attempting to do one step')
                    GPIO.output(mod_step_pins, True)
                    #                print('Step completed')
                    sleep(stepdelay)
                    GPIO.output(mod_step_pins, False)
                    sleep(stepdelay)
                    if verbose:
                        print("Steps count {}".format(i))
                else:
                    GPIO.output(self.step_pins, True)
                    #                print('Step completed')
                    sleep(stepdelay)
                    GPIO.output(self.step_pins, False)
                    sleep(stepdelay)
                    if verbose:
                        print("Steps count {}".format(i))

        except KeyboardInterrupt:
            print("User Keyboard Interrupt : RpiMotorLib:")
        except Exception as motor_error:
            print(sys.exc_info()[0])
            print(motor_error)
            print("RpiMotorLib  :(is it here)  Unexpected error:")
        else:
            # print report status
            if verbose:
                print('\nMotor Run finished, Details:\n')
                print(f'Direction = {direction}')
                print(f"Number of steps = {steps}")
                print(f"Step Delay = {stepdelay}")
                print(f"Initial delay = {initdelay}")
                print(f"Rotation of wheels in degrees = {degree_calc(steps)}")
                print(f"Total distance travelled = {steps_2_dist_wheel(steps)}m ")
        finally:
            # cleanup
            GPIO.output(self.step_pins, False)
            GPIO.output(self.direction_pins, False)

    def go_steps(self, direction='forward', steps=100, stepdelay=.05, initdelay=.05, verbose=False):
        GPIO.output(self.direction_pins, directions[direction])
        try:
            sleep(initdelay)
            for i in range(steps):
                GPIO.output(self.step_pins, True)
                sleep(stepdelay)
                GPIO.output(self.step_pins, False)
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
            GPIO.output(self.step_pins, False)
            GPIO.output(self.direction_pins, False)

    def turn(self, turn_type='tots_cw'):
        # TODO:
        # For handling turning
        pass

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.direction_pins, GPIO.OUT)
        GPIO.setup(self.step_pins, GPIO.OUT)
