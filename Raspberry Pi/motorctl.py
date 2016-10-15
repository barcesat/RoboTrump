# Import required libraries
import sys
import time

# use on pi:
import RPi.GPIO as GPIO
# use on PC:
#from RPi import GPIO

# Use BCM GPIO references
# instead of physical pin numbers
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
#mode=GPIO.getmode()
#print " mode ="+str(mode)
#GPIO.cleanup()

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24

MotLA= 31
MotLB= 33
MotRA= 35
MotRB= 37
sleeptime=1


GPIO.setup(MotLA, GPIO.OUT)
GPIO.setup(MotLB, GPIO.OUT)
GPIO.setup(MotRA, GPIO.OUT)
GPIO.setup(MotRB, GPIO.OUT)

def forward():
    forwardL()
    forwardR()

def reverse():
    reverseL()
    reverseR()

def stop():
    stopL()
    stopR()

def TurnLeft():
    stopL()
    forwardR()

def TurnRight():
    stopR()
    forwardL()

def forwardL():
    GPIO.output(MotLA, GPIO.HIGH)
    GPIO.output(MotLB, GPIO.LOW)
    print "forwarding running left motor"
    #time.sleep(x)
    #GPIO.output(StepPinForward, GPIO.LOW)

def reverseL():
    GPIO.output(MotLA, GPIO.LOW)
    GPIO.output(MotLB, GPIO.HIGH)
    print "backwarding running left motor"
    #time.sleep(x)
    #GPIO.output(StepPinBackward, GPIO.LOW)

def stopL():
    GPIO.output(MotLA, GPIO.LOW)
    GPIO.output(MotLB, GPIO.LOW)
    print "stopping left motor"
    #time.sleep(x)
    #GPIO.output(StepPinBackward, GPIO.LOW)


def forwardR():
    GPIO.output(MotRA, GPIO.HIGH)
    GPIO.output(MotRB, GPIO.LOW)
    print "forwarding running right motor"
    #time.sleep(x)
    #GPIO.output(StepPinForward, GPIO.LOW)

def reverseR():
    GPIO.output(MotRA, GPIO.LOW)
    GPIO.output(MotRB, GPIO.HIGH)
    print "backwarding running right motor"
    #time.sleep(x)
    #GPIO.output(StepPinBackward, GPIO.LOW)

def stopR():
    GPIO.output(MotRA, GPIO.LOW)
    GPIO.output(MotRB, GPIO.LOW)
    print "stopping right motor"

def cleanup():
    GPIO.cleanup()

#test
'''
forwardL()
time.sleep(5)
reverseL()
time.sleep(5)
stopL()

forwardR()
time.sleep(5)
reverseR()
time.sleep(5)
stopR()
'''

#on exit
#GPIO.cleanup()
