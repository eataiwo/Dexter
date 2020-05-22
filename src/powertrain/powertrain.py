"""
Numbering/Naming convention for wheels on Dexter
[1 , 2] [FL , FR]
[3 , 4] [RL , RR]
"""

import sys
import RPi.GPIO as GPIO
from src.powertrain.step_converter import dist_2_steps
from src.powertrain.step_converter import steps_2_dist
from src.powertrain.speed_converter import percentage_to_step_delay
from src.powertrain.speed_converter import step_delay_to_percentage
from src.powertrain.step_converter import deg_2_steps
from time import sleep


# Turning is relative to if you were looking down onto the robot from above
directions = {'forward': (0, 1, 0, 1), 'backward': (1, 0, 1, 0),
              'left': (1, 1, 0, 0), 'right': (0, 0, 1, 1),
              'tots_cw': (0, 0, 0, 0), 'tots_ccw': (1, 1, 1, 1),
              'diag_fl': (' ', 1, 0, ' '), 'diag_fr': (1, ' ', ' ', 0),
              'diag_rl': (0, ' ', ' ', 1), 'diag_rr': (' ', 0, 1, ' '),
              'cor_right_cw:': (0, ' ', 0, ' '), 'cor_right_ccw': (1, ' ', 1, ' '),
              'cor_left_cw:': (' ', 1, ' ', 1), 'cor_left_ccw': (' ', 0, ' ', 0),
              'tur_rear_ax_cw': (0, 0, ' ', ' '), 'tur_rear_ax_ccw': (1, 1, ' ', ' '),
              'tur_front_ax_cw': (' ', ' ', 0, 0), 'tur_front_ax_ccw': (' ', ' ', 1, 1)}


class Powertrain:
    def __init__(self, direction_pins, step_pins):
        self.direction_pins = direction_pins
        self.step_pins = step_pins
        self.directions = directions
        self.drive = False
        self.remote_direction = ''

        # TODO: Change direction to self.direction and see if it works

    def go(self, direction='forward', distance=0.1, speed=30, initdelay=.05, verbose=False):
        GPIO.output(self.direction_pins, directions[direction])
        stepdelay = percentage_to_step_delay(speed)

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
                print(f"Total distance travelled = {steps_2_dist(steps)}m ")
        finally:
            # cleanup
            GPIO.output(self.step_pins, False)
            GPIO.output(self.direction_pins, False)

    def go_remote(self, speed=50, initdelay=.05, verbose=False):
        stepdelay = percentage_to_step_delay(speed)
        print(f'Speed is {speed}, and stepdelay is {stepdelay}')
        self.drive = True
        try:
            while self.drive:
                # TODO: Finish implementation of if statements for directions
                self.go_steps(self.remote_direction, 1, stepdelay, 0)
        except KeyboardInterrupt:
            print("User Keyboard Interrupt : Remote Controller")
        except Exception as remote_error:
            print(sys.exc_info()[0])
            print(remote_error)
            print("Unexpected error:")
        finally:
            # print report status
            GPIO.output(self.step_pins, False)
            GPIO.output(self.direction_pins, False)

    def go_steps(self, direction='forward', steps=100, stepdelay=.05, initdelay=.05, verbose=False):
        GPIO.output(self.direction_pins, directions[direction])
        sleep(initdelay)
        try:
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
            # print report status
        else:
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
            print("Finally loop works")
            GPIO.output(self.direction_pins, False)

    def wait_for_command(self, command=' '):
        pass

    def stop(self):
        self.drive = False
        GPIO.output(self.step_pins, False)
        GPIO.output(self.direction_pins, False)

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.direction_pins, GPIO.OUT)
        GPIO.setup(self.step_pins, GPIO.OUT)
