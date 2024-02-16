from termcolor import cprint
from itertools import cycle
import subprocess
import time
import os

def waiting(n, delay=.1, prompt='Loading'):
    for _ in range(n):
        for char in '/-\|':
            print(f'\r {prompt} {char}', end='')
            time.sleep(delay)

contents = ['HostName::Password']  # record all data to export
_colors = ['blue', 'red']
colors = iter(cycle(_colors))
os.system('cls')

print('\n Welcome to WiFi Password Extractor (written by Sina.F)\n')
time.sleep(.7)

waiting(12, delay=0.15, prompt='Extracting WiFi Passwords... ')

time.sleep(1)
print('\n\n\n {:<30}|  Password\n'.format('Host Name'))
output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode().splitlines()
profiles = [line.split(':', 1)[-1].lstrip() for line in output if 'All User Profile' in line]

for profile in profiles:
    result = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', profile, 'key=clear']).decode('ISO-8859-1').splitlines()
    color = next(colors)

    try:
        password = [line.split(':', 1)[1].lstrip() for line in result if 'Key Content' in line][0]
        cprint(f' {profile:<30}|  {password}', color=color)
        contents.append(f'{profile}::{password}')

    except Exception:
        cprint(f' {profile:<30}|  <No Password>', color=color)
        contents.append(f'{profile}::')

    finally:
        time.sleep(.7)

if len(contents) > 1:
    with open('wifi-passwords.txt', 'w') as handler:
        for line in contents:
            handler.write(line + '\n')

    print('\n The informations have been saved in <wifi-passwords.txt>')


FIGLET = '''\n
   _____ _                __ 
  / ____(_)              / _|
 | (___  _ _ __   __ _  | |_ 
  \___ \| | '_ \ / _` | |  _|
  ____) | | | | | (_| |_| |  
 |_____/|_|_| |_|\__,_(_)_| 
'''

for line in FIGLET.splitlines():
    print(line)
    time.sleep(.2)

time.sleep(1)
input('\n\n Press <enter> to exit...')
