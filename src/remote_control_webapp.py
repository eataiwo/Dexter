from flask import Flask, render_template, redirect, url_for, make_response, Response
import socket

from powertrain.powertrain import Powertrain
from camera.camera import Camera

dexter = Powertrain()
dexter.setup()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', speed=dexter.speed)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/forward')
def forward():
    dexter.direction = 'forward'
    if not dexter.drive:
        dexter.remote_control()
    return "nothing"


@app.route('/backward')
def backward():
    dexter.direction = 'backward'
    if not dexter.drive:
        dexter.remote_control()
    return "nothing"


@app.route('/left')
def left():
    dexter.direction = 'left'
    if not dexter.drive:
        dexter.remote_control()
    return "nothing"


@app.route('/right')
def right():
    dexter.direction = 'right'
    if not dexter.drive:
        dexter.remote_control()
    return "nothing"


@app.route('/cw')
def tots_cw():
    dexter.direction = 'cw'
    if not dexter.drive:
        dexter.remote_control()
    return "nothing"


@app.route('/ccw')
def tots_ccw():
    dexter.direction = 'ccw'
    if not dexter.drive:
        dexter.remote_control()
    return "nothing"


@app.route('/stop')
def stop():
    dexter.stop()
    return "nothing"


@app.route('/speed_up')
def speed_up():
    dexter.speed += 5
    return "nothing"


@app.route('/speed_down')
def speed_down():
    dexter.speed -= 5
    return "nothing"


app.run(debug=True, host='0.0.0.0', port=8000, threaded=True)
