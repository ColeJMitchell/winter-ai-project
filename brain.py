import socket
import time
import struct
import pickle
import cv2
import numpy as np

# Connects to the server set up on Windows from WSL to send data to the Arduino
def main():
    #client_motors = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_motors.connect(('windows ip', 5000))
    client_vision = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_vision.connect(('windows ip', 5001))
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
            '''
            frame_filename = f"/home/cole/github/winter-ai-project/frames/frame_{frame_count}.jpg"
            cv2.imwrite(frame_filename, frame)
            frame_count += 1
            '''
            canny = cv2.Canny(frame, 50, 150)
            hough = cv2.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10) 
            if hough is not None:
                for line in hough:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.imshow("frame", frame)
    #message = b'1-0|5-0|9-20\n'
    #client_motors.send(message)

    client_motors.close()

if __name__ == "__main__":
    main()