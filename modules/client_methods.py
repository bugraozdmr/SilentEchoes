from colorama import Fore

def receive_messages(client_socket,cipher,user):
    while True:
        try:
            encrypted_response = client_socket.recv(1024)
            if not encrypted_response:
                print("Connection closed by the server.")
                break
            response = cipher.decrypt(encrypted_response).decode()
            print(f"\n{response}\n{user}: ", end="")
        except Exception as e:
            print(f"{Fore.RED}Error while receiving message: {e}{Fore.RED}{Fore.RESET}")
            break

def send_messages(client_socket,cipher,user):
    while True:
        try:
            user_input = input(f"{user}: ") or user
            message = f"{user} : {user_input}"
            encrypted_message = cipher.encrypt(message.encode())
            client_socket.send(encrypted_message)
        except Exception as e:
            print(f"{Fore.RED}Error while sending message: {e}{Fore.RED}{Fore.RESET}")
            break