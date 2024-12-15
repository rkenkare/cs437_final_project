from utils.general import LOGGER
from picamera2 import Picamera2
from datetime import datetime
import socket
import subprocess
import shutil
import os

def detection():
	LOGGER.info("Cafeteria Checkout")
	subprocess.run(["python3", "detect.py"], check=True)
	LOGGER.info("Program ended")

def start_server(host='192.168.88.191', port=12345):
    LOGGER.info("Scan your ID")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # Listen for one connection
    
    print(f"Server listening on {host}:{port}")
    conn, addr = server_socket.accept()  # Accept a connection
    print(f"Connection from {addr}")
    
    data = conn.recv(1024)  # Receive up to 1024 bytes
    try:
        data = data.decode('utf-8')
        print(f"Message received: {data}")
    except UnicodeDecodeError:
        LOGGER.error("Failed to decode data")
        data = "unknown_data"
		
    conn.close()  # Close the connection
    server_socket.close()
	
    return data

def take_picture(data):
    picam2 = Picamera2()
    try:
        picam2.start()
        time = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_data = "".join([c if c.isalnum() else "_" for c in data]).replace(" ", "")
        output_dir = "data/images"
        os.makedirs(output_dir, exist_ok=True)
        img_name = os.path.join(output_dir, f"transaction_{time}_{safe_data}.jpg")
        picam2.capture_file(img_name)
    finally:
        picam2.stop()
    return img_name

def remove_img(img_name):
	if os.path.exists(img_name):
		os.remove(img_name)
		print("File has been deleted")
	else:
		print("File does not exist")
		
	if os.path.exists("exp"):
		shutil.rmtree("exp")
		print("Folder has been deleted")
	else:
		print("Folder does not exist")
	
	

if __name__ == "__main__":
    data = start_server()
    img_name = take_picture(data)
    detection()
    remove_img(img_name)
