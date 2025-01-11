import socket
import struct
import pickle
import cv2
import numpy as np
from square import square
import os 

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
        ((500, 623), (22, 136)), ((510, 633), (139, 253)), ((514, 637), (252, 366)), ((525, 648), (364, 478)),
        ((529, 652), (472, 586)), ((529, 652), (580, 694)), ((530, 653), (690, 804)), ((533, 656), (823, 937)),
        ((628, 751), (24, 138)), ((630, 753), (137, 251)), ((635, 758), (251, 365)), ((635, 758), (366, 480)),
        ((640, 763), (474, 588)), ((640, 763), (584, 698)), ((643, 766), (692, 806)), ((643, 766), (799, 913)),
        ((740, 863), (22, 136)), ((743, 866), (137, 251)), ((744, 867), (251, 365)), ((748, 871), (363, 477)),
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
        ((1294, 1417), (473, 587)), ((1291, 1414), (581, 695)), ((1288, 1411), (688, 802)), ((1295, 1418), (800, 914))
    ]
    for coords in coordinates:
        squares.append(square(coords[0], coords[1], counter))
        counter += 1
    return squares

# Collect training data for the machine learning chess piece classification
def collectData(board, squares):
    board[0].saveImage(squares, "black", "rook", "1,1")
    board[1].saveImage(squares, "black", "knight", "2,1")
    board[2].saveImage(squares, "black", "bishop", "3,1")
    board[3].saveImage(squares, "black", "king", "4,1")
    board[4].saveImage(squares, "black", "queen", "5,1")
    board[5].saveImage(squares, "black", "bishop", "6,1")
    board[6].saveImage(squares, "black", "knight", "7,1")
    board[7].saveImage(squares, "black", "rook", "8,1")
    board[8].saveImage(squares, "black", "pawn", "1,2")
    board[9].saveImage(squares, "black", "pawn", "2,2")
    board[10].saveImage(squares, "black", "pawn", "3,2")
    board[11].saveImage(squares, "black", "pawn", "4,2")
    board[12].saveImage(squares, "black", "pawn", "5,2")
    board[13].saveImage(squares, "black", "pawn", "6,2")
    board[14].saveImage(squares, "black", "pawn", "7,2")
    board[15].saveImage(squares, "black", "pawn", "8,2")
    board[16].saveImage(squares, "empty", "square", "1,3")
    board[17].saveImage(squares, "empty", "square", "2,3")
    board[18].saveImage(squares, "empty", "square", "3,3")
    board[19].saveImage(squares, "empty", "square", "4,3")
    board[20].saveImage(squares, "empty", "square", "5,3")
    board[21].saveImage(squares, "empty", "square", "6,3")
    board[22].saveImage(squares, "empty", "square", "7,3")
    board[23].saveImage(squares, "empty", "square", "8,3")
    board[24].saveImage(squares, "empty", "square", "1,4")
    board[25].saveImage(squares, "empty", "square", "2,4")
    board[26].saveImage(squares, "empty", "square", "3,4")
    board[27].saveImage(squares, "empty", "square", "4,4")
    board[28].saveImage(squares, "empty", "square", "5,4")
    board[29].saveImage(squares, "empty", "square", "6,4")
    board[30].saveImage(squares, "empty", "square", "7,4")
    board[31].saveImage(squares, "empty", "square", "8,4")
    board[32].saveImage(squares, "empty", "square", "1,5")
    board[33].saveImage(squares, "empty", "square", "2,5")
    board[34].saveImage(squares, "empty", "square", "3,5")
    board[35].saveImage(squares, "empty", "square", "4,5")
    board[36].saveImage(squares, "empty", "square", "5,5")
    board[37].saveImage(squares, "empty", "square", "6,5")
    board[38].saveImage(squares, "empty", "square", "7,5")
    board[39].saveImage(squares, "empty", "square", "8,5")
    board[40].saveImage(squares, "empty", "square", "1,6")
    board[41].saveImage(squares, "empty", "square", "2,6")
    board[42].saveImage(squares, "empty", "square", "3,6")
    board[43].saveImage(squares, "empty", "square", "4,6")
    board[44].saveImage(squares, "empty", "square", "5,6")
    board[45].saveImage(squares, "empty", "square", "6,6")
    board[46].saveImage(squares, "empty", "square", "7,6")
    board[47].saveImage(squares, "empty", "square", "8,6")
    board[48].saveImage(squares, "white", "pawn", "1,7")
    board[49].saveImage(squares, "white", "pawn", "2,7")
    board[50].saveImage(squares, "white", "pawn", "3,7")
    board[51].saveImage(squares, "white", "pawn", "4,7")
    board[52].saveImage(squares, "white", "pawn", "5,7")
    board[53].saveImage(squares, "white", "pawn", "6,7")
    board[54].saveImage(squares, "white", "pawn", "7,7")
    board[55].saveImage(squares, "white", "pawn", "8,7")
    board[56].saveImage(squares, "white", "rook", "1,8")
    board[57].saveImage(squares, "white", "knight", "2,8")
    board[58].saveImage(squares, "white", "bishop", "3,8")
    board[59].saveImage(squares, "white", "king", "4,8")
    board[60].saveImage(squares, "white", "queen", "5,8")
    board[61].saveImage(squares, "white", "bishop", "6,8")
    board[62].saveImage(squares, "white", "knight", "7,8")
    board[63].saveImage(squares, "white", "rook", "8,8")

# Collects a row of training data for the machine learning chess piece classification
def collectRowData(board, squares, start, end, color, piece, col):
    counter = 1
    for i in range(start, end+1):
        board[i].saveImage(squares, color, piece, f"{counter},{col}")
        counter += 1    

# Collect 2 data points for the machine learning chess piece classification
def collect2PData(board, squares, start, end, color, piece, col, start2):
    counter = 0
    for i in range(start, end+1):
        board[i].saveImage(squares, color, piece, f"{start2 + counter},{col}")
        counter += 1

# Connects to the server and processes the video feed
def main():
    board = initBoard()
    for square in board:
        square.normalize()
    try:
        client_vision = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        try:
            client_vision.connect((os.getenv("WINDOWS_IP"), 5001))
        except Exception as e:
            print(e)
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
                '''
                for square in board:
                    square.saveImage(squares)
                return
                '''
                collect2PData(board, squares, 62, 63, "black", "rook", 8, 7)
                #collectData(board, squares)
                cv2.imshow("Frame", squares[22:136, 517:640])
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