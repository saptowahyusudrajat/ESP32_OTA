from machine import Pin
from time import sleep
p5 = Pin(5, Pin.OUT)

def loop():
  p5.value(0)
  sleep(0.2)
  p5.value(1)
  sleep(1)
  print("blink pesawat")
