import time
import datetime
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.service import Service


url = "https://web.whatsapp.com/"
browser_binary = "C:\\Users\\User\\Downloads\\PortableApps\\PortableApps\\FirefoxPortable\\App\\Firefox64\\firefox.exe"  # Change this
geckodriver_path = "C:\\Users\\User\\Downloads\\geckodriver-v0.29.1-win64\\"  # Change this

# colors
YELLOW = '\x1b[33m'
LIGHT_CYAN = '\x1b[96m'
RESET = '\x1b[39m'
RED = '\x1b[31m'
GREEN = '\x1b[32m'
LIGHT_GREEN = '\x1b[92m'
BLACK = '\x1b[30m'
WHITE = '\x1b[47m'
LIGHT_RED = '\x1b[91m'
LIGHT_BLUE = '\x1b[94m'


class CanNotGetUserName(Exception):
    """
    Error class
    """


def _login():
    global driver

    binary = FirefoxBinary(browser_binary)
    driver = webdriver.Firefox(
        service=Service(geckodriver_path), firefox_binary=binary)

    driver.get(url)
    print("> Ready to scan QRCode... Type in `y` if finished scanning QRCode:")
    time.sleep(0.1)

    input(">> ")


def _get_user(username):
    try:
        # Searches for the user name and returns `True` if it was successful
        search_box_element = driver.find_elements_by_class_name(
            "selectable-text")[0]
        search_box_element.send_keys(username)
        search_box_element.send_keys(Keys.ENTER)
        search_box_element.send_keys(
            Keys.CONTROL + Keys.LEFT_SHIFT + Keys.BACKSPACE)
        return True, ""

    except Exception as e:
        # Otherwise it returns `False`
        return False, e


def _get_status(username) -> bool:
    get_user = _get_user(username)

    if not get_user[0]:
        raise CanNotGetUserName(f"{get_user[1]}")

    try:
        return driver.find_element_by_class_name("_7yrSq").text == "online"

    except Exception:
        return False


def _logs(data: str, file: str):
    with open(file, "a+") as f:
        f.write(data+"\n")


def print_loop(char: chr, loops: int) -> str:
    return "".join(char for _ in range(loops))


def spy(usernames: list, seconds: int, logs: str, duration: int = 1, md=False):
    global longest_length
    length = 0

    if md and logs.endswith(".txt"):
        print(
            f"{YELLOW}[{LIGHT_CYAN}i{YELLOW}]{RESET} Detected txt extension for md file, changing extension to 'md'...")
        logs = logs.split(".txt")[:-1]+'.md'

    for username in usernames:
        if len(username)+65 > length:
            length = len(username)+65
            longest_length = len(username)

    print_line = print_loop("-", 27+longest_length)
    print_line_with_space = "|"+print_loop(" ", 27+longest_length-2)+"|"
    print_line_with_space_logs = "|" + \
        print_loop(" ", 27+longest_length-2+10)+"|"

    print(
        f"\n\n{RED}<{GREEN} Start of logs {RED}>")
    print(print_line)
    print(f"{LIGHT_CYAN}Scanning for {', '.join(usernames)}{RED}")
    print(print_line)
    print(f"{RED}{print_line_with_space}")
    print(f"{print_line_with_space}")
    print(f"{print_line_with_space}{RESET}")

    if md:
        _logs(
            f"\n### Start of logs @ {datetime.datetime.now().strftime('%H:%M:%S, %d.%m.%Y')}", logs)
        _logs(print_line+'---', logs)
        _logs(f"Scanning for `{', '.join(usernames)}`:", logs)
        _logs(print_line+'---', logs)
    else:
        _logs(
            f"\n< Start of logs @ {datetime.datetime.now().strftime('%H:%M:%S, %d.%m.%Y')} >", logs)
        _logs(print_line+'----------', logs)
        _logs(f"Scanning for {', '.join(usernames)}:", logs)
        _logs(print_line+'----------', logs)
    _logs(print_line_with_space_logs, logs)
    _logs(print_line_with_space_logs, logs)
    _logs(print_line_with_space_logs, logs)

    for _ in range(int((duration*60*60)/seconds)):
        if len(usernames) > 1:
            for username in usernames:
                if _get_status(username):
                    msg = f"{RED}| >{YELLOW} [{LIGHT_CYAN}{username}{YELLOW}]{LIGHT_CYAN} online{RESET}: {LIGHT_CYAN}{datetime.datetime.now().strftime('%H:%M:%S')} {RED} "
                    msg_log = f"| > [{username}] online: {datetime.datetime.now().strftime('%H:%M:%S, %d.%m.%Y')}  "

                    while len(msg) <= length:
                        msg += ' '
                    while len(msg_log) <= length-8*5+10:
                        msg_log += ' '
                    msg += '|'
                    msg_log += '|'
                    print(msg)
                    _logs(data=msg_log,
                          file=logs)

        elif _get_status(usernames):
            msg = f"{RED}| >{YELLOW} [{LIGHT_CYAN}{usernames}{YELLOW}]{LIGHT_GREEN} online{RESET}: {LIGHT_CYAN}{datetime.datetime.now().strftime('%H:%M:%S')} {RED} "
            msg_log = f"| > [{usernames}] online: {datetime.datetime.now().strftime('%H:%M:%S, %d.%m.%Y')}  "
            while len(msg) <= length:
                msg += ' '
            while len(msg_log) <= length-8*5+10:
                msg_log += ' '
            msg += '|'
            msg_log += '|'
            print(msg)
            _logs(data=msg_log,
                  file=logs)

        time.sleep(seconds)

    print(f"{RED}{print_line_with_space}")
    print(f"{print_line_with_space}")
    print(f"{print_line_with_space}")
    print(f"{print_line}{RESET}")
    print(f"{RED}<{GREEN} End of logs {RED}>\n\n")
    print(f"{YELLOW}->{RESET} Good bye!")

    _logs(print_line_with_space_logs, logs)
    _logs(print_line_with_space_logs, logs)
    _logs(print_line_with_space_logs, logs)

    if md:
        _logs(print_line+"---", logs)
        _logs(
            f"### End of logs @ {datetime.datetime.now().strftime('%H:%M:%S, %d.%m.%Y')}\n", logs)
        _logs('### Good bye! Exiting program', logs)

    else:
        _logs(print_line+"----------", logs)
        _logs(
            f"< End of logs @ {datetime.datetime.now().strftime('%H:%M:%S, %d.%m.%Y')} >\n", logs)
        _logs('-> Good bye! Exiting program', logs)

    driver.close()
    exit(0)


def console_management():
    cmd = ""
    print(f"{BLACK}{WHITE}Help: Type in:\n    b -> break\n    p {time} -> pause for that time\n    s -> stop until starting\n    c -> continue{RESET}")
    while cmd != "b":
        cmd = input(
            f"{LIGHT_RED}>>> {LIGHT_CYAN}")
        cmds = ["p", "s", "c"]
        if cmd not in cmds:
            print("Command not found. Please check the help menu!")

        elif cmd.startswith("p"):
            if len(cmd) > 2:
                print("Isn't implemented yet.")

            else:
                print("Use: p {time}")

        elif cmd == "s":
            print("Isn't implemented yet.")

        elif cmd == "c":
            print("Isn't implemented yet.")


def main(usernames, seconds, logs, duration):
    """
    username(s) should be in form: username1, username2, username3, ...
    """

    _login()
    if ',' in usernames:
        usernames = [i.strip() for i in usernames.split(',')]
        spy(usernames, seconds, logs, duration)

    else:
        spy([usernames], seconds, logs, duration)


if __name__ == '__main__':

    welcome_msg = f"""
    {LIGHT_BLUE}o.0 always spying
    {LIGHT_GREEN}             _       ____          __       ____       
                | |     / / /_  ____ _/ /______/ __ \__  __
                | | /| / / __ \/ __ `/ __/ ___/ /_/ / / / /
                | |/ |/ / / / / /_/ / /_(__  ) ____/ /_/ / 
                |__/|__/_/ /_/\__,_/\__/____/_/    \__, /  
                                                  /____/{LIGHT_BLUE}
    """

    print(welcome_msg)

    time.sleep(3)
    try:
        parser = argparse.ArgumentParser(
            description='WhatsSpy is a tool for spying whatsapp users')
        parser.add_argument('-u', '--users', metavar='', type=str,
                            help="Users (should be in format: 'username1, username2, username3, ...')")
        parser.add_argument('-t', '--timeout', metavar='',
                            type=int, help="Time to sleep between checks")
        parser.add_argument('-l', '--logfile', metavar='', type=str,
                            help="Log file, any extension is allowed.")
        parser.add_argument('-d', '--duration', metavar='',
                            type=float, help='Duration (in hours) as float')

        args = parser.parse_args()
        main(args.users, args.timeout, args.logfile, duration=args.duration)

    except KeyboardInterrupt:
        print(f"\n{YELLOW}> Good bye!")
