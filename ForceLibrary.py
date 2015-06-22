

import RPi.GPIO as GPIO
import time

class ForceEngine:
  
  def __init__(self, pin, forceDurationThreshold):
    self.pin = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)
    self.forceDurationThreshold = forceDurationThreshold
    self.forceDuration = 0

  def isPushed(self):
    state = GPIO.input(self.pin)
    isOn = not state

    if not isOn:
      self.forceDuration = 0      
      return False
    else:
      self.forceDuration += 1

      if self.forceDurationThreshold <= self.forceDuration:
        return True

      print 'force is applied but threashold is not reached. Current count: %d' % self.forceDuration
      return False


def test():
  GPIO.setmode(GPIO.BCM)
  GPIO.cleanup()
  GPIO.setwarnings(False)
  GPIO.setup(17, GPIO.OUT)
  GPIO.setup(27, GPIO.OUT)
  print "Lights on"
  GPIO.output(17, GPIO.HIGH)
  GPIO.output(27, GPIO.HIGH)











def is_force_Active():
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(17,GPIO.IN)
      input = GPIO.input(17)
      while True:
       if (GPIO.input(17)):
        return True
        print("force is pressed")


#def is_force_Active():
 # prev_input = 0
  #while True:
   #input = GPIO.input(17)
    #if (not prev_input and input):
     # print("Button pressed")
      #prev_input = input



def is_status(pin):
    GPIO.setup(pin, GPIO.IN)
    state = GPIO.input(pin)
    if (state is True):
     return True
    else:
     return False

def isPushed(pin = 17):
  GPIO.setup(pin, GPIO.IN)
  state = GPIO.input(pin)
  return state
