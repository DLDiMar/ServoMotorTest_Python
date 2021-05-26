#motorTest.py
#Control a motor based on button input
#Board: Raspberry Pi 3 A+
#05/25/2021
#Notes
# 3-Button circuit with two LED's to indicate justification of servo motor
# I/O for buttons and LED's are pull-up resistors to common ground
# Servo Motor: EMAX ES08A Servo Motor
#--------------------------------------------------------------------------

#Import GPIO setup
import RPi.GPIO as GPIO
#import sleep for stop
from time import sleep

#GPIO Setup: Input and PWM Output
#Pin 2: 3.3V (Button and LED Power)
#Pin 4: 5V (Servo Motor Power)
#Pin 6: GND
#Pin 33: Motor Output PWM
#Pin 16: Right Button
#Pin 18: Neutral Button
#Pin 22: Left Button
#Pin 36: Red LED
#Pin 37: Green LED

#Setup GPIO Board
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


#--------------------------------------------------------------------------

#Setup LED's
#Green LED
GPIO.setup(37, GPIO.OUT)
#Red LED
GPIO.setup(36, GPIO.OUT)

#--------------------------------------------------------------------------

#Button Setup

#Button 1: Left-Justified Servo Position
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#Button 2: Neutral-Justified Servo Position
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#Button 3: Right-Justified Servo Position
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#--------------------------------------------------------------------------

#Servo Motor Setup + Justification

#Left: setAngle(180)
#Right: setAngle(0)
#Neutral: setAngle(90)
#Pin 33: Available with PWM Output

#Set motor to GPIO Out
GPIO.setup(33, GPIO.OUT)
#Give Pulse Width Modulation: 50Hz
pwm = GPIO.PWM(33, 50)
#Initiate PWM at 0
pwm.start(0)

#--------------------------------------------------------------------------

#Callback Section

#Define Left Button Interrupt Callback
def buttonLeft_callback(channel):
    #Set motor to left angle relative to Neutral
    setAngle(0)
    #Turn on only Red LED
    GPIO.output(36, True)
    GPIO.output(37, False)

#Define Neutral Button Interrupt Callback
def buttonNeutral_callback(channel):
    #Set motor to middle angle relative to Neutral
    setAngle(90)
    #Turn on both Red LED and Green LED
    GPIO.output(36, True)
    GPIO.output(37, True)

#Define Right Button Interrupt Callback
def buttonRight_callback(channel):
    #Set motor to right angle relative to Neutral
    setAngle(180)
    #Turn on only Green LED
    GPIO.output(36, False)
    GPIO.output(37, True)

#--------------------------------------------------------------------------

#Servo Motor Operation
#Set angles to servo as percent duty cycle w/ equation: (Angle/20) + 2.1
#Min @ 0 deg = 2.1
#Mid @ 90 deg = 6.6
#Max @ 180 deg = 11.1
#Calibrated for: EMAX ES08A Servo Motor

def setAngle(angle):
    duty = angle/20.0 + 2.1
    # Turn on output to servo
    GPIO.output(33, True)
    # Change duty cycle to requested angle
    pwm.ChangeDutyCycle(duty)
    # Stop output once reached requested angle
    GPIO.output(33, False)
    #Wait for 3/4 second
    sleep(0.75)
    #Reset duty cycle
    #pwm.ChangeDutyCycle(0)

#--------------------------------------------------------------------------

#Define main function and Operate Main

def main():
    #Start motor at Neutral position and turn on both LED's
    setAngle(90)
    GPIO.output(36, True)
    GPIO.output(37, True)
    #Detect button presses and move motor and LED lighting accordingly
    #Left Button Callback
    GPIO.add_event_detect(22, GPIO.RISING, callback = buttonLeft_callback)
    #Neutral Button Callback
    GPIO.add_event_detect(18, GPIO.RISING, callback = buttonNeutral_callback)
    #Right Button Callback
    GPIO.add_event_detect(22, GPIO.RISING, callback = buttonRight_callback)

    #Output to console for method of closing program
    message = input("Press and Enter 'q' to quit\n")
    #If pressed, quit program and cleanup
    if message == 'q':
        pwm.stop()
        GPIO.cleanup()

#Run Main
main()
