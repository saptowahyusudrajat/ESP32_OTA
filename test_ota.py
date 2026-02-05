from machine import Pin
from time import sleep
p2 = Pin(2, Pin.OUT)

def loop():
  p2.value(0)
  sleep(1)
  p2.value(1)
  sleep(1)
  print("VERSI 30")
