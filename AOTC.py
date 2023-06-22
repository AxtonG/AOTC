import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define GPIO pins
Side1LEDG = 23
Side1LEDY = 24
Side1LEDR = 25

Side2LEDG = 16
Side2LEDY = 20
Side2LEDR = 21

Side1Trig = 26
Side1Echo = 13

Side2Trig = 19
Side2Echo = 6

# setup pins with action
GPIO.setup(Side1LEDG, GPIO.OUT)
GPIO.setup(Side1LEDY, GPIO.OUT)
GPIO.setup(Side1LEDR, GPIO.OUT)
GPIO.setup(Side2LEDG, GPIO.OUT)
GPIO.setup(Side2LEDY, GPIO.OUT)
GPIO.setup(Side2LEDR, GPIO.OUT)
GPIO.setup(Side1Trig, GPIO.OUT)
GPIO.setup(Side2Trig, GPIO.OUT)
GPIO.setup(Side1Echo, GPIO.IN)
GPIO.setup(Side2Echo, GPIO.IN)

# prompts
print('Speed limit:') # units can vary on scale
s1 = float(input())
print('Distance across:') # units can vary on scale
da = float(input())
time2cross = round(1.3 * (int((da/sl)*2600))) # in seconds... units can vary on scale
print('How long do you want program to run:')
timer = int(input())

def program():
  # initials
  GPIO.output(Side1LEDR, GPIO.HIGH)
  GPIO.output(Side2LEDR, GPIO.HIGH)
  i=0
  # yellow light indicator; if prevlight[0] is 'G'
  prevlight1 = ['R'] # begins red
  prevlight2 = ['R']

  while i < timer:
    #check sensor one
    GPIO.output(Side1Trig, False)
    time.sleep(.001)
    GPIO.output(Side1Trig, True)
    time.sleep(.001)
    GPIO.output(Side1Trig, False)
    while GPIO.input(Side1Echo) == 0:
      ps1 = time.time()
    while GPIO.input(Side1Echo) == 1:
      pe1 = time.time()
    pulsedur = pe1- ps1
    dist1 = oulsedur * 17150 # in cm... units can vary and are up to change 
    #check sensor two
    GPIO.output(Side2Trig, False)
    time.sleep(.001)
    GPIO.output(Side2Trig, True)
    time.sleep(.001)
    GPIO.output(Side2Trig, False)
    while GPIO.input(Side2Echo) == 0:
      ps2 = time.time()
    while GPIO.input(Side2Echo) == 1:
      pe2 = time.time()
    pulsedur2 = pe2 - ps2
    dist2 = pulsedur2 * 17150 # in cm... units can vary and are up to change 
    if dist1 < 10: # car detected by sensor one... can vary based on how sensitive you want it to be
      if prevlight2[0] == 'G':
        GPIO.output(Side2LEDG, GPIO.LOW)
        GPIO.output(Side2LEDY, GPIO.HIGH)
        time.sleep(3.5) # time for car to stop to yellow light
        GPIO.output(side2LEDY, GPIO.LOW)
        GPIO.output(Side2LEDR, GPIO.HIGH)
        prevlight2[0] = 'R'
        GPIO.output(Side1LEDR, GPIO.LOW)
        GPIO.output(Side1LEDG, GPIO.HIGH)
        prevlight1[0] = 'G'
        time.sleep(time2cross)
      elif prevlight1[0] == 'R':
        GPIO.output(Side1LEDR, GPIO.LOW)
        GPIO.output(Side1LEDG, GPIO.HIGH)
        prevlight1[0] == 'G'
        GPIO.output(Side2LEDR, GPIO.HIGH)
        prevlight2[0] = 'R'
        GPIO.output(Side2LEDG, GPIO.LOW)
        time.sleep(time2cross) # let light stay green after traffic begins to flow
    if dist2 < 10: # car detected by sesnor two... can vary based on how sensitive you want it to be
      if prevlight1[0] == 'G':
        GPIO.output(Side1LEDG, GPIO.LOW)
        GPIO.output(Side1LEDY, GPIO.HIGH)
        time.sleep(3.5) # time for car to stop to yellow light
        GPIO.output(side1LEDY, GPIO.LOW)
        GPIO.output(Side1LEDR, GPIO.HIGH)
        prevlight1[0] = 'R'
        GPIO.output(Side2LEDR, GPIO.LOW)
        GPIO.output(Side2LEDG, GPIO.HIGH)
        prevlight2[0] = 'G'
        time.sleep(time2cross)
      elif prevlight2[0] == 'R':
        GPIO.output(Side1LEDR, GPIO.HIGH)
        prevlight[0] = 'R'
        GPIO.output(Side1LEDG, GPIO.LOW)
        GPIO.output(Side2LEDR, GPIO.LOW)
        GPIO.output(Side2LEDG, GPIO.HIGH)
        prevlight2[0] = 'G'
        time.sleep(time2cross)
    time.sleep(.01)
    i += 1
program()
GPIO.output(Side1LEDR, GPIO.LOW)
GPIO.output(Side1LEDG, GPIO.LOW)
GPIO.output(Side1LEDY, GPIO.LOW)
GPIO.output(Side2LEDR, GPIO.LOW)
GPIO.output(Side2LEDG, GPIO.LOW)
GPIO.output(Side2LEDY, GPIO.LOW)
quit()
      
