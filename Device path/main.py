# import urequests
# import machine
# import time
# 
# from local_version import version as local_version
# 
# def get_remote_version():
#     try:
#         r = urequests.get("http://raw.githubusercontent.com/saptowahyusudrajat/ESP32_OTA/main/version.json")
#         remote_version = r.json().get("version")
#         r.close()
#         return remote_version
#     except Exception as e:
#         print("Error getting remote version:", e)
#         return None
# 
# def download_and_update():
#     try:
#         r = urequests.get("http://raw.githubusercontent.com/saptowahyusudrajat/ESP32_OTA/main/test_ota.py")
#         with open("test_ota.py", "w") as f:
#             f.write(r.text)
#         r.close()
# 
#         with open("local_version.py", "w") as f:
#             f.write(f"version = {get_remote_version()}\n")
# 
#         print("Updated successfully. Rebooting...")
#         time.sleep(2)
#         machine.reset()
#     except Exception as e:
#         print("Failed to update:", e)
# 
# def run():
#     remote_version = get_remote_version()
#     if remote_version and remote_version > local_version:
#         print(f"New version {remote_version} available. Updating...")
#         download_and_update()
#     else:
#         print("Already up to date.")
#         try:
#             import test_ota
#         except Exception as e:
#             print("Failed to run test_ota.py:", e)
# 
# run()
#
import urequests
import machine
import time
import gc
from local_version import version as local_version
import test_ota

def get_remote_version():
    try:
        r = urequests.get("http://raw.githubusercontent.com/saptowahyusudrajat/ESP32_OTA/main/version.json")
        remote_version = r.json().get("version")
        r.close()
        return remote_version
    except Exception as e:
        print("Error getting remote version:", e)
        return None

def download_and_update():
    try:
        r = urequests.get("http://raw.githubusercontent.com/saptowahyusudrajat/ESP32_OTA/main/test_ota.py")
        with open("test_ota.py", "w") as f:
            f.write(r.text)
        r.close()

        with open("local_version.py", "w") as f:
            f.write(f"version = {get_remote_version()}\n")

        print("Update applied. Rebooting...")
        time.sleep(2)
        machine.reset()
    except Exception as e:
        print("Failed to update:", e)

def check_and_run_ota():
    remote_version = get_remote_version()
    if remote_version and remote_version > local_version:
        print(f"New version {remote_version} found.")
        download_and_update()
    else:
        print("No new update.")

# Main loop: Run user logic and check OTA every 1 hour
last_ota_check = time.time()
while True:
    test_ota.loop()          # run the user loop once
    gc.collect()             # cleanup memory
    # Check every hour (or change to shorter time)
    
    now = time.time()
    if now - last_ota_check >= 10:
        check_and_run_ota()
        last_ota_check = now
