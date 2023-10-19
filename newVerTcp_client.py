import socket
import threading

# สร้าง socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# กำหนด IP address และ port ของ server
SERVER_IP = '0.tcp.ap.ngrok.io'  # หรือ IP address ของ server จริง
SERVER_PORT = 14016

# เชื่อมต่อกับ server
client_socket.connect((SERVER_IP, SERVER_PORT))


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            break


# รับชื่อจากผู้ใช้
username = input("กรุณาใส่ชื่อของคุณ: ")
client_socket.send(username.encode('utf-8'))

# เริ่ม thread ในการรับข้อมูลจาก server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    message = input()
    client_socket.send(message.encode('utf-8'))
