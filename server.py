import socket
import numpy
import pygame
import struct
import pickle
from PIL import Image

server = socket.socket()
server.bind(("192.168.244.232", 1234))
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

w, h = 1280, 720

print(client_width, client_height)
wind = pygame.display.set_mode((w, h))

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
        if i.type == pygame.KEYDOWN:
            k = i.key
            key = 0
            if k == pygame.K_a:
                key = 'a'
            elif k == pygame.K_b:
                key = 'b'
            elif k == pygame.K_c:
                key = 'c'
            elif k == pygame.K_d:
                key = 'd'
            elif k == pygame.K_e:
                key = 'e'
            elif k == pygame.K_f:
                key = 'f'
            elif k == pygame.K_g:
                key = 'g'
            elif k == pygame.K_h:
                key = 'h'
            elif k == pygame.K_i:
                key = 'i'
            elif k == pygame.K_j:
                key = 'j'
            elif k == pygame.K_k:
                key = 'k'
            elif k == pygame.K_l:
                key = 'l'
            elif k == pygame.K_m:
                key = 'm'
            elif k == pygame.K_n:
                key = 'n'
            elif k == pygame.K_o:
                key = 'o'
            elif k == pygame.K_p:
                key = 'p'
            elif k == pygame.K_q:
                key = 'q'
            elif k == pygame.K_r:
                key = 'r'
            elif k == pygame.K_s:
                key = 's'
            elif k == pygame.K_t:
                key = 't'
            elif k == pygame.K_u:
                key = 'u'
            elif k == pygame.K_v:
                key = 'v'
            elif k == pygame.K_w:
                key = 'w'
            elif k == pygame.K_x:
                key = 'x'
            elif k == pygame.K_y:
                key = 'y'
            elif k == pygame.K_z:
                key = 'z'
            elif k == pygame.K_SPACE:
                key = ' '
            if key != 0:
                key = ord(key)
                connect.send(struct.pack("b", 2))
                connect.send(struct.pack("h", key))
    while len(data) < payload_size:
        data += connect.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    # Retrieve all data based on message size
    while len(data) < msg_size:
        data += connect.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Extract frame
    frame = pickle.loads(frame_data)

    img = Image.fromarray(frame)

    img = img.resize((w, h), Image.ANTIALIAS)

    # Display
    img = numpy.array(img)
    img = numpy.rot90(img)
    img = numpy.flipud(img)
    img = pygame.surfarray.make_surface(img)
    wind.blit(img, (0, 0))
    pygame.display.update()
