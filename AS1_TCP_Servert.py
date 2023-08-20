import threading
import socket

host = '0.0.0.0'
port = 54321

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = client.index(client)
            client.remove(client)
            client.close()
            nicknames = nicknames[index]
            broadcast(f'{nicknames} left the chat!'.encode('ascii'))
            nicknames.remove(nicknames)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nick Name of the client is {nickname}')
        broadcast(f"{nickname} join the chat".encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening.....")
receive()


# asdasdsa
