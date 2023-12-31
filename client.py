import socket
import cv2
import pickle
import struct
import os
import threading


def sendImage():
    os.system('python3 server.py')

t1 = threading.Thread(target=sendImage)
t1.start()

#Create Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.29.122'
port = 9999
client_socket.connect((host_ip, port))
data = b""
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        # 8K bytes
        packet = client_socket.recv(8 * 1024)
        if not packet: break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(8 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("RECEVING VIDEO ", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

client_socket.close()
