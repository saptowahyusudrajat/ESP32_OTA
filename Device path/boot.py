import network
import time

SSID = "InixindoZone-Selasar 3"
PASSWORD = "inix2023surabaya"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        print("Connected. IP:", wlan.ifconfig()[0])
    else:
        print("WiFi connection failed.")

connect_wifi()
