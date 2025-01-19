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
    camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)  
    camera.set(cv2.CAP_PROP_FOCUS, 0)  
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) 
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    camera.set(cv2.CAP_PROP_FPS, 60) 
    while True:
        _, frame = camera.read()
        data = pickle.dumps(frame)
        message = struct.pack("Q", len(data)) + data
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
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