import warnings
from colorama import Fore, Style

warnings.filterwarnings("ignore")

module_description = "SilentEchoes offers a secure space for anonymous messaging. Enjoy private conversations with end-to-end encryption, ensuring your identity and messages remain confidential. Speak freely and stay hidden with SilentEchoes."
__version__ = "1.0.0"


def info():
    print(

        '   _________.__.__                 __ ___________      .__                             \n' +
        '  /   _____/|__|  |   ____   _____/  |\_   _____/ ____ |  |__   ____   ____   ______\n' +
        '  \_____  \ |  |  | _/ __ \ /    \   __\    __)__/ ___\|  |  \ /  _ \_/ __ \ /  ___/  \n' +
        '  /        \|  |  |_\  ___/|   |  \  | |        \  \___|   Y  (  <_> )  ___/ \___ \  \n' +
        ' /_______  /|__|____/\___  >___|  /__|/_______  /\___  >___|  /\____/ \___  >____  > \n' +
        '         \/              \/     \/            \/     \/     \/            \/     \/   \n'
    )
    print(f"SilentEchoes {__version__}\n{module_description} \n\n\n")
    #print(f"{Fore.CYAN}{Fore.YELLOW}Warning : /Only designed as a project, abuse is not my problem/{Fore.YELLOW}{Fore.RESET}")