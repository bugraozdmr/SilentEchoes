from cryptography.fernet import Fernet
import socket
import modules.read_key as rk
import modules.banner as banner
import modules.server_methods as sm
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

print(f"{Fore.CYAN}------------------{Fore.CYAN}{Fore.RESET}\nHost: {host} \nPort: {port}\n{Fore.CYAN}------------------{Fore.CYAN}{Fore.RESET}")

room_password = input("Room Password (Optional): ").strip()
if host != default_host:
    print(f"{Fore.RED}Host has to be your local IP address{Fore.RED}{Fore.RESET}")
    exit()

default_user = host
user = input(f"User (default '{default_user}'): ").strip() or default_user

if(len(user) > 20):
    print(f"{Fore.RED}Username can not be longer than 20 characters ...{Fore.RED}{Fore.RESET}")
    exit()

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


accept_thread = threading.Thread(target=sm.accept_connections,args=(server_socket,cipher,user,room_password))
send_thread = threading.Thread(target=sm.send_messages,args=(user,cipher))

accept_thread.start()
send_thread.start()

accept_thread.join()
send_thread.join()

server_socket.close()