import serial
import socket
import time

#Python script for Windows that bridges the serial connection between the Arduino and WSL
def main():
    ser = serial.Serial('COM3', 115200, timeout=1)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(1) 
    conn, addr = server.accept()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        ser.write(data)
        response = ser.read(20)
        print(f"Arduino response: {response}")
        conn.send(response if response else b'no_response')
    ser.close() 
    conn.close() 

if __name__ == "__main__":
    main()