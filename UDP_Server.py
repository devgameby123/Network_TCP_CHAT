import socket
import threading

# ฟังก์ชันสำหรับการจัดการการสื่อสารกับไคลเอ็นต์


def handle_client(client_socket, client_address):
    while True:
        try:
            # รับข้อมูลจากไคลเอ็นต์
            data, _ = client_socket.recvfrom(1024)
            if not data:
                break
            message = data.decode("utf-8")
            print(
                f"รับข้อมูลจาก {client_address[0]}:{client_address[1]}: {message}")

            # ส่งข้อความไปยังไคลเอ็นต์ทั้งหมดยกเว้นผู้ส่ง
            for client in clients:
                if client != client_socket:
                    client_socket.sendto(data, client_address)
        except:
            break

    # ปิดการเชื่อมต่อของไคลเอ็นต์
    print(f"การเชื่อมต่อจาก {client_address[0]}:{client_address[1]} ปิดแล้ว")
    clients.remove(client_socket)
    client_socket.close()


# การตั้งค่าของเซิร์ฟเวอร์
HOST = "localhost"
PORT = 12345

# สร้าง socket สำหรับเซิร์ฟเวอร์โปรโตคอล UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

# รายการเก็บไคลเอ็นต์ที่เชื่อมต่อ
clients = []

print("UDP Chat Server กำลังทำงาน...")

# ลูปหลักสำหรับรับและจัดการการเชื่อมต่อไคลเอ็นต์
while True:
    # รับข้อมูลจากไคลเอ็นต์
    client_data, client_address = server_socket.recvfrom(1024)
    if client_data:
        # ตรวจสอบว่าไคลเอ็นต์ต้องการปิดการเชื่อมต่อหรือไม่
        if client_data == b'exit':
            break
        # เพิ่มไคลเอ็นต์ในรายการถ้ายังไม่มีอยู่ในรายการ
        if client_data not in clients:
            clients.append(client_data)
            print(
                f"การเชื่อมต่อจาก {client_address[0]}:{client_address[1]} ได้เริ่มต้น")
            # สร้างเธรดเพื่อจัดการไคลเอ็นต์
            client_handler = threading.Thread(
                target=handle_client, args=(server_socket, client_address))
            client_handler.start()
