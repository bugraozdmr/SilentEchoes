from cryptography.fernet import Fernet
import socket
import modules.read_key as rk
import modules.banner as banner
import modules.get_local_ip as gli
import os
from colorama import Fore
import threading

banner.info()

# Read the key
try:
    key = rk.load_key()
    print(f"{Fore.CYAN}[+]{Fore.CYAN}{Fore.RESET}{Fore.YELLOW} Key upload success{Fore.YELLOW}{Fore.RESET}")
except Exception as e:
    print(f"{Fore.RED}Error: {e}{Fore.RED}{Fore.RESET}")
    exit()
    
cipher = Fernet(key)

# Get the local IP address
try:
    local_ip = gli.get_local_ip()
    print(f"{Fore.CYAN}[+]{Fore.CYAN}{Fore.RESET}{Fore.YELLOW} Local IP Found{Fore.YELLOW}{Fore.RESET}\n")
except Exception as e:
    print(f"{Fore.RED}Error: {e}{Fore.RED}{Fore.RESET}")
    exit()

# Default settings
default_host = local_ip
default_port = 1453

host = default_host
print(f"Host default '{default_host}'")
port_input = input(f"Port (default '{default_port}'): ").strip() or default_port

try:
    port = int(port_input)
except ValueError:
    print(f"{Fore.RED}The input is not a valid integer.{Fore.RED}{Fore.RESET}")
    exit()
except TypeError:
    print(f"{Fore.RED}The input is not of the correct type.{Fore.RED}{Fore.RESET}")
    exit()

print(f"{Fore.CYAN}------------------{Fore.CYAN}{Fore.RESET}\nHost: {host} \nPort: {port}\n{Fore.CYAN}------------------{Fore.CYAN}{Fore.RESET}\n")

room_password = input("Room Password (Optional): ").strip()
if host != default_host:
    print(f"{Fore.RED}Host has to be your local IP address{Fore.RED}{Fore.RESET}")
    exit()

default_user = host
user = input(f"User (default '{default_user}'): ").strip() or default_user

# Create and configure server socket
try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    os.system("clear")
    print("Server started waiting ...")
except Exception as e:
    print(f"{Fore.RED}Error: {e}{Fore.RED}{Fore.RESET}")
    exit()

clients = []

def handle_client(client_socket, addr):
    print(f"Connection success: {addr}")
    try:
        while True:
            encrypted_response = client_socket.recv(1024)
            if not encrypted_response:
                print(f"Connection closed by {addr}.")
                break
            response = cipher.decrypt(encrypted_response).decode()
            print(f"\r{response}\n{user}: ", end="")
    except Exception as e:
        print(f"{Fore.RED}Error while receiving message: {e}{Fore.RED}{Fore.RESET}")
    finally:
        client_socket.close()
        if client_socket in clients:
            clients.remove(client_socket)

def accept_connections():
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        client_handler_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler_thread.start()

def send_messages():
    while True:
        try:
            user_input = input(f"{user}: ") or user
            message = f"{user} : {user_input}"
            encrypted_message = cipher.encrypt(message.encode())
            # Send the encrypted message to all connected clients
            for client_socket in list(clients):  # Use list(clients) to avoid modifying the list while iterating
                try:
                    client_socket.send(encrypted_message)
                except BrokenPipeError:
                    print(f"{Fore.RED}Error: Broken pipe while sending message.{Fore.RED}{Fore.RESET}")
                    client_socket.close()
                    if client_socket in clients:
                        clients.remove(client_socket)
        except Exception as e:
            print(f"{Fore.RED}Error while sending message: {e}{Fore.RED}{Fore.RESET}")

# Start threads for accepting connections and sending messages
accept_thread = threading.Thread(target=accept_connections)
send_thread = threading.Thread(target=send_messages)

accept_thread.start()
send_thread.start()

accept_thread.join()
send_thread.join()

server_socket.close()
