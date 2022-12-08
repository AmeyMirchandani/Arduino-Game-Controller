import asyncio
import bleak
import time
import mouse
import struct
from pynput import keyboard
from pynput.keyboard import Controller
import keyboard as k

target_device = "Halo-Controller"

kbd = Controller()
mousePressed = False
currently_pressed_key = -1

async def main():    
    
    print("Searching for devices...")

    scanner = bleak.BleakScanner()
    await scanner.start()
    time.sleep(5)
    await scanner.stop()
    devices = scanner.discovered_devices

    for device in devices:
        if target_device == device.name:
            print(f"Found device: {device.name} with address: {device.address}")

            async with bleak.BleakClient(device.address) as client:
                print(f"Connected to {client.address}")
                #print("Services Available:")

                services = client.services
                proxChar = services.get_characteristic("00002AA4-0000-1000-8000-00805f9b34fb")
                gyroXChar = services.get_characteristic("00002AA3-0000-1000-8000-00805f9b34fb")
                gyroYChar = services.get_characteristic("00002AA5-0000-1000-8000-00805f9b34fb")
                gyroZChar = services.get_characteristic("00002AA6-0000-1000-8000-00805f9b34fb")
                pitchChar = services.get_characteristic("00002AA1-0000-1000-8000-00805f9b34fb")
                rollChar = services.get_characteristic("00002AA2-0000-1000-8000-00805f9b34fb")
                gestureChar = services.get_characteristic("00002AA7-0000-1000-8000-00805f9b34fb")

                #await client.start_notify(proxChar, proxCallback)
                #await client.start_notify(gyroXChar, gyroXCallback)
                #await client.start_notify(pitchChar, pitchCallback)
                await client.start_notify(gestureChar, gestureCallback)
                
                '''
                proxData = await client.read_gatt_char(proxChar)
                proxData = int.from_bytes(proxData, "big")
                print(f"Proximity Value: {proxData}")
                '''

                await asyncio.sleep(20)
            break

def printAvailableServicesInfo(services):
    for service in services:
        print("--------------------------------------")
        print(f"Service UUID: {service.uuid}")
        for chars in service.characteristics:
            print(f"Characteristic UUID: {chars.uuid}")

def gestureCallback(sender, data: bytearray):
    key = int.from_bytes(data, "little")

    previously_pressed_key = currently_pressed_key
    releaseKey(currently_pressed_key) #release currently pressed key

    if key != previously_pressed_key: #if same key was not pressed
        pressKey(key) #press new key

def pitchCallback(sender, data: bytearray):
    data = int.from_bytes(data, "little", signed=True)
    print(data)

def gyroXCallback(sender, data: bytearray):
    data = struct.unpack("f", data)
    print(data[0])

def proxCallback(sender, data: bytearray):
    global mousePressed
    if mousePressed == False:
        mouse.press(button="left")
        mousePressed = True
    else:
        mouse.release(button="left")
        mousePressed = False

def pressKey(key):
    global currently_pressed_key
    if key == 0:
        #kbd.press("w")
        k.press("shift")
        currently_pressed_key = 0
    elif key == 1:
        #kbd.press("s")
        k.press("alt")
        currently_pressed_key = 1
    elif key == 2:
        #kbd.press("a")
        k.press("left ctrl")
        currently_pressed_key = 2
    elif key == 3:
        #kbd.press("d")
        k.press("right ctrl")
        currently_pressed_key = 3

def releaseKey(key):
    global currently_pressed_key
    if key == 0:
        #kbd.release("w")
        k.release("shift")
        currently_pressed_key = -1
    elif key == 1:
        #kbd.release("s")
        k.release("alt")
        currently_pressed_key = -1
    elif key == 2:
        #kbd.release("a")
        k.release("left ctrl")
        currently_pressed_key = -1
    elif key == 3:
        #kbd.release("d")
        k.release("right ctrl")
        currently_pressed_key = -1

if __name__ == "__main__":
    asyncio.run(main())