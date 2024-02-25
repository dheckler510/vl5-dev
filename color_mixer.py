import time
import threading
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import board
import motor_control

# Initialize MotorKits
kit1 = MotorKit(i2c=board.I2C())
kit2 = MotorKit(i2c=board.I2C())

# Create intuitive variables
cyan_motor = kit1.stepper1
magenta_motor = kit1.stepper2
yellow_motor = kit2.stepper1
diff_motor = kit2.stepper2

# Example usage:
motor_control.set_color("purple", diffusion=25)
motor_control.set_color("orange")
