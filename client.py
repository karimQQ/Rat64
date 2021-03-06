import socket
import struct
import pickle
import time
import threading
import numpy
import pyautogui
from PIL import Image

client = socket.socket()
client.connect(("10.18.0.144", 1234))

w, h = pyautogui.size()

client.send(struct.pack("l", w))
client.send(struct.pack("l", h))

data = b''


def send_screen():
    while True:
        frame = pyautogui.screenshot()
        frame = numpy.array(frame)
        frame = Image.fromarray(frame)
        frame = frame.resize((640, 360), Image.ANTIALIAS)
        frame = numpy.array(frame)

        data1 = pickle.dumps(frame)

        # Send message length first
        message_size = struct.pack("L", len(data1))

        # Then data
        client.sendall(message_size + data1)
        time.sleep(0.25)


def read_int(f: str):
    global data
    payload_size = struct.calcsize(f)
    while len(data) < payload_size:
        data += client.recv(1024)
    ans = data[:payload_size]
    data = data[payload_size:]
    try:
        ans = struct.unpack(f, ans)[0]
    except struct.error:
        print(f)
    return ans


def read_commands():
    while True:
        cmd = read_int("b")
        if cmd == 1:
            btn = read_int("b")
            x = read_int("h")
            y = read_int("h")
            pyautogui.moveTo(x, y)
            if btn == 1:
                pyautogui.click()
            elif btn == 2:
                pyautogui.click(button='middle')
            elif btn == 3:
                pyautogui.click(button='right')
        elif cmd == 2:
            key = chr(read_int("h"))
            if key == ' ':
                pyautogui.press("Space")
            else:
                pyautogui.press(key)


t1 = threading.Thread(target=send_screen)
t2 = threading.Thread(target=read_commands)
t1.start()
t2.start()
t1.join()
t2.join()
