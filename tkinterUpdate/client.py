import socket
import cv2
import pickle
import struct
import pyaudio
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = 'SERVER_IP_HERE' 
port = 9999

client_socket.connect((host_ip, port))
data = b""
payload_size = struct.calcsize("Q")

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, output=True,
                    frames_per_buffer=CHUNK)

def video_stream():
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)  
            if not packet: break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

def audio_stream():
    while True:
        data = client_socket.recv(1024)
        stream.write(data)

threading.Thread(target=video_stream).start()
threading.Thread(target=audio_stream).start()
