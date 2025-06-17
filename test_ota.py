from machine import Pin
from time import sleep
p5 = Pin(5, Pin.OUT)

while True:
  p5.value(0)
  sleep(1)
  p5.value(1)
  sleep(1)
  print("Hello Sapto")
