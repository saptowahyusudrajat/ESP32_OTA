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


#WORK WELL BUT MAIN LOOP IN TEST_OTA INTERUPTED
# import urequests
# import machine
# import time
# import gc
# from local_version import version as local_version
# import test_ota
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
#         print("Update applied. Rebooting...")
#         time.sleep(2)
#         machine.reset()
#     except Exception as e:
#         print("Failed to update:", e)
# 
# def check_and_run_ota():
#     remote_version = get_remote_version()
#     if remote_version and remote_version > local_version:
#         print(f"New version {remote_version} found.")
#         download_and_update()
#     else:
#         print("No new update.")
# 
# # Main loop: Run user logic and check OTA every 10 seconds
# last_ota_check = time.time()
# while True:
#     test_ota.loop()          # run the user loop once
#     gc.collect()             # cleanup memory
#     # Check every hour (or change to shorter time)
#     
#     now = time.time()
#     if now - last_ota_check >= 10:
#         check_and_run_ota()
#         last_ota_check = now


import uasyncio as asyncio
import gc
from local_version import version as local_version
import test_ota
import urequests
import machine

async def check_and_run_ota():
    while True:
        try:
            r = urequests.get("http://raw.githubusercontent.com/saptowahyusudrajat/ESP32_OTA/main/version.json")
            remote_version = r.json().get("version")
            r.close()
            if remote_version and remote_version > local_version:
                print(f"New version {remote_version} found. Updating...")
                await download_and_update()
            else:
                print("No New Update")
        except Exception as e:
            print("OTA check failed:", e)
        await asyncio.sleep(10)  # Wait 10 seconds (adjustable)

async def download_and_update():
    try:
        r = urequests.get("http://raw.githubusercontent.com/saptowahyusudrajat/ESP32_OTA/main/test_ota.py")
        with open("test_ota.py", "w") as f:
            f.write(r.text)
        r.close()

        # Update local_version
        r = urequests.get("http://raw.githubusercontent.com/saptowahyusudrajat/ESP32_OTA/main/version.json")
        with open("local_version.py", "w") as f:
            f.write(f"version = {r.json().get('version')}")
        r.close()

        print("Updated. Rebooting...")
        await asyncio.sleep(2)
        machine.reset()
    except Exception as e:
        print("Update failed:", e)

async def run_user_loop():
    while True:
        test_ota.loop()
        gc.collect()
        await asyncio.sleep(0)  # yield to other tasks

async def main():
    await asyncio.gather(
        run_user_loop(),
        check_and_run_ota()
    )

# Entry point
asyncio.run(main())
