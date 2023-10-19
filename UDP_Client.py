import socket
import threading

# ฟังก์ชันสำหรับรับข้อความจากเซิร์ฟเวอร์


def receive_messages(client_socket):
    while True:
        try:
            data, _ = client_socket.recvfrom(1024)
            print("\n" + data.decode("utf-8"))
        except:
            break

# ฟังก์ชันสำหรับส่งข้อความ


def send_messages(client_socket, client_name, server_address):
    while True:
        try:
            message = input("input you Text: ")
            if message == 'exit':
                client_socket.sendto(message.encode("utf-8"), server_address)
                break
            client_socket.sendto(
                f"{client_name}: {message}".encode("utf-8"), server_address)
        except:
            break


# การตั้งค่าเซิร์ฟเวอร์และพอร์ต
HOST = "16.ip.gl.ply.gg"
PORT = 9502

# สร้าง socket สำหรับไคลเอ็นต์แบบ UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# รับชื่อผู้ใช้จากผู้ใช้งาน
client_name = input("ป้อนชื่อของคุณ: ")
client_socket.sendto(client_name.encode("utf-8"), (HOST, PORT))

# เริ่มเธรดสำหรับรับข้อความจากเซิร์ฟเวอร์
receive_thread = threading.Thread(
    target=receive_messages, args=(client_socket,))
receive_thread.start()

send_messages(client_socket, client_name, (HOST, PORT))

client_socket.close()
