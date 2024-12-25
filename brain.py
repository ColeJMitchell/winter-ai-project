import socket
import time

# Connects to the server set up on Windows from WSL to send data to the Arduino
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('windows ip', 5000))
    print("Connected to server")
    
    while True:
        message = b'1-0|5-0|9-20\n'
        client.send(message)
        time.sleep(5)

    client.close()

if __name__ == "__main__":
    main()