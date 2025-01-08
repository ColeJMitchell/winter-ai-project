import socket
import struct
import pickle
import cv2
import numpy as np
from square import square

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

'''
Dead Code
# Filters out points that are too close to each other
def distance(points, threshold):
    try:
        filtered = []
        while len(filtered) != 81 and points:
            x, y = points[0]
            for i in range(len(points) - 1, 0, -1):  
                x2, y2 = points[i]
                if abs(x2 - x) < threshold and abs(y2 - y) < threshold:
                    points.pop(i)  
            filtered.append(points.pop(0))  
        return filtered
    except Exception as e:
        print(e)
'''
# Initializes the chess board based on the square coordinates
def initBoard():
    squares = []
    counter = 1
    coordinates = [
        ((517, 640), (26, 140)), ((521, 644), (139, 253)), ((524, 647), (252, 366)), ((525, 648), (364, 478)),
        ((529, 652), (472, 586)), ((529, 652), (580, 696)), ((530, 653), (690, 804)), ((533, 656), (799, 913)),
        ((628, 751), (24, 138)), ((630, 753), (137, 252)), ((635, 758), (251, 365)), ((635, 758), (366, 480)),
        ((640, 763), (474, 588)), ((640, 763), (584, 698)), ((643, 766), (692, 806)), ((643, 766), (799, 913)),
        ((740, 863), (22, 136)), ((743, 866), (137, 241)), ((744, 867), (251, 365)), ((748, 871), (363, 477)),
        ((748, 871), (472, 586)), ((750, 873), (582, 696)), ((750, 873), (688, 802)), ((750, 873), (798, 912)),
        ((856, 979), (24, 138)), ((856, 979), (138, 252)), ((856, 979), (250, 364)), ((856, 979), (362, 476)),
        ((856, 979), (474, 588)), ((858, 981), (582, 696)), ((858, 981), (690, 804)), ((858, 981), (798, 912)),
        ((967, 1090), (24, 138)), ((967, 1090), (138, 252)), ((967, 1090), (252, 366)), ((967, 1090), (362, 476)),
        ((967, 1090), (472, 586)), ((967, 1090), (582, 696)), ((967, 1090), (690, 804)), ((967, 1090), (796, 910)),
        ((1080, 1203), (24, 138)), ((1080, 1203), (137, 251)), ((1080, 1203), (251, 365)), ((1076, 1199), (364, 478)),
        ((1076, 1199), (473, 587)), ((1076, 1199), (581, 695)), ((1073, 1196), (689, 803)), ((1073, 1196), (793, 907)),
        ((1193, 1316), (24, 138)), ((1188, 1311), (138, 252)), ((1188, 1311), (252, 366)), ((1188, 1311), (364, 478)),
        ((1183, 1306), (473, 587)), ((1183, 1306), (582, 696)), ((1183, 1306), (688, 802)), ((1183, 1306), (794, 908)),
        ((1302, 1425), (26, 140)), ((1302, 1425), (140, 254)), ((1300, 1423), (254, 368)), ((1297, 1420), (364, 478)),
        ((1294, 1417), (473, 587)), ((1291, 1414), (581, 695)), ((1288, 1411), (688, 802)), ((1285, 1408), (685, 799))
    ]
    for coords in coordinates:
        squares.append(square(coords[0], coords[1], counter))
        counter += 1
    return squares

# Connects to the server and processes the video feed
def main():
    try:
        client_vision = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client_vision.connect(('windows ip', 5001))
        data_size = struct.calcsize("Q")
        while True:
            try:
                result = receive_frame(client_vision, data_size)
                squares = result.copy()
                '''
                Dead Code
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
                for hlines in horizontal:
                    for vlines in vertical:
                        x1, y1, x2, y2 = hlines
                        x3, y3, x4, y4 = vlines
                        px, py = findIntersection(x1, y1, x2, y2, x3, y3, x4, y4)
                        cv2.circle(frame, (int(px), int(py)) ,5 ,(0, 0, 255), 5)
                frame = frame[30:930, 638:1567]
                '''
                cv2.imshow("frame", squares)
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