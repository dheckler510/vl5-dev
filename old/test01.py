# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
import board
from adafruit_motorkit import MotorKit

kit1 = MotorKit(i2c=board.I2C())

for i in range(200):
    kit1.stepper1.onestep(style=stepper.DOUBLE)
    time.sleep(0.01)
