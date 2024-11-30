import socket
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

def send_rfid_data(rfid_id, server_ip, server_port):
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server_ip, server_port)
        print(f"Connecting to {server_ip}:{server_port}")
        sock.connect(server_address)

        try:
            # Send data
            message = str(rfid_id)
            print(f"Sending RFID ID: {message}")
            sock.sendall(message.encode('utf-8'))
        finally:
            sock.close()
    except Exception as e:
        print(f"Failed to send RFID data: {e}")

def main():
    reader = SimpleMFRC522()
    server_ip = '192.168.1.100'  # Replace with Raspberry Pi 5 IP address
    server_port = 65432  # Port number to match the server

    try:
        while True:
            print("Place your RFID card near the reader")
            rfid_id, text = reader.read()
            print(f"RFID ID read: {rfid_id}")
            send_rfid_data(rfid_id, server_ip, server_port)
            time.sleep(2)  # Delay before next read
    except KeyboardInterrupt:
        print("Exiting RFID reader")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()