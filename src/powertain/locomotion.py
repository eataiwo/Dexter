"""

"""
from . import powertrain

# Motor pins - maybe look into adding info like this into a config file.
direction_pins = (27, 23, 19, 20)
step_pins = (22, 24, 26, 21)

dexter = powertrain(direction_pins, step_pins)

# Testing objection creation
dexter.go('forward', 0.3, 50, 0.05, True)
dexter.go('backward', 0.3, 50, 1)
dexter.go('forward', 0.3, 50, 0.1)
dexter.go('backward', 0.3, 50, 0.1)
dexter.go('right', 0.3, 50, 1)
dexter.go('left', 0.3, 50, 1)
dexter.go('tots_cw', 1, 50, 1)
dexter.go('tots_ccw', 1, 50, 1)

for key in powertrain.directions.keys:
    try:
        dexter.go(key, 0.3, 50, 1, True)
    except Exception as error:
        print(error)


# def listen():
#     while True:
#         'listen out for input direction and speed'
#         choice = input('What directions and how far do you want Dexter to go')
#         break
