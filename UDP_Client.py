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


# การตั้งค่าเซิร์ฟเวอร์และพอร์ต
HOST = "25.50.17.169"
PORT = 54321

# สร้าง socket สำหรับไคลเอ็นต์แบบ UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# รับชื่อผู้ใช้จากผู้ใช้งาน
client_name = input("ป้อนชื่อของคุณ: ")
# ส่งชื่อผู้ใช้ไปยังเซิร์ฟเวอร์
client_socket.sendto(client_name.encode("utf-8"), (HOST, PORT))

# เริ่มเธรดสำหรับรับข้อความจากเซิร์ฟเวอร์
receive_thread = threading.Thread(
    target=receive_messages, args=(client_socket,))
receive_thread.start()

print("พิมพ์ 'exit' เพื่อออกจากแชท\n")

# ลูปหลักสำหรับส่งข้อความ
while True:
    message = input()
    if message == 'exit':
        # ส่งข้อความ 'exit' เพื่อแจ้งให้เซิร์ฟเวอร์ทราบว่าต้องการออกจากแชท
        client_socket.sendto(message.encode("utf-8"), (HOST, PORT))
        break
    # ส่งข้อความที่ผู้ใช้ป้อนไปยังเซิร์ฟเวอร์
    client_socket.sendto(
        f"{client_name}: {message}".encode("utf-8"), (HOST, PORT))

# ปิดการเชื่อมต่อเมื่อเสร็จสิ้นการใช้งาน
client_socket.close()
