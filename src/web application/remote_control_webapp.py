from flask import Flask, render_template, request, redirect, url_for, make_response
import RPi.GPIO as GPIO
# import motors
import socket
from src.powertrain.powertrain import Powertrain

direction_pins = (27, 23, 19, 20)
step_pins = (22, 24, 26, 21)

dexter = Powertrain(direction_pins, step_pins)
dexter.setup()

# Get server ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server_ip = s.getsockname()[0]
s.close()

app = Flask(__name__)


# TODO: Edit index.html and control app to include turning on the spot.
# TODO: Edit index.html for centering the buttons and sizing them so they fit on my iphone and laptop screens.
@app.route('/')
def index():
    return render_template('index.html', server_ip=server_ip)


@app.route('/<changepin>', methods=['POST'])
def reroute(changepin):
    changePin = int(changepin)
    if changePin == 1:
        dexter.remote_direction = 'left'
    elif changePin == 2:
        dexter.remote_direction = 'forward'
    elif changePin == 3:
        dexter.remote_direction = 'right'
    elif changePin == 4:
        dexter.remote_direction = 'backward'
    elif changePin == 5:
        dexter.stop()
    elif changePin == 6:
        dexter.remote_direction = 'tots_cw'
    elif changePin == 7:
        dexter.remote_direction = 'tots_ccw'
    elif changePin == 8:
        dexter.speed -= 5
    elif changePin == 9:
        dexter.speed += 5
    else:
        print("Wrong command")

    if not dexter.drive and changePin != 5 or changePin == 8 or changePin == 9:
        # Move dexter with the new powertrain variables
        dexter.remote()

    response = make_response(redirect(url_for('index')))
    return response


app.run(debug=True, host='0.0.0.0', port=8000)
