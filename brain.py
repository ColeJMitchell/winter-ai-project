import socket
import time

# Connects to the server set up on Windows from WSL to send data to the Arduino
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('windows ip', 5000))
    print("Connected to server")
    
    while True:
        servo_channel = input("Enter the servo channel: ")
        angle = input("Enter the angle: ")
        message = f'{servo_channel}-{angle}'.encode('utf-8')
        client.send(message)

    client.close()

if __name__ == "__main__":
    main()