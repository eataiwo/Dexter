"""

"""
from src.powertrain.powertrain import Powertrain

# Motor pins - maybe look into adding info like this into a config file.
direction_pins = (27, 23, 19, 20)
step_pins = (22, 24, 26, 21)

dexter = Powertrain(direction_pins, step_pins)
dexter.setup()


# Testing objection creation
speed = 80
distance = 0.3
turn = 360
dexter.go('forward', distance, speed, 0.05, True)
dexter.go('backward', distance, speed, 1)
dexter.go('forward', distance, 100, 0.1)
dexter.go('backward', distance, 100, 0.1)
dexter.go('right', distance, speed, 1)
dexter.go('left', distance, speed, 1)
dexter.go('tots_cw', turn, speed, 1)
dexter.go('tots_ccw', turn, 100, 1)

# def listen():
#     while True:
#         'listen out for input direction and speed'
#         choice = input('What directions and how far do you want Dexter to go')
#         break
