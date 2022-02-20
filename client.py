import socket
import struct

import pyautogui

client = socket.socket()
client.connect(("192.168.0.110", 1234))

w, h = pyautogui.size()

client.send(struct.pack("l", w))
client.send(struct.pack("l", h))

data = b''


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
        pyautogui.dragTo(x, y)
