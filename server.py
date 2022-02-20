import socket
import pygame
import struct
import time
import cv2
import pickle
import threading

server = socket.socket()
server.bind(("192.168.0.110", 1234))
server.listen(1)
connect, address = server.accept()

payload_size = struct.calcsize("l")

data = b''

while len(data) < payload_size:
    data += connect.recv(1024)

client_width = data[:payload_size]
client_width = struct.unpack("L", client_width)[0]
data = data[payload_size:]

while len(data) < payload_size:
    data += connect.recv(1024)

client_height = data[:payload_size]
client_height = struct.unpack("L", client_height)[0]
data = data[payload_size:]

w, h = 1080, 720

print(client_width, client_height)


def read_screen():
    data1 = b''
    while True:
        while len(data1) < payload_size:
            data1 += connect.recv(4096)

        packed_msg_size = data1[:payload_size]
        data1 = data1[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        # Retrieve all data based on message size
        while len(data1) < msg_size:
            data1 += connect.recv(4096)

        frame_data = data1[:msg_size]
        data1 = data1[msg_size:]

        # Extract frame
        frame = pickle.loads(frame_data)

        # Display
        cv2.imshow('frame', frame)
        cv2.waitKey(1)


def send_commands():
    wind = pygame.display.set_mode((1080, 720))
    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                connect.close()
                server.close()
                exit(0)
            if i.type == pygame.MOUSEBUTTONDOWN:
                connect.send(struct.pack("b", 1))
                connect.send(struct.pack("b", i.button))
                x, y = i.pos[0], i.pos[1]
                x *= client_width
                x //= w
                y *= client_height
                y //= h
                connect.send(struct.pack("h", x))
                connect.send(struct.pack("h", y))
        time.sleep(0.1)


t1 = threading.Thread(target=read_screen)
t2 = threading.Thread(target=send_commands)
t1.start()
t2.start()
t1.join()
t2.join()
