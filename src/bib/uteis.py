from datetime import datetime
from colorama import init, Fore, Style
import asyncio
import time

def log_term(msg: str, color: str = "DEFAULT") -> None: 
    now = datetime.now()
    timestamp = now.strftime("[%d/%m/%Y %H:%M:%S]")

    if (color == "DEFAULT"):
        outColor = ""
    elif (color == "BLUE"):
        outColor = Fore.BLUE
    elif (color == "GREEN"):
        outColor = Fore.GREEN
    else:
        outColor = Fore.WHITE        

    print(f"{Fore.BLUE}K:{Style.RESET_ALL} {Fore.YELLOW}{timestamp}{Style.RESET_ALL}  {outColor}{msg}{Style.RESET_ALL}")


async def sleep_async(seconds: int) -> None:
    await asyncio.sleep(seconds)  

def sleep(seconds: int) -> None:
    time.sleep(seconds)  





