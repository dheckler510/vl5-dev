# Motor Control
import time
import threading

from adafruit_motorkit import MotorKit
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

# Constants
MOTOR_POSITIONS_FILE = "motor_positions.txt"
MAX_MOTOR_STEPS = 380  # Update this to your motor's step count

# Initialize MotorKits
kit1 = MotorKit(i2c=board.I2C())
kit2 = MotorKit(i2c=board.I2C())

# Create intuitive variables
cyan_motor = kit1.stepper1
magenta_motor = kit1.stepper2
yellow_motor = kit2.stepper1
diff_motor = kit2.stepper2

# Load motor positions from file on startup
def load_motor_positions():
    try:
        with open(MOTOR_POSITIONS_FILE, 'r') as f:
            positions = f.readlines()
            cyan_motor.stepper._position = int(positions[0])
            magenta_motor.stepper._position = int(positions[1])
            yellow_motor.stepper._position = int(positions[2])
            diff_motor.stepper._position = int(positions[3])
    except (FileNotFoundError, ValueError):
        print("No previous position file or invalid data. Using defaults.")

# Save motor positions to file
def save_motor_positions():
    with open(MOTOR_POSITIONS_FILE, 'w') as f:
        f.write(str(cyan_motor.stepper._position) + "\n")
        f.write(str(magenta_motor.stepper._position) + "\n")
        f.write(str(yellow_motor.stepper._position) + "\n")
        f.write(str(diff_motor.stepper._position) + "\n")

# Scaling function
def scale_value(value, max_steps=MAX_MOTOR_STEPS):
    return int(round((value / 100) * max_steps))

def set_color(desired_color, diffusion=0):
    color_positions = {
        "red":   (0, 100, 100, diffusion),
        "green": (100, 0, 100, diffusion),
        "blue":  (100, 100, 0, diffusion),
        "white": (100, 100, 100, diffusion),
        "purple": (75, 100, 0, diffusion),
        "orange": (0, 50, 100, diffusion)
    }

    if desired_color.lower() in color_positions:
        # Calculate relative movement needed
        cyan_target_delta, magenta_target_delta, yellow_target_delta, diff_target_delta = color_positions[desired_color.lower()]
        cyan_target = cyan_motor.stepper._position + scale_value(cyan_target_delta)
        magenta_target = magenta_motor.stepper._position + scale_value(magenta_target_delta)
        yellow_target = yellow_motor.stepper._position + scale_value(yellow_target_delta)
        diff_target = diff_motor.stepper._position + scale_value(diff_target_delta)

        threads = []
        threads.append(threading.Thread(target=move_motor, args=(cyan_motor, cyan_target)))
        threads.append(threading.Thread(target=move_motor, args=(magenta_motor, magenta_target)))
        threads.append(threading.Thread(target=move_motor, args=(yellow_motor, yellow_target)))
        threads.append(threading.Thread(target=move_motor, args=(diff_motor, diff_target)))

        # Start all threads
        for t in threads:
            t.start()

        save_motor_positions()

# Helper function for motor movement (handles reverse)
def move_motor(motor, target_position):
    steps_to_move = target_position - motor.stepper._position
    direction = stepper.FORWARD if steps_to_move >= 0 else stepper.BACKWARD

    for _ in range(abs(steps_to_move)):
        motor.onestep(direction=direction)
        time.sleep(0.005)

# Load positions at the start
load_motor_positions()

# ------------------------
# Flask Web Service Code
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/set_color/<color_name>/<diffusion>')
def api_set_color(color_name, diffusion):
    set_color(color_name, int(diffusion))
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
