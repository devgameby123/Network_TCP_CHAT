import socket
import threading

# รับข้อมูล IP และ Port ของเซิร์ฟเวอร์ที่ต้องการเชื่อมต่อ
ip_connect = input("กรุณาใส่ IP: ")
port_connect = input("กรุณาใส่ Port: ")

# สร้าง socket สำหรับเชื่อมต่อเซิร์ฟเวอร์แบบ TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip_connect, int(port_connect)))

# รับชื่อเล่นของผู้ใช้งาน
nickname = input("กรุณาใส่ชื่อเล่น: ")

# ฟังก์ชันสำหรับรับข้อความที่ถูกส่งมาจากเซิร์ฟเวอร์


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            # ถ้าข้อความที่ได้รับเป็น 'NICK' ให้ส่งชื่อเล่นของผู้ใช้งานไป
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)

        except:
            print('เกิดข้อผิดพลาด!')
            client.close()
            break

# ฟังก์ชันสำหรับการส่งข้อความไปยังเซิร์ฟเวอร์


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


# เริ่มเธรดสำหรับรับข้อความ
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# เริ่มเธรดสำหรับการส่งข้อความ
write_thread = threading.Thread(target=write)
write_thread.start()
