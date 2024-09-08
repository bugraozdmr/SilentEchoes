from colorama import Fore
from cryptography.fernet import Fernet
import threading

clients = []

def handle_client(client_socket, addr,cipher,user):
    print(f"Connection success: {addr}")
    try:
        while True:
            encrypted_response = client_socket.recv(1024)
            if not encrypted_response:
                print(f"Connection closed by {addr}.")
                break
            response = cipher.decrypt(encrypted_response).decode()
            print(f"\r{response}\n{user} : ", end="")
    except Exception as e:
        print(f"{Fore.RED}Error while receiving message: {e}{Fore.RED}{Fore.RESET}")
    finally:
        client_socket.close()
        if client_socket in clients:
            clients.remove(client_socket)

def accept_connections(server_socket,cipher,user):
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        client_handler_thread = threading.Thread(target=handle_client, args=(client_socket, addr,cipher,user))
        client_handler_thread.start()

def send_messages(user,cipher):
    while True:
        try:
            user_input = input(f"{user}: ") or user
            message = f"{user} : {user_input}"
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