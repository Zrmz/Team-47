# Project 3: GEARS Robot
# File: Proj3_main.py
# Date: 28 March, 2022
# By:   Zachary Ramirez
#       zrramire
#       Brandon Mar
#       Login ID
#       Adam Zogl
#       Login ID
#       Luke Muckerheide
#       Login ID
# Section: 3
# Team: 47
#
# ELECTRONIC SIGNATURE
# Zachary Ramirez
# Brandon Mar
# Adam Zogl
# Luke Muckerheide
#
# The electronic signatures above indicate that the program
# submitted for evaluation is the combined effort of all
# team members and that each member of the team was an
# equal participant in its creation. In addition, each
# member of the team has a general understanding of
# all aspects of the program development and execution.
#
# MAIN CODE FOR WALL FOLLOWING

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi

grovepi.set_bus("RPI_1")
BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.reset_all()

GYRO_PORT = BP.PORT_1
RIGHT_PORT = 4
FRONT_PORT = 3

LEFT = BP.PORT_D
RIGHT = BP.PORT_A
# Identify which motor ports on the pi are used

BP.set_sensor_type(GYRO_PORT, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)

gain = float(input("Set a gain value for PID: "))
optimalUlt= float(input("Enter the robot's optimal distance form the wall in cm: "))
speed = -1 * float(input("How fast should the robot move in DPS: "))
time.sleep(1)
def turn(angle):
    turnSpeed = -30
    turnTime = angle / turnSpeed
    BP.set_motor_dps(LEFT, turnSpeed)
    BP.set_motor_dps(RIGHT, -1 * turnSpeed)
    time.sleep(turnTime)
    BP.set_motor_dps(LEFT, 0)
    BP.set_motor_dps(RIGHT, 0)
    time.sleep(1)
    return()

def main():
    try:
        EVENT = 0
        ZeroPosition1 = BP.get_motor_encoder(LEFT)
        ZeroPosition2 = BP.get_motor_encoder(RIGHT)

        BP.offset_motor_encoder(LEFT, ZeroPosition1)
        BP.offset_motor_encoder(RIGHT, ZeroPosition2)

        optimalGyro = BP.get_sensor(GYRO_PORT)
        optimalGyro = optimalGyro[0]
        while (grovepi.ultrasonicRead(FRONT_PORT) > 30):
            gyro_current = BP.get_sensor(GYRO_PORT)
            angle_delta = gyro_current[0] - optimalGyro
            wall_delta = grovepi.ultrasonicRead(RIGHT_PORT) - optimalUlt
            if (grovepi.ultrasonicRead(RIGHT_PORT) > 40):
                EVENT = 1
                break
            correction = angle_delta * wall_delta / optimalUlt
            
            BP.set_motor_dps(LEFT, speed * (1 - correction))
            BP.set_motor_dps(RIGHT, speed)
        
        BP.set_motor_dps(LEFT, 0)
        BP.set_motor_dps(RIGHT, 0)
        time.sleep(1)
        if (EVENT == 0):
            turn(90)
        elif (EVENT == 1):
            turn(90)
            BP.set_motor_dps(LEFT, speed)
            BP.set_motor_dps(RIGHT, speed)
            time.sleep(1)           
    except KeyboardInterrupt:
        BP.reset_all()

if __name__ == "__main__":
    main()
