import modules.banner as b
import server
import client
from colorama import Fore
import os

b.info()

print(f"{Fore.CYAN}1. Start Session\n2. Connect to a session{Fore.CYAN}{Fore.RESET}")

user_choice = input(f"Choice : ").strip()

match user_choice:
    case "1":
        os.system('clear')
        server.main()
    case "2":
        os.system('clear')
        client.main()
    case _:
        print(f"{Fore.RED}Invalid choice. Exiting...{Fore.RED}{Fore.RESET}")