from cryptography.fernet import Fernet
import socket
import modules.read_key as rk
import modules.banner as banner
import modules.get_local_ip as gli
import modules.client_methods as cm
import os
from colorama import Fore
import threading


banner.info()

# read the key
try:
    key = rk.load_key()
    print(f"{Fore.CYAN}[+]{Fore.CYAN}{Fore.RESET}{Fore.YELLOW} Key upload success{Fore.YELLOW}{Fore.RESET}")
except Exception as e:
    print(f"Error: {e}")
    exit()

cipher = Fernet(key)

try:
    local_ip = gli.get_local_ip()
    print(f"{Fore.CYAN}[+]{Fore.CYAN}{Fore.RESET}{Fore.YELLOW} Local IP Found{Fore.YELLOW}{Fore.RESET}\n")
except Exception as e:
    print(f"{Fore.RED}Error: {e}{Fore.RED}{Fore.RESET}")
    exit()

default_user = local_ip
user = input(f"User (default '{default_user}'): ") or default_user

host = input("Connect Host IP: ").strip()
port_input = input("Connect Host Port: ").strip()

try:
    port = int(port_input)
except ValueError:
    print(f"{Fore.RED}Port must be an integer.{Fore.RED}{Fore.RESET}")
    exit()

print(f"Connecting {host}:{port_input}")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((host, port))
except Exception as e:
    print(f"{Fore.RED}Error: {e}{Fore.RED}{Fore.RESET}")
    exit()

os.system("clear")
print(f"Connected {Fore.CYAN}{host}:{port_input}{Fore.CYAN}{Fore.RESET}")

receive_thread = threading.Thread(target=cm.receive_messages, args=(client_socket, cipher, user))
send_thread = threading.Thread(target=cm.send_messages, args=(client_socket, cipher, user))

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()

client_socket.close()