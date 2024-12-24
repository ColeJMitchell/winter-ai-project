import socket
import time

# Connects to the server set up on Windows from WSL to send data to the Arduino
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('windows ip', 5000))
    print("Connected to server")
    
    while True:
        message = b'1'
        client.send(message)
        response = client.recv(1024)
        print(f"Arduino Says: {response}")    
        time.sleep(1)

    client.close()

if __name__ == "__main__":
    main()