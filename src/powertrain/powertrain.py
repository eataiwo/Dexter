"""
==================================================
Author: TJ Taiwo

Projects Referenced:
RpiMotorLib (Gavin Lyons) - https://github.com/gavinlyonsrepo/RpiMotorLib
gatoBot (Jorge Rancé) - https://github.com/jorgerance/gatoBot

==================================================
Numbering/Naming convention for wheels on Dexter
[1 , 2] [FL , FR]
[3 , 4] [RL , RR]
"""

import sys
import RPi.GPIO as GPIO
from src.powertrain.step_converter import dist_2_steps
from src.powertrain.speed_converter import percent_to_stepdelay
from src.powertrain.step_converter import deg_2_steps
from time import sleep

# Turning is relative to if you were looking down onto the robot from above
# Clockwise rotation is a value of 0, False, Low
# Motors should be connected so all motors spin the wheels forward when stepper motor is set in the clockwise direction
# TODO: Test that new directions dictionary corresponds to the right movements.
directions = {'forward': (0, 0, 0, 0), 'backward': (1, 1, 1, 1),
              'left': (1, 0, 0, 1), 'right': (0, 1, 1, 0),
              'tots_cw': (0, 1, 0, 1), 'tots_ccw': (1, 0, 1, 0),
              'diag_fl': (' ', 0, 0, ' '), 'diag_fr': (1, ' ', ' ', 1),
              'diag_rl': (0, ' ', ' ', 0), 'diag_rr': (' ', 1, 1, ' '),
              'cor_right_cw:': (0, ' ', 0, ' '), 'cor_right_ccw': (1, ' ', 1, ' '),
              'cor_left_cw:': (' ', 0, ' ', 0), 'cor_left_ccw': (' ', 1, ' ', 1),
              'tur_rear_ax_cw': (0, 1, ' ', ' '), 'tur_rear_ax_ccw': (1, 0, ' ', ' '),
              'tur_front_ax_cw': (' ', ' ', 0, 1), 'tur_front_ax_ccw': (' ', ' ', 1, 0)}


class Powertrain:
    """
    A class to control and interact with Dexter's powertrain.

    Attributes
    --------------
    direction_pins: GPIO pins connected to the direction pin on the stepper motor driver
    step_pins: GPIO pins connected to the step pin on the stepper motor driver
    directions: Dictionary that maps global directions to the individual wheel direction pins
    drive: Variable that tracks if the powertain is active or not
    remote_direction: Last direction sent from the web application

    Methods
    -------
    go():
        Moves Dexter based on desired direction, speed and distance.
    go_steps():
        Moves Dexter based on desired direction, step delay and number of steps
    remote():
        Moves Dexter based on commands from a web application
    stop():
        Stops Dexter
    setup():
        Setup for the powertrain
    """

    def __init__(self, direction_pins, step_pins):
        """
        :param direction_pins: GPIO pins connected to the direction pin on the stepper motor driver
        :param step_pins: GPIO pins connected to the step pin on the stepper motor driver
        :type direction_pins: list, tuple
        :type step_pins: list, tuple
        """

        self.direction_pins = direction_pins
        self.step_pins = step_pins
        self.drive = False
        self.direction = ''
        self.remote_direction = ''
        self.speed = 50

    def go(self, direction, distance, speed=0, initdelay=.05, verbose=False):
        """
        Moves Dexter based on desired direction, speed and distance.

        :param direction: Desired direction of Dexter.
        :param distance: Distance to be travelled in meters or degrees depending on direction.
        :param speed: Value from 0-100 for wheel speed.
        :param initdelay: Initial delay before motors begin moving.
        :param verbose: Prints information related to motor movement
        :type direction: str
        :type distance: int, float
        :type speed: int, float
        :type initdelay: int, float
        :type verbose: bool
        """

        self.direction = direction
        self.speed = speed
        GPIO.output(self.direction_pins, directions[direction])

        # Prevent user selecting speeds outside of the limits
        if 0 > speed:
            speed = 0

        elif speed > 100:
            speed = 100
        else:
            stepdelay = percent_to_stepdelay(speed)

        if direction in ['forward', 'backward', 'left', 'right']:
            steps = dist_2_steps(distance)[0]
        elif direction in ['tots_cw', 'tots_ccw']:
            steps = deg_2_steps(distance)[0]

        sleep(initdelay)

        try:
            for i in range(steps):
                GPIO.output(self.step_pins, True)
                sleep(stepdelay)
                GPIO.output(self.step_pins, False)
                sleep(stepdelay)
                if verbose:
                    print(f'Steps count {i}')
        except KeyboardInterrupt:
            print('User Keyboard Interrupt @ Powertrain.go()')
        except Exception as motor_error:
            print(sys.exc_info()[0])
            print(motor_error)
            print("Powertrain.go(): Unexpected error:")
        else:
            if verbose:
                print(f'Direction = {direction}')
                print(f'Number of steps = {steps}')
                print(f'Speed = {speed}')
                print(f'Step Delay = {stepdelay}')
                print(f'Initial delay = {initdelay}')
        finally:
            # cleanup
            GPIO.output(self.step_pins, False)
            GPIO.output(self.direction_pins, False)

    def go_steps(self, direction='forward', steps=100, stepdelay=.05, initdelay=.05, verbose=False):
        """
        Moves Dexter based on desired direction, stepdelay and number of steps.

        :param direction: Desired direction of Dexter.
        :param steps: Steps stepper motor should turn.
        :param stepdelay: Delay between each step in seconds.
        :param initdelay: Initial delay before motors begin moving.
        :param verbose: Prints information related to motor movement
        :type direction: str
        :type steps: int
        :type stepdelay: int, float
        :type initdelay: int, float
        :type verbose: bool
        """

        self.direction = direction
        GPIO.output(self.direction_pins, directions[direction])
        sleep(initdelay)

        try:
            for i in range(steps):
                GPIO.output(self.step_pins, True)
                sleep(stepdelay)
                GPIO.output(self.step_pins, False)
                sleep(stepdelay)
                if verbose:
                    print(f'Steps count {i}')
        except KeyboardInterrupt:
            print('User Keyboard Interrupt @ Powertrain.go_steps()')
        except Exception as motor_error:
            print(sys.exc_info()[0])
            print(motor_error)
            print("Powertrain.go_steps(): Unexpected error:")
        else:
            if verbose:
                print(f'Direction = {direction}')
                print(f'Number of steps = {steps}')
                print(f'Step Delay = {stepdelay}')
                print(f'Initial delay = {initdelay}')
        finally:
            # cleanup
            GPIO.output(self.step_pins, False)
            GPIO.output(self.direction_pins, False)

    def remote(self, verbose=False):
        """
        Moves Dexter based on desired direction from web application.

        :param speed: Steps stepper motor should turn.
        :param verbose: Prints information related to motor movement
        :type speed: int, float
        :type verbose: bool
        """

        self.drive = True

        if 0 > self.speed:
            self.speed = 0

        elif self.speed > 100:
            self.speed = 100
        else:
            stepdelay = percent_to_stepdelay(self.speed)

        while self.drive:
            self.go_steps(self.remote_direction, 1, stepdelay, 0, verbose)

    def stop(self):
        """
        Stops powertrain
        """
        self.drive = False
        GPIO.output(self.step_pins, False)
        GPIO.output(self.direction_pins, False)

    def setup(self):
        """
        Setup for powertrain
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.direction_pins, GPIO.OUT)
        GPIO.setup(self.step_pins, GPIO.OUT)

