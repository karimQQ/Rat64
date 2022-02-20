import socket
import struct

import pyautogui

client = socket.socket()
client.connect(("192.168.0.110", 1234))

payload_size = struct.calcsize("h")

w, h = pyautogui.size()

client.send(struct.pack("l", w))
client.send(struct.pack("l", h))

data = b''


def read_int():
    global data
    while len(data) < payload_size:
        data += client.recv(1024)
    ans = data[:payload_size]

    data = data[payload_size:]
    ans = struct.unpack("h", ans)[0]
    return ans


while True:
    cmd = read_int()
    if cmd == 0:
        x = read_int()
        y = read_int()
        pyautogui.moveTo(x, y)
