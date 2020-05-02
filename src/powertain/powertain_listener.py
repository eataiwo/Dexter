"""

"""
from utils.Motor import Motor
from . import locomotion

# Motor pins - maybe look into adding info like this into a config file.
# TODO: Finish adding the pins here
pins = {'FR': (1, 2)}

FR_motor = Motor(pins['FR'])
FL_motor = Motor()

RR_motor = Motor()
RL_motor = Motor()


def listen():
    while True:
        'listen out for input direction and speed'
        choice = input('What directions and how far do you want Dexter to go')

        # e.g.
        locomotion.motor_go.forward()
        break
