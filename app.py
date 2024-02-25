from flask import Flask, jsonify
import time
import threading
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import board
import motor_control  # Your motor control file
from color_mixer import cyan_motor, magenta_motor, yellow_motor, diff_motor

app = Flask(__name__)

@app.route('/set_color/<color_name>/<diffusion>')
def api_set_color(color_name, diffusion):
    motor_control.set_color(color_name, int(diffusion))
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
