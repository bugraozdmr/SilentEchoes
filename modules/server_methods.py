from colorama import Fore
from cryptography.fernet import Fernet
import threading

# kisi sayisi metodu ile su kadar kisi ile sinirla olabilir musait ekle
# sifreleme eklencek
# boslukları ayarla
# not alıncak istenirse tüm mesajlar txt dosyasına

clients = []
usernames = {}
flag = 2

def handle_client(client_socket, addr, cipher, user, password):
    try:
        print(f"\nConnection attempt from {addr}")
        username_message = client_socket.recv(1024)
            
        username, received_password = [part.split(":")[1] for part in username_message.split(",")]
        
        usernames[client_socket] = username
        
        if password and password != received_password:
            print("Failed password attempt")
            client_socket.close()
            if client_socket in clients:
                clients.remove(client_socket)
            flag = 1
        else :
            notify_message = f"{username} has joined the chat. (Active users {len(clients) + 1})"
            broadcast(cipher.encrypt(notify_message.encode()), None)
            while True:
                encrypted_response = client_socket.recv(1024)
                if not encrypted_response:
                    # \n
                    print(f"\nConnection closed by {addr}.")
                    break
                response = cipher.decrypt(encrypted_response).decode()
                print(f"\n{response}\n{user}: ", end="")
                broadcast(encrypted_response, client_socket)
                
        if flag != 1:
            notify_message = f"{username} has left the chat (Active users {len(clients) + 1})"
            broadcast(cipher.encrypt(notify_message.encode()), None)
            client_socket.close()
            if client_socket in clients:
                clients.remove(client_socket)
            flag = 2
                
    except IndexError:
        # can not add another try except inside or boom
        print(f"Connection from {addr} rejected: Invalid format.")
        client_socket.send(cipher.encrypt(b"Invalid format"))
        client_socket.close()
        return
    except Exception as e:
        print(f"{Fore.RED}Error while receiving message: {e}{Fore.RED}{Fore.RESET}")

def broadcast(message, sender_socket):
    for client_socket in list(clients):
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except BrokenPipeError:
                print(f"{Fore.RED}Error: Broken pipe while broadcasting message.{Fore.RED}{Fore.RESET}")
                client_socket.close()
                if client_socket in clients:
                    clients.remove(client_socket)

def accept_connections(server_socket, cipher, user,password):
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        client_handler_thread = threading.Thread(target=handle_client, args=(client_socket, addr, cipher, user,password))
        client_handler_thread.start()

def send_messages(user, cipher):
    while True:
        try:
            user_input = input(f"{user}: ") or user
            message = f"{user}: {user_input}"
            encrypted_message = cipher.encrypt(message.encode())
            for client_socket in list(clients):
                try:
                    client_socket.send(encrypted_message)
                except BrokenPipeError:
                    print(f"{Fore.RED}Error: Broken pipe while sending message.{Fore.RED}{Fore.RESET}")
                    client_socket.close()
                    if client_socket in clients:
                        clients.remove(client_socket)
        except Exception as e:
            print(f"{Fore.RED}Error while sending message: {e}{Fore.RED}{Fore.RESET}")