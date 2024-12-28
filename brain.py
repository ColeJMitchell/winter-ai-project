import socket
import time
import struct
import pickle
import cv2

# Connects to the server set up on Windows from WSL to send data to the Arduino
def main():
    #client_motors = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_motors.connect(('192.168.86.32', 5000))
    client_vision = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_vision.connect(('192.168.86.32', 5001))
    data_size = struct.calcsize("Q")
    data = b''
    frame_count = 0
    while True:
        while len(data) < data_size:
            packet = client_vision.recv(4*1024)
            data += packet
            packed_msg_size = data[:data_size]
            data = data[data_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_vision.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            frame_filename = f"/home/cole/github/winter-ai-project/frames/frame_{frame_count}.jpg"
            cv2.imwrite(frame_filename, frame)
            frame_count += 1
    #message = b'1-0|5-0|9-20\n'
    #client_motors.send(message)

    client_motors.close()

if __name__ == "__main__":
    main()