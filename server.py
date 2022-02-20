import socket
import pygame
import struct
import time

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

wind = pygame.display.set_mode((1080, 720))

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            connect.close()
            server.close()
            exit(0)
        if i.type == pygame.MOUSEMOTION:
            x, y = i.pos[0], i.pos[1]
            x *= client_width
            x //= w
            y *= client_height
            y //= h
            connect.send(struct.pack("h", 0))
            connect.send(struct.pack("h", x))
            connect.send(struct.pack("h", y))
    time.sleep(0.1)