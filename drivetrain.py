"""
Author: Zach Ramirez, zrramire@purdue.edu
Name: Drive Train
Date: 01/24/2022

Description:
    Runs the motors for an X-Drive to maintain distance from a wall

Contributors:
    None

My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""
import time
import brickpi3
import math as m

BP = brickpi3.BrickPi3()
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE_ULTRASONIC)
# Define sensors and brickPi

frontLeft = BP.PORT_A
frontRight = BP.PORT_B
backLeft = BP.PORT_C
backRight = BP.PORT_D
# Name motor ports for easier readability

def goStraight(directions):
    
    x = 0
    motors = [frontLeft, frontRight, backLeft, backRight]
    changeMat = [m.cos(m.pi / 4 + x * m.pi / 2), m.sin(m.pi / 4 + x * m.pi / 2), -m.sin(m.pi / 4 + x * m.pi / 2), m.cos(m.pi / 4 + x * m.pi / 2)]
    sensorMatrix = [BP.get_sensor(BP.PORT_1), BP.get_sensor(BP.PORT_2), BP.get_sensor(BP.PORT_3), BP.get_sensor(BP.PORT_4)]
    try:
        while True:
            try:
                front = sensorMatrix(x % 4)
                side = sensorMatrix((x + 1) % 4)
            except brickpi3.SensorError:
                pass
            time.sleep(0.02)
            
            while front > 6:
                BP.set_motor_power(frontLeft, changeMat(1) * m.sqrt(2) * 50)
                BP.set_motor_power(frontRight, changeMat(2) * m.sqrt(2) * 50)
                BP.set_motor_power(backLeft, changeMat(3) * m.sqrt(2) * 50)
                BP.set_motor_power(backRight, changeMat(4) * m.sqrt(2) * 50)
                
                if side > 6:
                    time.sleep(0.05)
                    x = x + 1
                    
                
    except KeyboardInterrupt:
        BP.reset_all()