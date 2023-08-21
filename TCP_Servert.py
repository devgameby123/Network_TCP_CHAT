import threading
import socket

# กำหนดข้อมูลเซิร์ฟเวอร์
host = '25.50.17.169'
port = 54321

# สร้าง socket สำหรับเซิร์ฟเวอร์แบบ TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# รายชื่อผู้เชื่อมต่อและชื่อเล่นของผู้ใช้งาน
clients = []
nicknames = []


# ฟังก์ชันสำหรับการส่งข้อความไปยังผู้ใช้งานทั้งหมด
def broadcast(message):
    for client in clients:
        client.send(message)


# ฟังก์ชันสำหรับการจัดการการสนทนาของแต่ละผู้ใช้งาน
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} ออกจากแชท!'.encode('utf-8'))
            nicknames.remove(nickname)
            break


# ฟังก์ชันสำหรับรอรับการเชื่อมต่อจากผู้ใช้งาน
def receive():
    while True:
        client, address = server.accept()
        print(f"เชื่อมต่อกับ {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'ชื่อเล่นของผู้ใช้งาน: {nickname}')
        broadcast(f"{nickname} เข้าร่วมแชท".encode('utf-8'))
        client.send('เชื่อมต่อกับเซิร์ฟเวอร์แล้ว'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server Runnig......")
receive()
