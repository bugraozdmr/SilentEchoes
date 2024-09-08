from cryptography.fernet import Fernet
import socket
import modules.read_key as rk
import modules.get_ip as gi
import modules.banner as banner
import modules.get_local_ip as gli
import random
import os
from colorama import Fore, Style

#todo
#sudo ufw allow 1453/tcp
#sudo ufw status verbose
#sudo ufw enable
#telnet [IP-adresi] 1453


banner.info()

# read the key
try:
    key = rk.load_key()
    print(f"{Fore.CYAN}[+]{Fore.CYAN}{Fore.RESET}{Fore.YELLOW} {Fore.YELLOW}Key upload success{Fore.YELLOW}{Fore.RESET}")
except Exception as e:
    print(f"{Fore.RED}Error: {e}{Fore.RED}{Fore.RESET}")
    exit()
    
cipher = Fernet(key)

try:
    local_ip = gli.get_local_ip()
    print(f"{Fore.CYAN}[+]{Fore.CYAN}{Fore.RESET}{Fore.YELLOW} Local Ip Found{Fore.YELLOW}{Fore.RESET}")
except Exception as e:
    print(f"{Fore.RED}Error: {e}{Fore.RED}{Fore.RESET}")
    exit()
    
#print(f"{Fore.RED}[+]{Fore.RED}{Fore.RESET}{Fore.GREEN} Global Ip Can Use\n{Fore.GREEN}{Fore.RESET}")

default_host = local_ip
default_port = 1453

host = input(f"Host (default '{default_host}'): ") or default_host
port_input = input(f"Port (default '{default_port}'): ") or default_port

# Control
try:
    port = int(port_input)
except ValueError:
    print(f"{Fore.RED}The input is not a valid integer.{Fore.RED}{Fore.RESET}")
    exit()
except TypeError:
    print(f"{Fore.RED}The input is not of the correct type.{Fore.RED}{Fore.RESET}")
    exit()

print(f"Host: {host}")
print(f"Port: {port}")

room_password = input("Room Password (Optional)")

"""get ip
public_ip = gi.get_public_ip()
if public_ip:
    default_user = public_ip
else:
    default_user = "user"+random.randint(100, 999)
    print("User Ip could not found continuing with random user")
    
if(host != default_host and host != public_ip):
    print(f"{Fore.RED}Host has to be either your local ip address or global ip address{Fore.RED}{Fore.RESET}")
    exit()
"""

if(host != default_host):
    print(f"{Fore.RED}Host has to be your local ip address{Fore.RED}{Fore.RESET}")
    exit()

default_user = host

user = input(f"User (default '{default_user}'): ") or default_user

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
except Exception as e :
    print(f"{Fore.RED}Error : {e}{Fore.RED}{Fore.RESET}")
    exit()

os.system("clear")
print("Server started waiting ...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection success: {addr}")
    
    while True:
        encrypted_message = client_socket.recv(1024)
        if not encrypted_message:
            break
        message = cipher.decrypt(encrypted_message).decode()
        print(f"{message}")
        
        user_input = input(f"{user}: ") or user
        
        response = f"{user} : {user_input}"
        
        encrypted_response = cipher.encrypt(response.encode())
        client_socket.send(encrypted_response)

    client_socket.close()
