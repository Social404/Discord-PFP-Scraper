

import discum,sys,os,shutil,requests
from colorama import Fore

if os.name == 'nt':
	os.system("cls")
else:
	os.system("clear")

open("scraped.txt", "w").close()

print(f'''{Fore.RED}
 ░█▀▄░▀█▀░█▀▀░█▀▀░█▀█░█▀▄░█▀▄
 ░█░█░░█░░▀▀█░█░░░█░█░█▀▄░█░█
 ░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀░
 ░█▀▀░█▀▀░█▀▄░█▀█░█▀█░█▀▀░█▀▄
 ░▀▀█░█░░░█▀▄░█▀█░█▀▀░█▀▀░█▀▄
 ░▀▀▀░▀▀▀░▀░▀░▀░▀░▀░░░▀▀▀░▀░▀ {Fore.MAGENTA}(PFP Edition)\n''')

TOKEN = input(f"{Fore.BLUE} Token: {Fore.RESET}")
SERVER_ID = input(f"{Fore.BLUE} Server ID: {Fore.RESET}")
CHANNEL_ID = input(f"{Fore.BLUE} Channel ID: {Fore.RESET}")

if (TOKEN == "" or SERVER_ID == "" or CHANNEL_ID == ""):
    print(f"{Fore.RED} Your provided an invalid token, server or channel id!{Fore.RESET}")
    sys.exit()

discord = discum.Client(token=TOKEN)
discord.gateway.log = False

def close(resp, guild_id):
    if discord.gateway.finishedMemberFetching(guild_id):
        discord.gateway.removeCommand({'function': close, 'params': {'guild_id': guild_id}})
        discord.gateway.close()

def fetch(guild_id, channel_id):
    discord.gateway.fetchMembers(guild_id, channel_id, keep='all', wait=.1)
    discord.gateway.command({'function': close, 'params': {'guild_id': guild_id}})
    discord.gateway.run()
    discord.gateway.resetSession()
    return discord.gateway.session.guild(guild_id).members

members_list = fetch(SERVER_ID, CHANNEL_ID)
id_list = []

for IDS in members_list:
    id_list.append(f"https://cdn.discordapp.com/avatars/{IDS}/{members_list[IDS]['avatar']}.png?size=512")

file = open("scraped.txt", "a")

for id in id_list:
    file.write(id + "\n")
file.close()

urls = open("scraped.txt").read().splitlines()

print(f"\n{Fore.YELLOW}[!] Starting download.. loaded {len(urls)} images.\n{Fore.RESET}")

counter = 1

for x in range(len(urls)):
    try:
        response = requests.get(urls[x], stream=True)
        if response.status_code == 200:
            with open(f'img/{counter}.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
                print(f"{Fore.GREEN} [+] Saved {counter}.png{Fore.RESET}")
                counter += 1
            del response
        else:
            print(f"{Fore.RED}Can't download {counter}.png{Fore.RESET}")
            counter -= 1
    except:
        print(f"{Fore.RED} [-] Can't download {counter}.png{Fore.RESET}")
        counter -= 1
        pass
# Not Made By Social404