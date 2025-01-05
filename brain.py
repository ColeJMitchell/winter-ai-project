import socket
import time
import struct
import pickle
import cv2
import numpy as np

# Processes frame data sent from the server's webcam
def receive_frame(client_socket, data_size):
    data = b''
    while len(data) < data_size:
        packet = client_socket.recv(4*1024)
        if not packet:
            return None
        data += packet
    
    packed_msg_size = data[:data_size]
    data = data[data_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        remaining = msg_size - len(data)
        packet = client_socket.recv(min(remaining, 4*1024))
        if not packet:
            return None
        data += packet
    
    frame_data = data[:msg_size]
    frame = pickle.loads(frame_data)
    return frame

# Connects to the server and processes the video feed
def main():
    try:
        client_vision = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        windows_ip = 'windows_ip' 
        client_vision.connect((windows_ip, 5001))
        data_size = struct.calcsize("Q")
        data = b''
        while True:
            try:
                result = receive_frame(client_vision, data_size)
                frame = result     
                canny = cv2.Canny(frame, 50, 150)
                hough = cv2.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
                if hough is not None:
                    for line in hough:
                        x1, y1, x2, y2 = line[0]
                        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
                cv2.imshow("frame", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
            except Exception as e:
                break

    except Exception as e:
        pass
    
    finally:
        cv2.destroyAllWindows()
        client_vision.close()

if __name__ == "__main__":
    main()