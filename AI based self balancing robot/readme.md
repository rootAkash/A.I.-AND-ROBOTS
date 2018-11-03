This is my project where i made a self balancing robot using reinforcement learning.
The training algorithm used is deep Q learning (tried with policy gradients method takes time to learn).
Used two arduinos one for getting gyroscope data (kalman filter is used), another for contorlling the motors.
I2c.ino and sketch_sep19c.ino files are for getting angle from mpu 6050, and motor.ino for motor control(only forward and backward)
working_angle_2_arduino.py is what was used ,other programs are variant of this code.
A sequential neural network with two outputs(only forward and backwork with a constant speed ) is used and the robot learns to balance by oscillating.
