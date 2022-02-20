import socket
import struct
import pickle
import time
import asyncio
import numpy
import pyautogui

client = socket.socket()
client.connect(("192.168.0.110", 1234))

w, h = pyautogui.size()

client.send(struct.pack("l", w))
client.send(struct.pack("l", h))

data = b''


async def send_screen():
    while True:
        frame = pyautogui.screenshot()
        frame = numpy.array(frame)
        data1 = pickle.dumps(frame)

        # Send message length first
        message_size = struct.pack("L", len(data1))

        # Then data
        client.sendall(message_size + data1)
        time.sleep(1)


asyncio.run(send_screen())


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
