from adafruit_motorkit import MotorKit
# Initialise the first hat on the default address
kit1 = MotorKit()
# Initialise the second hat on a different address
kit2 = MotorKit(address=0x61)

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
import board
from adafruit_motorkit import MotorKit

kit1 = MotorKit(i2c=board.I2C())

for i in range(200):
    kit1.stepper1.onestep(style=stepper.MICROSTEP)

