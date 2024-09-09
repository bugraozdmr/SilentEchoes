from colorama import Fore
from cryptography.fernet import Fernet
import modules.log as log
import threading
import random
import string
from datetime import datetime

clients = []
usernames = {}

# file_name if its needed
today = datetime.now().strftime("%b-%d-%y")
rastgele_karakterler = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
file_name = f"{today}-{rastgele_karakterler}.txt"

def handle_client(client_socket, addr, cipher, user, password,logging):
    try:
        global file_name
        
        flag = 2
        
        print(f"\nConnection attempt from {addr}")
        
        if logging == True:
            log.write_on_file(file_name,f"\nConnection attempt from {addr}\n")
            
        username_message = client_socket.recv(1024)
            
        decoded_message = cipher.decrypt(username_message).decode()
        
        username, received_password = [part.split(":")[1] for part in decoded_message.split(",")]
        
        usernames[client_socket] = username
        
        if password and password != received_password:
            print("Failed password attempt")
            client_socket.close()
            if client_socket in clients:
                clients.remove(client_socket)
            flag = 1
        else :
            notify_message = f"{username} has joined the chat. (Active users {len(clients) + 1})"
            
            if logging == True:
                log.write_on_file(file_name,f"{username} has joined the chat. (Active users {len(clients) + 1})\n")
            
            broadcast(cipher.encrypt(notify_message.encode()), None)
            while True:
                encrypted_response = client_socket.recv(1024)
                if not encrypted_response:
                    print(f"\nConnection closed by {addr}.")
                    break
                response = cipher.decrypt(encrypted_response).decode()
                print(f"\n{response}\n{user}: ", end="")
                
                if logging == True:
                    log.write_on_file(file_name,f"{response}\n")
                
                broadcast(encrypted_response, client_socket)
                
        if flag != 1:
            notify_message = f"{username} has left the chat (Active users {len(clients) + 1})"
            
            if logging == True:
                log.write_on_file(file_name,f"{username} has left the chat (Active users {len(clients) + 1})\n")
            
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

def accept_connections(server_socket, cipher, user,password,logging):
    global file_name
    
    if logging == True:
        log.create_file(file_name,"Session started waiting")
    
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        client_handler_thread = threading.Thread(target=handle_client, args=(client_socket, addr, cipher, user,password,logging))
        client_handler_thread.start()

def send_messages(user, cipher,logging):
    global file_name
    
    while True:
        try:
            user_input = input(f"{user}: ") or user
            message = f"{user}: {user_input}"
            encrypted_message = cipher.encrypt(message.encode())
            
            if logging == True:
                log.write_on_file(file_name,f"{message}\n")
            
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