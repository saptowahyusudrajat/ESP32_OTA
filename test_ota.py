from machine import Pin
from time import sleep
p5 = Pin(5, Pin.OUT)

def loop():
  p5.value(0)
  sleep(0.1)
  p5.value(1)
  sleep(0.1)
  print("Hello from surabaya")
