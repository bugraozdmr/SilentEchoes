from cryptography.fernet import Fernet
import socket
import modules.read_key as rk
import modules.get_ip as gi
import random
import modules.banner as banner
from colorama import Fore, Style
import os

banner.info()

# read the key
try:
    key = rk.load_key()
    print("Key upload success")
except Exception as e:
    print(f"Error: {e}")
    exit()
    
cipher = Fernet(key)

# get ip
public_ip = gi.get_public_ip()
if public_ip:
    default_user = public_ip
else:
    default_user = "user"+random.randint(100, 999)
    print("User Ip could not found continuing with random user")

user = input(f"User (default '{default_user}'): ") or default_user

host = input("Connect Host Ip :") 
port_input = input("Connect Host Port :")

port = int(port_input)

print(f"Connectiong {host}:{port_input}")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((host, port))
except Exception as e:
    print(f"{Fore.RED}Error: {e}{Fore.RED}{Fore.RESET}")
    exit()
    
os.system("clear")
print(f"Connected {Fore.CYAN}{host}:{port_input}{Fore.CYAN}{Fore.RESET}")

while True:
    user_input = input(f"{user}: ") or user
    message = f"{user} : {user_input}"
    
    encrypted_message = cipher.encrypt(message.encode())
    client_socket.send(encrypted_message)
    
    encrypted_response = client_socket.recv(1024)
    response = cipher.decrypt(encrypted_response).decode()
    print(f"Sunucudan yanıt: {response}")

client_socket.close()
