import cv2
import socket
import pickle
import struct

# Create a server that sends the video feed from Windows to WSL to be processed by machine learning model
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5001))
    server.listen(1)
    conn, _ = server.accept()
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
    while True:
        _, frame = camera.read()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        data = pickle.dumps(frame)
        message = struct.pack("Q", len(data)) + data
        try:
            conn.sendall(message)
        except:
            camera.release()
            cv2.destroyAllWindows()
            server.close() 
            conn.close() 
            main()
    camera.release()
    cv2.destroyAllWindows()
    server.close() 
    conn.close() 
if __name__ == '__main__':
    main()