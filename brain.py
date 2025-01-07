import socket
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

# Finds the intersection points of the vertical and horizontal lines
def findIntersection(x1,y1,x2,y2,x3,y3,x4,y4):
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
    return px, py

# Filters out points that are too close to each other
def distance(points, threshold):
    filtered = []
    while len(filtered) != 81:
        x, y = points[0]
        for i in range(len(points) - 1, 0, -1):  
            x2, y2 = points[i]
            if abs(x2 - x) < threshold and abs(y2 - y) < threshold:
                points.pop(i)  
        filtered.append(points.pop(0))  
    return filtered



# Connects to the server and processes the video feed
def main():
    try:
        client_vision = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client_vision.connect(('windows ip', 5001))
        data_size = struct.calcsize("Q")
        while True:
            try:
                result = receive_frame(client_vision, data_size)
                frame = result
                result = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
                result = cv2.GaussianBlur(result, (5, 5), 0)  
                ones = np.ones((9, 9), np.uint8)
                canny = cv2.Canny(result, 50, 100)
                dilated = cv2.dilate(canny, ones, iterations=1)
                hough = cv2.HoughLinesP(dilated, 1, np.pi/180, 100, minLineLength=650, maxLineGap=30)
                vertical = []
                horizontal = []
                if hough is not None:
                    for line in hough:
                        x1, y1, x2, y2 = line[0]
                        #cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                        if abs(x2 - x1) > abs(y2 - y1):
                            horizontal.append((x1, y1, x2, y2))
                            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                        if abs(y2-y1) > abs(x2 - x1):
                            vertical.append((x1, y1, x2, y2))
                            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)
                points = []
                for hlines in horizontal:
                    for vlines in vertical:
                        x1, y1, x2, y2 = hlines
                        x3, y3, x4, y4 = vlines
                        px, py = findIntersection(x1, y1, x2, y2, x3, y3, x4, y4)
                        cv2.circle(frame, (int(px), int(py)), 5, (0, 0, 255), 5)
                        points.append((int(px), int(py)))
                frame = frame[30:930, 638:1567]
                filtered = distance(points, 50)
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