import serial
import socket
import time

#Python script for windows that bridges the serial connection between the Arduino and WSL
def main():
    ser = serial.Serial('COM3', 250000 , timeout=1)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(1) 
    conn, _ = server.accept()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        ser.write(data)
    ser.close() 
    conn.close() 

if __name__ == "__main__":
    main()