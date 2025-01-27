import os
import time
import random
import json
import platform  # Добавляем импорт для системной информации
import psutil  # Добавляем импорт для системной информации
import ping3   # Добавляем импорт для пинга
import difflib  # Добавляем импорт для сравнения файлов
# Добавляем новые импорты для сетевых утилит
import requests
import socket
import paramiko
import netifaces
from urllib.parse import urlparse
from datetime import datetime as d, timedelta
import pyfiglet
import colorama
from colorama import Fore, Style, Back
import curses
from curses import textpad
import sys
import zipfile
import tarfile
import gzip
import shutil
from datetime import datetime as d, timedelta
import threading
import schedule
import shutil
import re
import sqlite3
from datetime import datetime, timedelta
import calendar as cal

version = '1.0'
versionName = 'Alpha 1'
global Cn
Cn = 'hbash'

# Добавим новые цветовые стили
class Colors:
    PROMPT = Fore.CYAN + Style.BRIGHT
    PATH = Fore.BLUE + Style.BRIGHT
    USERNAME = Fore.GREEN + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    RESET = Style.RESET_ALL
    HEADER = Fore.MAGENTA + Style.BRIGHT
    FILE = Fore.WHITE
    DIR = Fore.BLUE + Style.BRIGHT
    INPUT = Fore.CYAN
    ICONS = Fore.YELLOW

class Icons:
    FOLDER = "📁"
    FILE = "📄"
    ERROR = "❌"
    SUCCESS = "✅"
    WARNING = "⚠️"
    ARROW = "→"
    PROMPT = "❯"
    TIME = "🕒"
    CALC = "🔢"
    USER = "👤"
    PC = "💻"
    PACKAGE = "📦"
    HOME = "🏠"
    BACK = "⬅️"
    SETTINGS = "⚙️"
    HELP = "❔"
    LOGIN = "🔑"
    LOGOUT = "🚪"
    ADD_USER = "➕"
    DEL_USER = "➖"
    DATABASE = "💾"
    EDIT = "✏️"
    SAVE = "💾"
    CANCEL = "❌"
    NEW_FILE = "📝"
    COPY = "📋"
    MOVE = "✂️"
    DELETE = "🗑️"
    NEW_FOLDER = "📂"
    VIEW = "👀"
    TOUCH = "✨"
    SEARCH = "🔍"
    TREE = "🌳"
    BRANCH = "├──"
    LAST_BRANCH = "└──"
    PIPE = "│   "
    SPACE = "    "
    PROCESS = "⚙️"
    KILL = "💀"
    MONITOR = "📊"
    DISK = "💽"
    MEMORY = "🧠"
    CLOCK = "⏰"
    NETWORK = "🌐"
    PING = "📡"
    ZIP = "📦"
    UNZIP = "📨"
    COMPRESS = "🗜️"
    EXTRACT = "📤"
    SEARCH_TEXT = "🔎"
    SORT = "↕️"
    COUNT = "🔢"
    DIFF = "🔄"
    HEAD = "⬆️"
    TAIL = "⬇️"

# Класс для работы с пользователями
class UserManager:
    def __init__(self):
        self.users_file = "users.json"
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {"root": {"password": "root", "is_admin": True}}

    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def add_user(self, username, password, is_admin=False):
        if username in self.users:
            return False, "User already exists"
        self.users[username] = {"password": password, "is_admin": is_admin}
        self.save_users()
        return True, "User added successfully"

    def delete_user(self, username):
        if username == "root":
            return False, "Cannot delete root user"
        if username in self.users:
            del self.users[username]
            self.save_users()
            return True, "User deleted successfully"
        return False, "User not found"

    def verify_user(self, username, password):
        if username in self.users:
            return self.users[username]["password"] == password
        return False

    def is_admin(self, username):
        return username in self.users and self.users[username]["is_admin"]

# Инициализация менеджера пользователей
user_manager = UserManager()
current_user = None

# Добавляем класс для работы с локализацией
class Localization:
    def __init__(self):
        self.strings = {}
        self.current_lang = 'en'
        self.available_langs = {}
        self.load_languages()
        self.load_config()
        self.load_language()

    def load_languages(self):
        base_path = os.path.join(os.path.dirname(__file__), 'localization')
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            # Создаем базовые языковые файлы
            self.create_default_langs(base_path)
        
        for lang_dir in os.listdir(base_path):
            lang_path = os.path.join(base_path, lang_dir)
            if os.path.isdir(lang_path):
                lang_file = os.path.join(lang_path, 'strings.json')
                if os.path.exists(lang_file):
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        info = json.load(f)
                        self.available_langs[lang_dir] = info.get('language_name', lang_dir)

    def create_default_langs(self, base_path):
        default_langs = {
            'en': {
                'language_name': 'English',
                'strings': {
                    'welcome': 'Welcome to hbash!',
                    'login_prompt': 'Username: ',
                    'password_prompt': 'Password: ',
                    'login_success': 'Login successful',
                    'login_failed': 'Invalid username or password',
                    # ...добавьте другие строки здесь...
                }
            },
            'ru': {
                'language_name': 'Русский',
                'strings': {
                    'welcome': 'Добро пожаловать в hbash!',
                    'login_prompt': 'Имя пользователя: ',
                    'password_prompt': 'Пароль: ',
                    'login_success': 'Вход выполнен успешно',
                    'login_failed': 'Неверное имя пользователя или пароль',
                    # ...добавьте другие строки здесь...
                }
            }
        }
        
        for lang, data in default_langs.items():
            lang_dir = os.path.join(base_path, lang)
            os.makedirs(lang_dir, exist_ok=True)
            with open(os.path.join(lang_dir, 'strings.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.current_lang = config.get('language', 'en')
        except:
            self.current_lang = 'en'

    def save_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        config = {'language': self.current_lang}
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)

    def load_language(self):
        lang_file = os.path.join(os.path.dirname(__file__), 
                               'localization', 
                               self.current_lang, 
                               'strings.json')
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.strings = data['strings']
        except:
            print(f"Error loading language {self.current_lang}, falling back to English")
            self.current_lang = 'en'
            self.load_language()

    def get_string(self, key, default=''):
        return self.strings.get(key, default)

# Инициализируем локализацию
localization = Localization()

# Функция входа пользователя (перемещаем в начало, после определения классов)
def login_user():
    global current_user
    clearscreen()
    while not current_user:
        try:
            username = input(f"{Colors.INPUT}{Icons.USER} {localization.get_string('login_prompt', 'Username: ')}{Colors.RESET}")
            if not username:
                continue
            password = input(f"{Colors.INPUT}{Icons.LOGIN} {localization.get_string('password_prompt', 'Password: ')}{Colors.RESET}")
            if user_manager.verify_user(username, password):
                current_user = username
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} {localization.get_string('login_success', 'Login successful')}{Colors.RESET}")
                time.sleep(1)
                clearscreen()
            else:
                print(f"{Colors.ERROR}{Icons.ERROR} {localization.get_string('login_failed', 'Invalid username or password')}{Colors.RESET}")
        except KeyboardInterrupt:
            print('\nAbort.')
            quit()

# Модифицируем функцию очистки экрана (ASCII-логотип хуйни ебучей, поэтому без него)
def clearscreen(): 
    os.system('cls' if os.name == 'nt' else 'clear')
#   print(Colors.HEADER + r"""
#  _    _ _______                  
# | |  | |__   __|                 
# | |__| |  | | ___ _ __ _ __ ___  
# |  __  |  | |/ _ \ '__| '_ ` _ \ 
# | |  | |  | |  __/ |  | | | | | |
# |_|  |_|  |_|\___|_|  |_| |_| |_| 
# Version """ + str(version) + ': "' + versionName + '"' + Colors.RESET) 

clearscreen()

def show_options_menu():
    global Cn  # Это сейчас избыточно, но безопасно оставить: а вообще, если это удалить, всё нахуй сломается
    while True:
        print(f"{Colors.HEADER}{localization.get_string('options.title', 'Options')}{Colors.RESET}\n--------")
        print(f"[T] {localization.get_string('options.terminal_color', 'Terminal Color')}")
        print(f"[L] {localization.get_string('options.language', 'Language')}")
        print(f"[C] {localization.get_string('options.computer_name', 'Computer Name')}")
        print(f"[B] {localization.get_string('options.back', 'Back')}")
        
        choice = input(f"\n{Colors.INPUT}Choice: {Colors.RESET}").lower()
        
        if choice == 't':
            # Локализация меню цветов (пока не работает)
            print(f"\n{localization.get_string('options.colors.title', 'Colors')}\n--------")
            colors = { # этот селектор бесполезен, так как изначально эта хуила делалась на начальных этапах.
                'D': 'default',
                'W': 'white',
                'R': 'red',
                'Y': 'yellow',
                'G': 'green',
                'B': 'blue',
                'C': 'cyan',
                'M': 'magenta'
            }
            for key, name in colors.items():
                print(f"[{key}] {localization.get_string(f'options.colors.{name}', name.capitalize())}")
            
            Ch = input().lower()
            # После установки цвета:
            print(localization.get_string('options.colors.color_set', 'Color set.'))

        elif choice == 'l':
            print(f"\n{localization.get_string('options.language_selection.available', 'Available Languages')}:")
            for code, name in localization.available_langs.items():
                if code == localization.current_lang:
                    print(f"{Colors.SUCCESS}[{code}] {name} ({localization.get_string('options.language_selection.current', 'current')}){Colors.RESET}")
                else:
                    print(f"[{code}] {name}")
            
            lang = input(f"\n{Colors.INPUT}{localization.get_string('options.language_selection.select', 'Select language')}: {Colors.RESET}").lower()
            if lang in localization.available_langs:
                localization.current_lang = lang
                localization.save_config()
                localization.load_language()
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} {localization.get_string('options.language_selection.success', 'Language set to: {0}').format(localization.available_langs[lang])}{Colors.RESET}")
                time.sleep(1)
                clearscreen()
            else:
                print(f"{Colors.ERROR}{Icons.ERROR} {localization.get_string('options.language_selection.invalid', 'Invalid language selection')}{Colors.RESET}")
        
        elif choice == 'c':
            current_name = Cn
            print(f"\n{username}@{current_name}")
            new_name = input(f"\n{localization.get_string('options.computer_name_prompt', 'Enter new computer name')}: ")
            if new_name:
                Cn = new_name
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} {localization.get_string('options.computer_name_set', 'Computer name set as')} \"{Cn}\"{Colors.RESET}")
        
        elif choice == 'b':
            break
        else:
            print(f"{Colors.ERROR}{Icons.ERROR} {localization.get_string('options.invalid_option', 'Invalid option')}{Colors.RESET}")

# Изменяем начальное меню
try:
    I = input(Colors.PROMPT + localization.get_string('main_menu', '[L]ogin, [O]ptions, or [Q]uit ') + Colors.RESET)
except KeyboardInterrupt:
    print('\n' + localization.get_string('abort', 'Abort.'))
    quit()

if I == 'L' or I == 'l':
    login_user()  # Используем новую функцию входа
elif I == 'Q' or I == 'q':
    print('Abort.')
    quit()
elif I == 'O' or I == 'o':
    show_options_menu()
    login_user()
else:
    try:
        O = input('Options\n--------\n[T]erminal Color\n[L]icense\n"[C]omputer" Name\n')
        if O == 'T' or O == 't':
            Ch = input('Colors\n--------\n[D]efault\n[W]hite\n[R]ed\n[Y]ellow\n[G]reen\n[B]lue\n[C]yan\n[M]agenta\n')
            if Ch == 'D' or Ch == 'd':
                print(Fore.RESET)
                print('Color set.')
            elif Ch == 'W' or Ch == 'w':
                print(Fore.WHITE)
                print('Color set.')
            elif Ch == 'R' or Ch == 'r':
                print(Fore.RED)
                print('Color set.')
            elif Ch == 'Y' or Ch == 'y':
                print(Fore.YELLOW)
                print('Color set.')
            elif Ch == 'G' or Ch == 'g':
                print(Fore.GREEN)
                print('Color set.')
            elif Ch == 'B' or Ch == 'b':
                print(Fore.BLUE)
                print('Color set.')
            elif Ch == 'C' or Ch == 'c':
                print(Fore.CYAN)
                print('Color set.')
            elif Ch == 'M' or Ch == 'm':
                print(Fore.MAGENTA)
                print('Color set.')
            else:
                print(Fore.RESET)
                print('Defaulting.')
        elif O == 'L' or O == 'l':
            Li = open("LICENSE", "r")
            print(Li.read())
            Li.close()
        elif O == 'C' or O == 'c':
            Cn = input('\nusername@hbash\n\nWhat do you want to change "hbash" to?\n')
            print(f'"Computer" name set as "{Cn}"\n')
        time.sleep(0.05)
        print('Saving...')
        time.sleep(0.2)
        login_user()  # Используем новую функцию входа после настроек
    except KeyboardInterrupt:
        print('\nAbort.')
        quit()

# Полезная штука для описания команд в справочнике команд (help)
helpCommand = '''
    quit - Quits the terminal.
    help - Shows this message.
    whoami - Prints your username.
    clear (cls) - Clears the screen.
    ver - Prints the current version.
    echo - Repeats what you tell it to.
    parcel - Installs new packages to use.
    cd - Change directory
    ls - List directory contents
    pwd - Print working directory
    calc - Calculator
    time - Show current date and time
    logout - Log out current user
    adduser - Add new user (root only)
    deluser - Delete user (root only)
    edit - Edit text file
    uname - Print system information
    cp - Copy files and directories
    mv - Move or rename files and directories
    rm - Remove files and directories
    mkdir - Create directories
    touch - Create empty files or update timestamps
    cat - Display file contents
    find - Search for files and directories
    tree - Display directory structure as a tree
    ps - List running processes
    kill - Terminate processes
    top - System resource monitor
    df - Disk space information
    free - Memory information
    uptime - System uptime
    netstat - Network connections
    ping - Check host availability
    zip - Create ZIP archives
    unzip - Extract ZIP archives
    tar - Work with TAR archives
    gzip - Compress files with GZIP
    gunzip - Decompress GZIP files
    grep - Search for text in files
    sort - Sort lines of text files
    wc - Print word, line, and byte counts
    diff - Compare files line by line
    head - Output the first part of files
    tail - Output the last part of files
    wget - Download files from the web
    curl - Transfer data from or to a server
    ifconfig - Display network interface configuration
    ssh - Open secure shell connection
    scp - Securely copy files between hosts
    weather - Show weather forecast for a city
    todo - Task management
    note - Note management
    calendar - Show calendar
    timer - Countdown timer
    stopwatch - Stopwatch function
'''
# Ещё более полезная хуйня (она просто более развёрнутая)
helpList = {
    'quit': '''\n    quit - Quits the terminal.\n    Usage: quit\n''',
    'help': '''\n    help - Shows the help message.\n    Usage: help [command]\n''',
    'whoami': '''\n    whoami - Prints your username.\n    Usage: whoami\n''',
    'clear': '''\n    clear - Clears the screen.\n    Usage: clear (or cls)\n''',
    'cls': '''\n    cls - Clears the screen.\n    Usage: cls (or clear)\n''',
    'ver': '''\n    ver - Prints the current version.\n    Usage: ver\n''',
    'echo': '''\n    echo - Repeats what you tell it to.\n    Usage: echo [arg] [string]\n    Arguments:\n    -u - Uppercase.\n    -l - Lowercase.\n    -sc - Swap case.\n    -r - Reversed.\n    -se - Seperate letters\n''',
    'parcel': '''\n    parcel - Installs new packages to use.\n    Usage: parcel [arg] [package]\n    Use "parcel help" to see all the usable arguments\n''',
    'cd': '''\n    cd - Change directory.\n    Usage: cd [path]\n''',
    'ls': '''\n    ls - List directory contents.\n    Usage: ls\n''',
    'pwd': '''\n    pwd - Print working directory.\n    Usage: pwd\n''',
    'calc': '''\n    calc - Calculator.\n    Usage: calc [expression]\n    Example: calc 2 + 2\n''',
    'time': '''\n    time - Show current date and time.\n    Usage: time\n''',
    'logout': '''\n    logout - Log out current user.\n    Usage: logout\n''',
    'adduser': '''\n    adduser - Add new user (root only).\n    Usage: adduser\n''',
    'deluser': '''\n    deluser - Delete user (root only).\n    Usage: deluser\n''',
    'edit': '''\n    edit - Edit text file.\n    Usage: edit <filename>\n    Commands: :w (save), :q (quit), :wq (save and quit), :h (help)\n''',
    'uname': '''\n    uname - Print system information.\n    Usage: uname [option]\n    Options:\n    -a - Print all information\n    -s - Print kernel name\n    -n - Print network node hostname\n    -r - Print kernel release\n    -v - Print kernel version\n    -m - Print machine hardware name\n    -p - Print processor type\n    -o - Print operating system\n''',
    'cp': '''\n    cp - Copy files and directories.\n    Usage: cp <source> <destination>\n    Example: cp file.txt backup/\n''',
    'mv': '''\n    mv - Move or rename files and directories.\n    Usage: mv <source> <destination>\n    Example: mv old.txt new.txt\n''',
    'rm': '''\n    rm - Remove files and directories.\n    Usage: rm <path>\n    Options:\n    -r - Remove directories and their contents recursively\n''',
    'mkdir': '''\n    mkdir - Create directories.\n    Usage: mkdir <directory>\n    Example: mkdir new_folder\n''',
    'touch': '''\n    touch - Create empty files or update timestamps.\n    Usage: touch <file>\n    Example: touch newfile.txt\n''',
    'cat': '''\n    cat - Display file contents.\n    Usage: cat <file>\n    Example: cat readme.txt\n''',
    'find': '''\n    find - Search for files and directories.\n    Usage: find <pattern>\n    Options:\n    -d - Search only directories\n    -f - Search only files\n    Example: find *.py\n''',
    'tree': '''\n    tree - Display directory structure as a tree.\n    Usage: tree [directory]\n    Options:\n    -d - Show only directories\n    Example: tree myproject\n''',
    'ps': '''\n    ps - List running processes.\n    Usage: ps [-a]\n    Options:\n    -a - Show all processes (default: user processes)\n''',
    'kill': '''\n    kill - Terminate processes.\n    Usage: kill <pid>\n    Example: kill 1234\n''',
    'top': '''\n    top - System resource monitor.\n    Usage: top\n    Press Q to exit\n''',
    'df': '''\n    df - Disk space information.\n    Usage: df [-h]\n    Options:\n    -h - Show sizes in human readable format\n''',
    'free': '''\n    free - Memory information.\n    Usage: free [-h]\n    Options:\n    -h - Show sizes in human readable format\n''',
    'uptime': '''\n    uptime - System uptime.\n    Usage: uptime\n''',
    'netstat': '''\n    netstat - Network connections.\n    Usage: netstat\n''',
    'ping': '''\n    ping - Check host availability.\n    Usage: ping <host> [-c count]\n    Example: ping google.com -c 4\n''',
    'zip': '''\n    zip - Create ZIP archives.\n    Usage: zip <archive.zip> <files...> [-r]\n    Example: zip archive.zip file1.txt dir1 -r\n''',
    'unzip': '''\n    unzip - Extract ZIP archives.\n    Usage: unzip <archive.zip> [destination]\n    Example: unzip archive.zip ./extracted/\n''',
    'tar': '''\n    tar - Work with TAR archives.\n    Usage: tar [options] <archive.tar> <files...>\n    Options:\n    -c - Create archive\n    -x - Extract archive\n    -f - Archive file (required)\n    Example: tar -cf archive.tar file1 file2\n           tar -xf archive.tar\n''',
    'gzip': '''\n    gzip - Compress files with GZIP.\n    Usage: gzip <file>\n    Example: gzip file.txt\n''',
    'gunzip': '''\n    gunzip - Decompress GZIP files.\n    Usage: gunzip <file.gz>\n    Example: gunzip file.txt.gz\n''',
    'grep': '''\n    grep - Search for text in files.\n    Usage: grep <pattern> <file> [options]\n    Options:\n    -i - Case insensitive search\n    -n - Show line numbers\n    Example: grep "text" file.txt -i -n\n''',
    'sort': '''\n    sort - Sort lines of text files.\n    Usage: sort <file> [options]\n    Options:\n    -r - Sort in reverse order\n    -n - Sort numerically\n    Example: sort data.txt -r\n''',
    'wc': '''\n    wc - Print word, line, and byte counts.\n    Usage: wc <file> [options]\n    Options:\n    -l - Print line count only\n    -w - Print word count only\n    -c - Print byte count only\n    Example: wc file.txt -l\n''',
    'diff': '''\n    diff - Compare files line by line.\n    Usage: diff <file1> <file2>\n    Example: diff old.txt new.txt\n''',
    'head': '''\n    head - Output the first part of files.\n    Usage: head <file> [-n lines]\n    Default: 10 lines\n    Example: head file.txt -n 5\n''',
    'tail': '''\n    tail - Output the last part of files.\n    Usage: tail <file> [-n lines]\n    Default: 10 lines\n    Example: tail file.txt -n 5\n''',
    'wget': '''\n    wget - Download files from the web.\n    Usage: wget <url> [output filename]\n    Example: wget https://example.com/file.txt my_file.txt\n''',
    'curl': '''\n    curl - Transfer data from or to a server.\n    Usage: curl [-X METHOD] [-H 'header: value'] [-d 'data'] <url>\n    Example: curl -X POST -H 'Content-Type: application/json' -d '{"key":"value"}' https://api.example.com\n''',
    'ifconfig': '''\n    ifconfig - Display network interface configuration.\n    Usage: ifconfig\n''',
    'ssh': '''\n    ssh - Open secure shell connection.\n    Usage: ssh <username>@<host> [-p port]\n    Example: ssh user@example.com -p 2222\n''',
    'scp': '''\n    scp - Securely copy files between hosts.\n    Usage: scp <source> <user>@<host>:<destination> [-p port]\n    Example: scp file.txt user@example.com:/home/user/\n''',
    'weather': '''\n    weather - Show weather forecast for a city.\n    Usage: weather <city>\n    Example: weather London\n''',
    'todo': '''\n    todo - Task management.\n    Usage: todo [command] [args]\n    Commands:\n    add <task> [--due YYYY-MM-DD] - Add new task\n    done <id> - Mark task as done\n    del <id> - Delete task\n    (no args) - List all tasks\n''',
    'note': '''\n    note - Note management.\n    Usage: note [command] [args]\n    Commands:\n    add - Add new note\n    del <id> - Delete note\n    edit <id> - Edit note\n    (no args) - List all notes\n''',
    'calendar': '''\n    calendar - Show calendar.\n    Usage: calendar [month] [year]\n    Example: calendar 12 2023\n    (no args) - Show current month\n''',
    'timer': '''\n    timer - Countdown timer.\n    Usage: timer <start|stop> [seconds]\n    Example: timer start 60\n''',
    'stopwatch': '''\n    stopwatch - Stopwatch function.\n    Usage: stopwatch <start|stop|lap>\n''',
}

# Тут я просто баловался, но это была заготовка для hpkg.
class package:
    def figlet(arg):
        pyfiglet.print_figlet(arg)
    
    def ball(arg):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]

        answer = random.choice(responses)
        if not arg == '':
            print(arg)
        print("My answer is:", answer)

# Добавляем глобальные структуры данных
command_history = []
aliases = {}
cron_jobs = {}
env_vars = os.environ.copy()
todo_db = "todo.db"
notes_db = "notes.db"
timer_threads = {}
stopwatch_start = None

# Инициализация баз данных
def init_databases():
    # Инициализация базы данных для задач
    conn = sqlite3.connect(todo_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS todos
                 (id INTEGER PRIMARY KEY, task TEXT, status TEXT, due_date TEXT)''')
    conn.commit()
    conn.close()

    # Инициализация базы данных для заметок
    conn = sqlite3.connect(notes_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY, title TEXT, content TEXT, created_date TEXT)''')
    conn.commit()
    conn.close()

init_databases()

class commands:
    def kill(arg):
        quit()

    def helpme(arg):
        if arg in helpList:
            print(helpList.get(arg))
        else:
            print(helpCommand)

    # Функция для вывода текущего юзера
    def whoami(arg):
        print(f"{Colors.SUCCESS}{Icons.USER} {current_user}{Colors.RESET}")
    
    # Функция очистки консоли
    def clear(arg):
        clearscreen()
    
    # Показ версии hbash
    def version(arg):
        print(f"{Colors.SUCCESS}{Icons.PC} hbash v{version}\n    {Icons.ARROW} \"{versionName}\"{Colors.RESET}")
    
    # Вывод строки пользователя (с поддержкой опций вывода)
    def echo(arg):
        try:
            # Верхний регистр
            if '-u' in prompt:
                text = prompt.split('-u')[1].strip().upper()
            # Нижний регистр
            elif '-l' in prompt:
                text = prompt.split('-l')[1].strip().lower()
            # Замена регистра
            elif '-sc' in prompt:
                text = prompt.split('-sc')[1].strip().swapcase()
            # Реверс текста
            elif '-r' in prompt:
                text = prompt.split('-r')[1].strip()[::-1]
            # Разделение символов пробелами (по приколу, видимо)
            elif '-se' in prompt: 
                textB = prompt.split('-se')[1].strip()
                textL = [*textB]
                text = ' '.join(textL)
            # Если опций нет, то башу будет поебать: он выведет просто текст юзера.
            # Да ему и так будет поебать: если аргументов будет много, он выберет
            # последний применённый в терминале аргумент
            else:
                text = prompt.split('echo ')[1].strip()
            print(text)
        # Неверный аргумент? Баш будет слать нахуй (ладно шучу, он просто выдаст ошибку)
        except IndexError:
            print('Missing argument for echo command.')
    
    def cfiglet(arg):
        # Рисует текст пользователя в ASCII (если пакет fig "установлен")
        if 'fig' in installed:
            package.figlet(arg)
        else:
            print('Command "fig" not found.')
    
    def cball(arg):
        if '8ball' in installed:
            package.ball(arg)
        else:
            print('Command "8ball" not found.')

    def package(arg):
        try:
            if 'help' in prompt:
                reply = f'''\n    {Icons.PACKAGE} PkgMaster v1.0
    -----------
    {Icons.HELP} help - Shows this message
    {Icons.SUCCESS} get - Installs a package
    {Icons.ERROR} remove - Removes a package
    {Icons.ARROW} list
        -a - Lists available packages
        -i - Lists installed packages
    '''
            elif 'get' in prompt:
                argu = prompt.split('get')[1].strip()
                if not argu == '':
                    if argu in pkgList:
                        reply = f'Installing package "{argu}"'
                        installPackage(argu)
                        time.sleep(0.2)
                    else:
                        reply = f'Incorrect package "{argu}"'
                else:
                    reply = 'Missing package name.'
            elif 'remove' in prompt:
                argu = prompt.split('remove')[1].strip()
                if not argu == '':
                    if argu in installed:
                        reply = f'Uninstalling package "{argu}"'
                        rmpkg(argu)
                        time.sleep(0.2)
                    else:
                        reply = f'Incorrect package "{argu}"'
                else:
                    reply = 'Missing package name.'
            elif 'list -i' in prompt:
                reply = " ".join(installed)
            elif 'list -a' in prompt:
                reply = " ".join(pkgList)
            else:
                reply = 'Incorrect argument. Use "parcel help".'
            print(reply)
        except IndexError:
            print(f"{Colors.ERROR}{Icons.ERROR} {localization.get_string('commands.missing_argument', 'Missing argument')}{Colors.RESET}")

    def cd(arg):
        try:
            os.chdir(arg)
        except FileNotFoundError:
            print(Colors.ERROR + f"Directory '{arg}' not found" + Colors.RESET)
        except NotADirectoryError:
            print(Colors.ERROR + f"'{arg}' is not a directory" + Colors.RESET)

    def ls(arg):
        try:
            files = os.listdir('.' if not arg else arg)
            for f in sorted(files):
                full_path = os.path.join('.' if not arg else arg, f)
                if os.path.isdir(full_path):
                    print(f"{Colors.DIR}{Icons.FOLDER} {f}/{Colors.RESET}")
                else:
                    print(f"{Colors.FILE}{Icons.FILE} {f}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def pwd(arg):
        print(Colors.PATH + os.getcwd() + Colors.RESET)

    def calc(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} {localization.get_string('commands.missing_argument', 'Missing argument')}{Colors.RESET}")
                return
            result = eval(arg)
            print(f"{Colors.SUCCESS}{Icons.CALC} {localization.get_string('commands.calc.result', 'Result')}: {result}{Colors.RESET}")
        except ZeroDivisionError:
            print(Colors.ERROR + "Error: Division by zero" + Colors.RESET)
        except SyntaxError:
            print(Colors.ERROR + "Error: Invalid expression" + Colors.RESET)
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} {localization.get_string('commands.error', 'Error')}: {str(e)}{Colors.RESET}")

    def show_time(arg):
        current_time = d.now()
        print(f"{Colors.SUCCESS}{Icons.TIME} Current date and time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")

    def logout(arg):
        global current_user
        print(f"{Colors.SUCCESS}{Icons.LOGOUT} Logging out...{Colors.RESET}")
        current_user = None
        login_user()

    def adduser(arg):
        if not user_manager.is_admin(current_user):
            # Ты не админ? ХАХАХА, ну ладно, ну с кем не бывает, братанчик!
            print(f"{Colors.ERROR}{Icons.ERROR} Access denied. Root privileges required.{Colors.RESET}")
            return
        try:
            username = input(f"{Colors.INPUT}{Icons.ADD_USER} Enter new username: {Colors.RESET}")
            if not username:
                print(f"{Colors.ERROR}{Icons.ERROR} Username cannot be empty{Colors.RESET}")
                return
            password = input(f"{Colors.INPUT}{Icons.LOGIN} Enter password: {Colors.RESET}")
            is_admin = input(f"{Colors.INPUT}{Icons.SETTINGS} Make admin? (y/N): {Colors.RESET}").lower() == 'y'
            success, message = user_manager.add_user(username, password, is_admin)
            if success:
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} {message}{Colors.RESET}")
            else:
                print(f"{Colors.ERROR}{Icons.ERROR} {message}{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Colors.ERROR}{Icons.ERROR} User creation cancelled{Colors.RESET}")

    def deluser(arg):
        if not user_manager.is_admin(current_user):
            # Ты не админ? ХАХАХА, ну ладно, ну с кем не бывает, братанчик!
            print(f"{Colors.ERROR}{Icons.ERROR} Access denied. Root privileges required.{Colors.RESET}")
            return
        try:
            username = input(f"{Colors.INPUT}{Icons.DEL_USER} Enter username to delete: {Colors.RESET}")
            if username == current_user:
                print(f"{Colors.ERROR}{Icons.ERROR} Cannot delete current user{Colors.RESET}")
                return
            success, message = user_manager.delete_user(username)
            if success:
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} {message}{Colors.RESET}")
            else:
                print(f"{Colors.ERROR}{Icons.ERROR} {message}{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Colors.ERROR}{Icons.ERROR} User deletion cancelled{Colors.RESET}")

    def edit(arg):
        if not arg:
            print(f"{Colors.ERROR}{Icons.ERROR} Usage: edit <filename>{Colors.RESET}")
            return
        edit_command(arg)

    def uname(arg):
        try:
            system = platform.system()
            node = platform.node()
            release = platform.release()
            version = platform.version()
            machine = platform.machine()
            processor = platform.processor()
            
            if not arg:
                # По умолчанию выводим только имя системы
                print(f"{Colors.SUCCESS}{Icons.PC} {system}{Colors.RESET}")
                return
                
            if arg == '-a':
                # Выводим всю информацию
                print(f"{Colors.SUCCESS}{Icons.PC} {system} {node} {release} {version} {machine} {processor}{Colors.RESET}")
            elif arg == '-s':
                print(f"{Colors.SUCCESS}{Icons.PC} {system}{Colors.RESET}")
            elif arg == '-n':
                print(f"{Colors.SUCCESS}{Icons.PC} {node}{Colors.RESET}")
            elif arg == '-r':
                print(f"{Colors.SUCCESS}{Icons.PC} {release}{Colors.RESET}")
            elif arg == '-v':
                print(f"{Colors.SUCCESS}{Icons.PC} {version}{Colors.RESET}")
            elif arg == '-m':
                print(f"{Colors.SUCCESS}{Icons.PC} {machine}{Colors.RESET}")
            elif arg == '-p':
                print(f"{Colors.SUCCESS}{Icons.PC} {processor}{Colors.RESET}")
            elif arg == '-o':
                print(f"{Colors.SUCCESS}{Icons.PC} {system}{Colors.RESET}")
            else:
                print(f"{Colors.ERROR}{Icons.ERROR} Invalid option. Use 'help uname' for usage information.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error getting system information: {str(e)}{Colors.RESET}")

    def cp(arg):
        try:
            args = arg.split()
            if len(args) != 2:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: cp <source> <destination>{Colors.RESET}")
                return
            
            source, dest = args
            import shutil
            
            if os.path.isdir(source):
                shutil.copytree(source, dest)
            else:
                shutil.copy2(source, dest)
            
            print(f"{Colors.SUCCESS}{Icons.COPY} Copied {source} to {dest}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def mv(arg):
        try:
            args = arg.split()
            if len(args) != 2:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: mv <source> <destination>{Colors.RESET}")
                return
            
            source, dest = args
            import shutil
            shutil.move(source, dest)
            print(f"{Colors.SUCCESS}{Icons.MOVE} Moved {source} to {dest}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def rm(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: rm <path> [-r]{Colors.RESET}")
                return
            
            args = arg.split()
            path = args[0]
            recursive = '-r' in args
            
            if os.path.isdir(path):
                if recursive:
                    import shutil
                    shutil.rmtree(path)
                    print(f"{Colors.SUCCESS}{Icons.DELETE} Removed directory {path} and its contents{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}{Icons.ERROR} {path} is a directory. Use -r to remove directories{Colors.RESET}")
            else:
                os.remove(path)
                print(f"{Colors.SUCCESS}{Icons.DELETE} Removed {path}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def mkdir(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: mkdir <directory>{Colors.RESET}")
                return
            
            os.makedirs(arg, exist_ok=True)
            print(f"{Colors.SUCCESS}{Icons.NEW_FOLDER} Created directory {arg}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def touch(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: touch <file>{Colors.RESET}")
                return
            
            with open(arg, 'a'):
                os.utime(arg, None)
            print(f"{Colors.SUCCESS}{Icons.TOUCH} Created/updated {arg}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def cat(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: cat <file>{Colors.RESET}")
                return
            
            with open(arg, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"{Colors.FILE}{Icons.VIEW} File: {arg}{Colors.RESET}\n{content}")
        except UnicodeDecodeError:
            # Пробуем другие кодировки
            encodings = ['cp1251', 'ascii', 'latin1']
            for encoding in encodings:
                try:
                    with open(arg, 'r', encoding=encoding) as f:
                        content = f.read()
                        print(f"{Colors.FILE}{Icons.VIEW} File: {arg}{Colors.RESET}\n{content}")
                        break
                except UnicodeDecodeError:
                    continue
            else:
                print(f"{Colors.ERROR}{Icons.ERROR} Could not decode file {arg}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def find(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: find <pattern> [-d|-f]{Colors.RESET}")
                return

            args = arg.split()
            pattern = args[0]
            only_dirs = '-d' in args
            only_files = '-f' in args

            import fnmatch
            matches = []

            for root, dirnames, filenames in os.walk('.'):
                if only_files:
                    # Ищем только файлы
                    for filename in fnmatch.filter(filenames, pattern):
                        matches.append(os.path.join(root, filename))
                elif only_dirs:
                    # Ищем только директории
                    for dirname in fnmatch.filter(dirnames, pattern):
                        matches.append(os.path.join(root, dirname))
                else:
                    # Ищем и файлы и директории
                    for dirname in fnmatch.filter(dirnames, pattern):
                        matches.append(os.path.join(root, dirname))
                    for filename in fnmatch.filter(filenames, pattern):
                        matches.append(os.path.join(root, filename))

            if matches:
                print(f"{Colors.SUCCESS}{Icons.SEARCH} Found {len(matches)} matches:{Colors.RESET}")
                for match in matches:
                    if os.path.isdir(match):
                        print(f"{Colors.DIR}{Icons.FOLDER} {match}{Colors.RESET}")
                    else:
                        print(f"{Colors.FILE}{Icons.FILE} {match}{Colors.RESET}")
            else:
                print(f"{Colors.WARNING}{Icons.SEARCH} No matches found{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def tree(arg):
        def print_tree(dir_path, prefix="", only_dirs=False):
            entries = os.listdir(dir_path)
            entries = sorted([e for e in entries if not e.startswith('.')])  # Исключаем скрытые файлы
            
            if only_dirs:
                entries = [e for e in entries if os.path.isdir(os.path.join(dir_path, e))]
            
            for i, entry in enumerate(entries):
                full_path = os.path.join(dir_path, entry)
                is_last = i == len(entries) - 1
                
                # Определяем символы для отрисовки дерева
                branch = Icons.LAST_BRANCH if is_last else Icons.BRANCH
                new_prefix = prefix + (Icons.SPACE if is_last else Icons.PIPE)
                
                if os.path.isdir(full_path):
                    print(f"{Colors.DIR}{prefix}{branch} {Icons.FOLDER} {entry}{Colors.RESET}")
                    print_tree(full_path, new_prefix, only_dirs)
                elif not only_dirs:
                    print(f"{Colors.FILE}{prefix}{branch} {Icons.FILE} {entry}{Colors.RESET}")

        try:
            args = arg.split() if arg else ['.']
            path = args[0]
            only_dirs = '-d' in args

            if not os.path.exists(path):
                print(f"{Colors.ERROR}{Icons.ERROR} Directory not found: {path}{Colors.RESET}")
                return

            print(f"{Colors.SUCCESS}{Icons.TREE} Directory tree for: {path}{Colors.RESET}")
            print_tree(path, "", only_dirs)

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def ps(arg):
        try:
            all_processes = '-a' in arg.split() if arg else False
            print(f"{Colors.HEADER}{Icons.PROCESS} Process List:{Colors.RESET}")
            print(f"{'PID':>7} {'CPU%':>6} {'MEM%':>6} {'Name':<20}")
            print("-" * 42)
            
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    if all_processes or pinfo['username'] == os.getlogin():
                        print(f"{pinfo['pid']:>7} {pinfo['cpu_percent']:>6.1f} "
                              f"{pinfo['memory_percent']:>6.1f} {pinfo['name']:<20}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def kill_process(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: kill <pid>{Colors.RESET}")
                return
            
            pid = int(arg)
            process = psutil.Process(pid)
            process.terminate()
            print(f"{Colors.SUCCESS}{Icons.KILL} Process {pid} terminated{Colors.RESET}")
        except psutil.NoSuchProcess:
            print(f"{Colors.ERROR}{Icons.ERROR} Process {pid} not found{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def top(arg):
        try:
            import curses
            def show_top(stdscr):
                curses.start_color()
                curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
                curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
                stdscr.nodelay(1)
                
                while True:
                    stdscr.clear()
                    height, width = stdscr.getmaxyx()
                    
                    # CPU и память
                    cpu_percent = psutil.cpu_percent()
                    mem = psutil.virtual_memory()
                    swap = psutil.swap_memory()
                    
                    stdscr.addstr(0, 0, f"CPU Usage: {cpu_percent}%", curses.color_pair(1))
                    stdscr.addstr(1, 0, f"Memory: {mem.percent}% of {mem.total/1024/1024/1024:.1f}GB", 
                                curses.color_pair(1))
                    
                    # Процессы
                    stdscr.addstr(3, 0, f"{'PID':>7} {'CPU%':>6} {'MEM%':>6} {'Name':<20}", 
                                curses.color_pair(2))
                    row = 4
                    for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                                     key=lambda p: p.info['cpu_percent'],
                                     reverse=True)[:height-5]:
                        try:
                            pinfo = proc.info
                            stdscr.addstr(row, 0, 
                                        f"{pinfo['pid']:>7} {pinfo['cpu_percent']:>6.1f} "
                                        f"{pinfo['memory_percent']:>6.1f} {pinfo['name']:<20}")
                            row += 1
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    
                    stdscr.refresh()
                    ch = stdscr.getch()
                    if ch == ord('q') or ch == ord('Q'):
                        break
                    time.sleep(1)
            
            curses.wrapper(show_top)
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def df(arg):
        try:
            human_readable = '-h' in arg.split() if arg else False
            print(f"{Colors.HEADER}{Icons.DISK} Disk Space Information:{Colors.RESET}")
            print(f"{'Mount':20} {'Total':>10} {'Used':>10} {'Free':>10} {'Use%':>5}")
            print("-" * 58)
            
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    if human_readable:
                        total = f"{usage.total/1024/1024/1024:.1f}G"
                        used = f"{usage.used/1024/1024/1024:.1f}G"
                        free = f"{usage.free/1024/1024/1024:.1f}G"
                    else:
                        total = str(usage.total)
                        used = str(usage.used)
                        free = str(usage.free)
                    
                    print(f"{partition.mountpoint:<20} {total:>10} {used:>10} {free:>10} {usage.percent:>4}%")
                except:
                    continue
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def free(arg):
        try:
            human_readable = '-h' in arg.split() if arg else False
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            def format_bytes(bytes):
                if human_readable:
                    return f"{bytes/1024/1024/1024:.1f}G"
                return str(bytes)
            
            print(f"{Colors.HEADER}{Icons.MEMORY} Memory Information:{Colors.RESET}")
            print(f"{'Type':7} {'Total':>10} {'Used':>10} {'Free':>10} {'Use%':>5}")
            print("-" * 45)
            print(f"Memory {format_bytes(memory.total):>10} "
                  f"{format_bytes(memory.used):>10} "
                  f"{format_bytes(memory.free):>10} "
                  f"{memory.percent:>4}%")
            print(f"Swap   {format_bytes(swap.total):>10} "
                  f"{format_bytes(swap.used):>10} "
                  f"{format_bytes(swap.free):>10} "
                  f"{swap.percent:>4}%")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def uptime(arg):
        try:
            uptime = time.time() - psutil.boot_time()
            uptime_str = str(timedelta(seconds=int(uptime)))
            boot_time = d.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{Colors.SUCCESS}{Icons.CLOCK} System uptime: {uptime_str}")
            print(f"{Colors.SUCCESS}{Icons.CLOCK} Boot time: {boot_time}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def netstat(arg):
        try:
            print(f"{Colors.HEADER}{Icons.NETWORK} Network Connections:{Colors.RESET}")
            print(f"{'Proto':6} {'Local Address':21} {'Remote Address':21} {'Status':11}")
            print("-" * 62)
            
            for conn in psutil.net_connections(kind='inet'):
                try:
                    proto = 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP'
                    laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "*:*"
                    raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "*:*"
                    status = conn.status if conn.status else 'NONE'
                    print(f"{proto:<6} {laddr:21} {raddr:21} {status:11}")
                except:
                    continue
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def ping_host(arg):
        try:
            args = arg.split()
            if not args:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: ping <host> [-c count]{Colors.RESET}")
                return
            
            host = args[0]
            count = 4  # По умолчанию 4 пинга
            if len(args) > 2 and args[1] == '-c':
                count = int(args[2])
            
            print(f"{Colors.HEADER}{Icons.PING} Pinging {host}...{Colors.RESET}")
            for i in range(count):
                try:
                    delay = ping3.ping(host)
                    if delay is not None:
                        print(f"{Colors.SUCCESS}Reply from {host}: time={delay*1000:.1f}ms{Colors.RESET}")
                    else:
                        print(f"{Colors.ERROR}Request timed out{Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.ERROR}Error: {str(e)}{Colors.RESET}")
                time.sleep(1)
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def zip_files(arg):
        try:
            args = arg.split()
            if len(args) < 2:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: zip <archive.zip> <files...> [-r]{Colors.RESET}")
                return

            archive_name = args[0]
            recursive = '-r' in args
            files = [f for f in args[1:] if f != '-r']

            with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file in files:
                    if os.path.isdir(file) and recursive:
                        for root, _, filenames in os.walk(file):
                            for filename in filenames:
                                filepath = os.path.join(root, filename)
                                arcname = os.path.relpath(filepath, os.path.dirname(file))
                                zf.write(filepath, arcname)
                                print(f"{Colors.SUCCESS}{Icons.ZIP} Adding: {filepath}{Colors.RESET}")
                    elif os.path.isfile(file):
                        zf.write(file)
                        print(f"{Colors.SUCCESS}{Icons.ZIP} Adding: {file}{Colors.RESET}")
                    else:
                        print(f"{Colors.WARNING}{Icons.WARNING} Skipping: {file}{Colors.RESET}")

            print(f"{Colors.SUCCESS}{Icons.ZIP} Archive created: {archive_name}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def unzip_files(arg):
        try:
            args = arg.split()
            if not args:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: unzip <archive.zip> [destination]{Colors.RESET}")
                return

            archive_name = args[0]
            extract_dir = args[1] if len(args) > 1 else '.'

            with zipfile.ZipFile(archive_name, 'r') as zf:
                zf.extractall(extract_dir)
                for filename in zf.namelist():
                    print(f"{Colors.SUCCESS}{Icons.UNZIP} Extracting: {filename}{Colors.RESET}")

            print(f"{Colors.SUCCESS}{Icons.UNZIP} Archive extracted to: {extract_dir}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def tar_archive(arg):
        try:
            args = arg.split()
            if len(args) < 2:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: tar [-c|-x] -f <archive.tar> [files...]{Colors.RESET}")
                return

            mode = None
            archive_name = None
            files = []

            i = 0
            while i < len(args):
                if args[i] == '-c':
                    mode = 'w'
                elif args[i] == '-x':
                    mode = 'r'
                elif args[i] == '-f':
                    i += 1
                    if i < len(args):
                        archive_name = args[i]
                else:
                    files.append(args[i])
                i += 1

            if not mode or not archive_name:
                print(f"{Colors.ERROR}{Icons.ERROR} Invalid arguments{Colors.RESET}")
                return

            if mode == 'w':
                with tarfile.open(archive_name, mode) as tar:
                    for file in files:
                        tar.add(file)
                        print(f"{Colors.SUCCESS}{Icons.COMPRESS} Adding: {file}{Colors.RESET}")
                print(f"{Colors.SUCCESS}{Icons.COMPRESS} Archive created: {archive_name}{Colors.RESET}")
            else:
                with tarfile.open(archive_name, mode) as tar:
                    tar.extractall()
                    for member in tar.getmembers():
                        print(f"{Colors.SUCCESS}{Icons.EXTRACT} Extracting: {member.name}{Colors.RESET}")
                print(f"{Colors.SUCCESS}{Icons.EXTRACT} Archive extracted{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def gzip_file(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: gzip <file>{Colors.RESET}")
                return

            input_file = arg
            output_file = input_file + '.gz'

            with open(input_file, 'rb') as f_in:
                with gzip.open(output_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                    print(f"{Colors.SUCCESS}{Icons.COMPRESS} Compressed: {input_file} -> {output_file}{Colors.RESET}")

            os.remove(input_file)  # Удаляем исходный файл, как это делает настоящий gzip

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def gunzip_file(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: gunzip <file.gz>{Colors.RESET}")
                return

            input_file = arg
            if not input_file.endswith('.gz'):
                print(f"{Colors.ERROR}{Icons.ERROR} Not a gzip file: {input_file}{Colors.RESET}")
                return

            output_file = input_file[:-3]  # Удаляем .gz из имени файла

            with gzip.open(input_file, 'rb') as f_in:
                with open(output_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                    print(f"{Colors.SUCCESS}{Icons.EXTRACT} Decompressed: {input_file} -> {output_file}{Colors.RESET}")

            os.remove(input_file)  # Удаляем сжатый файл, как это делает настоящий gunzip

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def grep(arg):
        try:
            args = arg.split()
            if len(args) < 2:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: grep <pattern> <file> [-i] [-n]{Colors.RESET}")
                return

            pattern = args[0]
            filename = args[1]
            case_insensitive = '-i' in args
            show_numbers = '-n' in args
            
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                with open(filename, 'r', encoding='cp1251') as f:
                    lines = f.readlines()

            found = False
            for i, line in enumerate(lines, 1):
                if case_insensitive:
                    match = pattern.lower() in line.lower()
                else:
                    match = pattern in line
                
                if match:
                    found = True
                    line = line.rstrip('\n')
                    if show_numbers:
                        print(f"{Colors.SUCCESS}{i:4d}{Colors.RESET}: {line}")
                    else:
                        print(line)

            if not found:
                print(f"{Colors.WARNING}{Icons.SEARCH_TEXT} Pattern not found{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def sort_file(arg):
        try:
            args = arg.split()
            if not args:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: sort <file> [-r] [-n]{Colors.RESET}")
                return

            filename = args[0]
            reverse = '-r' in args
            numeric = '-n' in args

            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if numeric:
                # Пытаемся преобразовать строки в числа для сортировки
                lines.sort(key=lambda x: float(x.strip()), reverse=reverse)
            else:
                lines.sort(reverse=reverse)

            print(f"{Colors.SUCCESS}{Icons.SORT} Sorted content:{Colors.RESET}")
            for line in lines:
                print(line.rstrip('\n'))

        except ValueError:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: Invalid numeric data for -n option{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def wc(arg):
        try:
            args = arg.split()
            if not args:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: wc <file> [-l] [-w] [-c]{Colors.RESET}")
                return

            filename = args[0]
            show_lines = '-l' in args or len(args) == 1
            show_words = '-w' in args or len(args) == 1
            show_bytes = '-c' in args or len(args) == 1

            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.count('\n') + (not content.endswith('\n') and len(content) > 0)
                words = len(content.split())
                bytes = len(content.encode('utf-8'))

            results = []
            if show_lines:
                results.append(f"{lines:8d} lines")
            if show_words:
                results.append(f"{words:8d} words")
            if show_bytes:
                results.append(f"{bytes:8d} bytes")

            print(f"{Colors.SUCCESS}{Icons.COUNT} {' '.join(results)} {filename}{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def diff(arg):
        try:
            args = arg.split()
            if len(args) != 2:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: diff <file1> <file2>{Colors.RESET}")
                return

            file1, file2 = args

            with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
                lines1 = f1.readlines()
                lines2 = f2.readlines()

            differ = difflib.Differ()
            diff = list(differ.compare(lines1, lines2))
            
            if all(line.startswith('  ') for line in diff):
                print(f"{Colors.SUCCESS}{Icons.DIFF} Files are identical{Colors.RESET}")
                return

            print(f"{Colors.HEADER}{Icons.DIFF} Comparing {file1} with {file2}:{Colors.RESET}")
            for line in diff:
                if line.startswith('+ '):
                    print(f"{Colors.SUCCESS}{line.rstrip()}{Colors.RESET}")
                elif line.startswith('- '):
                    print(f"{Colors.ERROR}{line.rstrip()}{Colors.RESET}")
                elif not line.startswith('? '):  # Пропускаем строки с подсказками
                    print(line.rstrip())

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def head(arg):
        try:
            args = arg.split()
            if not args:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: head <file> [-n lines]{Colors.RESET}")
                return

            filename = args[0]
            num_lines = 10  # По умолчанию 10 строк

            if len(args) > 2 and args[1] == '-n':
                try:
                    num_lines = int(args[2])
                except ValueError:
                    print(f"{Colors.ERROR}{Icons.ERROR} Invalid number of lines{Colors.RESET}")
                    return

            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:num_lines]

            print(f"{Colors.SUCCESS}{Icons.HEAD} First {num_lines} lines of {filename}:{Colors.RESET}")
            for line in lines:
                print(line.rstrip('\n'))

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def tail(arg):
        try:
            args = arg.split()
            if not args:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: tail <file> [-n lines]{Colors.RESET}")
                return

            filename = args[0]
            num_lines = 10  # По умолчанию 10 строк

            if len(args) > 2 and args[1] == '-n':
                try:
                    num_lines = int(args[2])
                except ValueError:
                    print(f"{Colors.ERROR}{Icons.ERROR} Invalid number of lines{Colors.RESET}")
                    return

            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-num_lines:]

            print(f"{Colors.SUCCESS}{Icons.TAIL} Last {num_lines} lines of {filename}:{Colors.RESET}")
            for line in lines:
                print(line.rstrip('\n'))

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def wget(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: wget <url> [output filename]{Colors.RESET}")
                return

            args = arg.split()
            url = args[0]
            
            # Определяем имя файла из URL если не указано
            if len(args) > 1:
                output_file = args[1]
            else:
                output_file = os.path.basename(urlparse(url).path)
                if not output_file:
                    output_file = 'downloaded_file'

            print(f"{Colors.SUCCESS}{Icons.NETWORK} Downloading {url}...{Colors.RESET}")
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            downloaded = 0

            with open(output_file, 'wb') as f:
                for data in response.iter_content(block_size):
                    f.write(data)
                    downloaded += len(data)
                    if total_size > 0:
                        percent = (downloaded * 100) / total_size
                        print(f"\rProgress: {percent:.1f}%", end='')

            print(f"\n{Colors.SUCCESS}{Icons.SUCCESS} Downloaded to {output_file}{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Download failed: {str(e)}{Colors.RESET}")

    def curl(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: curl [-X METHOD] [-H 'header: value'] [-d 'data'] <url>{Colors.RESET}")
                return

            args = arg.split()
            method = 'GET'
            headers = {}
            data = None
            url = args[-1]  # URL всегда последний аргумент

            i = 0
            while i < len(args) - 1:
                if args[i] == '-X':
                    method = args[i + 1]
                    i += 2
                elif args[i] == '-H':
                    header_parts = args[i + 1].split(': ')
                    headers[header_parts[0]] = header_parts[1]
                    i += 2
                elif args[i] == '-d':
                    data = args[i + 1]
                    i += 2
                else:
                    i += 1

            response = requests.request(method, url, headers=headers, data=data)
            
            print(f"{Colors.SUCCESS}{Icons.NETWORK} Response Status: {response.status_code}{Colors.RESET}")
            print("\nHeaders:")
            for header, value in response.headers.items():
                print(f"{header}: {value}")
            
            print("\nBody:")
            print(response.text)

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Request failed: {str(e)}{Colors.RESET}")

    def ifconfig(arg):
        try:
            interfaces = netifaces.interfaces()
            
            for iface in interfaces:
                print(f"\n{Colors.SUCCESS}{Icons.NETWORK} Interface: {iface}{Colors.RESET}")
                
                # MAC адрес
                try:
                    mac = netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]
                    print(f"    MAC Address: {mac['addr']}")
                except KeyError:
                    pass
                
                # IPv4
                try:
                    ipv4 = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
                    print(f"    IPv4 Address: {ipv4['addr']}")
                    print(f"    Netmask: {ipv4['netmask']}")
                except KeyError:
                    pass
                
                # IPv6
                try:
                    ipv6 = netifaces.ifaddresses(iface)[netifaces.AF_INET6][0]
                    print(f"    IPv6 Address: {ipv6['addr']}")
                except KeyError:
                    pass

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error getting network information: {str(e)}{Colors.RESET}")

    def ssh(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: ssh <username>@<host> [-p port]{Colors.RESET}")
                return

            args = arg.split()
            connection_string = args[0]
            port = 22

            if len(args) > 2 and args[1] == '-p':
                port = int(args[2])

            username, host = connection_string.split('@')
            
            # Запрос пароля
            import getpass
            password = getpass.getpass('Password: ')

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            print(f"{Colors.SUCCESS}{Icons.NETWORK} Connecting to {host}...{Colors.RESET}")
            client.connect(host, port=port, username=username, password=password)
            
            channel = client.invoke_shell()
            print(f"{Colors.SUCCESS}{Icons.SUCCESS} Connected! Use 'exit' to disconnect.{Colors.RESET}")

            # Интерактивная сессия
            while True:
                if channel.recv_ready():
                    output = channel.recv(1024).decode('utf-8')
                    print(output, end='')
                
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    cmd = sys.stdin.readline()
                    if cmd.strip() == 'exit':
                        break
                    channel.send(cmd)

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} SSH connection failed: {str(e)}{Colors.RESET}")
        finally:
            try:
                client.close()
            except:
                pass

    def scp(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: scp <source> <user>@<host>:<destination> [-p port]{Colors.RESET}")
                return

            args = arg.split()
            source = args[0]
            target = args[1]
            port = 22

            if len(args) > 3 and args[2] == '-p':
                port = int(args[3])

            # Парсинг целевого пути
            user_host, remote_path = target.split(':')
            username, host = user_host.split('@')

            # Запрос пароля
            import getpass
            password = getpass.getpass('Password: ')

            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            
            sftp = paramiko.SFTPClient.from_transport(transport)
            
            print(f"{Colors.SUCCESS}{Icons.NETWORK} Copying {source} to {host}:{remote_path}...{Colors.RESET}")
            sftp.put(source, remote_path, callback=lambda x, y: print(f"\rProgress: {(x/y)*100:.1f}%", end=''))
            
            print(f"\n{Colors.SUCCESS}{Icons.SUCCESS} File transferred successfully{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} SCP transfer failed: {str(e)}{Colors.RESET}")
        finally:
            try:
                sftp.close()
                transport.close()
            except:
                pass

    def history(arg):
        try:
            args = arg.split()
            if not args:
                # Показать всю историю
                for i, cmd in enumerate(command_history, 1):
                    print(f"{Colors.SUCCESS}{i:4d}{Colors.RESET}  {cmd}")
            elif args[0] == '-c':
                # Очистить историю
                command_history.clear()
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} History cleared{Colors.RESET}")
            elif args[0].startswith('!'):
                # Выполнить команду из истории
                try:
                    if args[0] == '!!':
                        # Выполнить последнюю команду
                        index = len(command_history) - 1
                    else:
                        # Выполнить команду по номеру
                        index = int(args[0][1:]) - 1
                    
                    if 0 <= index < len(command_history):
                        cmd = command_history[index]
                        print(f"Executing: {cmd}")
                        commandInput = cmd.split()
                        command = commandInput[0].lower()
                        arg = ' '.join(commandInput[1:]) if len(commandInput) > 1 else ''
                        if command in commandList:
                            commandList[command](arg)
                        else:
                            print(f"{Colors.ERROR}{Icons.ERROR} Command not found: {command}{Colors.RESET}")
                    else:
                        print(f"{Colors.ERROR}{Icons.ERROR} Invalid history index{Colors.RESET}")
                except ValueError:
                    print(f"{Colors.ERROR}{Icons.ERROR} Invalid history reference{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def alias(arg):
        try:
            args = arg.split()
            if not args:
                # Показать все псевдонимы
                for alias, command in aliases.items():
                    print(f"{Colors.SUCCESS}{alias}{Colors.RESET}={command}")
                return

            if '=' in arg:
                # Создать новый псевдоним
                alias, command = arg.split('=', 1)
                alias = alias.strip()
                command = command.strip().strip("'\"")
                aliases[alias] = command
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} Alias created: {alias} -> {command}{Colors.RESET}")
            elif args[0] == '-r' and len(args) > 1:
                # Удалить псевдоним
                alias = args[1]
                if alias in aliases:
                    del aliases[alias]
                    print(f"{Colors.SUCCESS}{Icons.SUCCESS} Alias removed: {alias}{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}{Icons.ERROR} Alias not found: {alias}{Colors.RESET}")
            else:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: alias [name=command] [-r alias]{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def cron(arg):
        try:
            args = arg.split()
            if not args:
                # Показать все задачи
                for job_id, job in cron_jobs.items():
                    print(f"{Colors.SUCCESS}{job_id}{Colors.RESET}: {job['schedule']} -> {job['command']}")
                return

            if args[0] == 'add':
                # cron add "* * * * *" command arg1 arg2...
                if len(args) < 3:
                    print(f"{Colors.ERROR}{Icons.ERROR} Usage: cron add 'schedule' command [args...]{Colors.RESET}")
                    return
                
                schedule_str = args[1]
                command = args[2]
                command_args = ' '.join(args[3:])
                
                job_id = str(len(cron_jobs) + 1)
                cron_jobs[job_id] = {
                    'schedule': schedule_str,
                    'command': f"{command} {command_args}",
                    'job': schedule.every().day.at(schedule_str).do(
                        lambda: commandList[command](command_args) if command in commandList else None
                    )
                }
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} Job added with ID: {job_id}{Colors.RESET}")
                
            elif args[0] == 'remove' and len(args) > 1:
                # Удалить задачу
                job_id = args[1]
                if job_id in cron_jobs:
                    schedule.cancel_job(cron_jobs[job_id]['job'])
                    del cron_jobs[job_id]
                    print(f"{Colors.SUCCESS}{Icons.SUCCESS} Job removed: {job_id}{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}{Icons.ERROR} Job not found: {job_id}{Colors.RESET}")
            else:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: cron [add|remove] [parameters...]{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def man(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: man <command>{Colors.RESET}")
                return

            command = arg.lower()
            if command in helpList:
                # Форматируем документацию в стиле man
                print(f"{Colors.HEADER}COMMAND{Colors.RESET}")
                print(f"    {command} - {helpList[command].strip()}")
                print(f"\n{Colors.HEADER}DESCRIPTION{Colors.RESET}")
                print(helpList[command])
            else:
                print(f"{Colors.ERROR}{Icons.ERROR} No manual entry for {command}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def which(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: which <command>{Colors.RESET}")
                return

            command = arg.lower()
            if command in commandList:
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} {command}: built-in command{Colors.RESET}")
            elif command in aliases:
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} {command}: aliased to '{aliases[command]}'{Colors.RESET}")
            else:
                # Поиск в системных путях
                paths = env_vars.get('PATH', '').split(os.pathsep)
                found = False
                for path in paths:
                    exec_path = os.path.join(path, command)
                    if os.path.isfile(exec_path) and os.access(exec_path, os.X_OK):
                        print(f"{Colors.SUCCESS}{exec_path}{Colors.RESET}")
                        found = True
                        break
                
                if not found:
                    print(f"{Colors.ERROR}{Icons.ERROR} {command} not found{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def export(arg):
        try:
            if not arg:
                # Показать все переменные окружения
                for key, value in sorted(env_vars.items()):
                    print(f"{Colors.SUCCESS}{key}{Colors.RESET}={value}")
                return

            if '=' in arg:
                # Установить переменную
                key, value = arg.split('=', 1)
                key = key.strip()
                value = value.strip().strip("'\"")
                env_vars[key] = value
                os.environ[key] = value
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} Environment variable set: {key}={value}{Colors.RESET}")
            elif arg.startswith('-u '):
                # Удалить переменную
                key = arg[3:].strip()
                if key in env_vars:
                    del env_vars[key]
                    if key in os.environ:
                        del os.environ[key]
                    print(f"{Colors.SUCCESS}{Icons.SUCCESS} Environment variable unset: {key}{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}{Icons.ERROR} Environment variable not found: {key}{Colors.RESET}")
            else:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: export [name=value] [-u name]{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def weather(arg):
        try:
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: weather <city>{Colors.RESET}")
                return
            
            # Используем OpenWeatherMap API
            API_KEY = '9f90021d8b23784b389c1ffb2ef577af'
            # Кодируем название города для URL
            city = requests.utils.quote(arg)
            # Добавляем языковой параметр для русского языка
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
            
            response = requests.get(url)
            
            if response.status_code == 401:
                print(f"{Colors.ERROR}{Icons.ERROR} Invalid API key{Colors.RESET}")
                return
                
            if response.status_code == 404:
                print(f"{Colors.ERROR}{Icons.ERROR} City '{arg}' not found{Colors.RESET}")
                return
                
            if response.status_code != 200:
                print(f"{Colors.ERROR}{Icons.ERROR} API Error: {response.status_code}{Colors.RESET}")
                return
                
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            
            print(f"\n{Colors.SUCCESS}Weather in {arg}:{Colors.RESET}")
            print(f"Temperature: {temp}°C (feels like {feels_like}°C)")
            print(f"Conditions: {weather}")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind} m/s")
            
        except requests.exceptions.ConnectionError:
            print(f"{Colors.ERROR}{Icons.ERROR} Connection error. Check your internet connection{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def todo(arg):
        try:
            args = arg.split()
            conn = sqlite3.connect(todo_db)
            c = conn.cursor()
            
            if not args:
                # Показать все задачи
                c.execute("SELECT * FROM todos")
                tasks = c.fetchall()
                if tasks:
                    print(f"\n{Colors.SUCCESS}Todo List:{Colors.RESET}")
                    for task in tasks:
                        status = "✓" if task[2] == 'done' else "☐"
                        due = f" (Due: {task[3]})" if task[3] else ""
                        print(f"{Colors.SUCCESS}{status} {task[0]}.{Colors.RESET} {task[1]}{due}")
                else:
                    print(f"{Colors.WARNING}No tasks found{Colors.RESET}")
            
            elif args[0] == 'add':
                # Добавить задачу
                task = ' '.join(args[1:])
                if '--due' in task:
                    task, due_date = task.split('--due')
                    due_date = due_date.strip()
                else:
                    due_date = None
                c.execute("INSERT INTO todos (task, status, due_date) VALUES (?, ?, ?)",
                         (task.strip(), 'pending', due_date))
                conn.commit()
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} Task added{Colors.RESET}")
            
            elif args[0] == 'done':
                # Отметить задачу как выполненную
                task_id = args[1]
                c.execute("UPDATE todos SET status = 'done' WHERE id = ?", (task_id,))
                conn.commit()
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} Task marked as done{Colors.RESET}")
            
            elif args[0] == 'del':
                # Удалить задачу
                task_id = args[1]
                c.execute("DELETE FROM todos WHERE id = ?", (task_id,))
                conn.commit()
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} Task deleted{Colors.RESET}")
            
            conn.close()
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def note(arg):
        try:
            args = arg.split()
            conn = sqlite3.connect(notes_db)
            c = conn.cursor()
            
            if not args:
                # Показать все заметки
                c.execute("SELECT * FROM notes")
                notes = c.fetchall()
                if notes:
                    print(f"\n{Colors.SUCCESS}Notes:{Colors.RESET}")
                    for note in notes:
                        print(f"\n{Colors.SUCCESS}{note[0]}. {note[1]}{Colors.RESET}")
                        print(f"Created: {note[3]}")
                        print("-" * 40)
                        print(note[2])
                else:
                    print(f"{Colors.WARNING}No notes found{Colors.RESET}")
            
            elif args[0] == 'add':
                # Добавить заметку
                title = input(f"{Colors.INPUT}Title: {Colors.RESET}")
                print("Enter content (Ctrl+D or Ctrl+Z to finish):")
                content_lines = []
                while True:
                    try:
                        line = input()
                        content_lines.append(line)
                    except EOFError:
                        break
                content = '\n'.join(content_lines)
                created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                c.execute("INSERT INTO notes (title, content, created_date) VALUES (?, ?, ?)",
                         (title, content, created_date))
                conn.commit()
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} Note added{Colors.RESET}")
            
            elif args[0] == 'del':
                # Удалить заметку
                note_id = args[1]
                c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
                conn.commit()
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} Note deleted{Colors.RESET}")
            
            elif args[0] == 'edit':
                # Редактировать заметку
                note_id = args[1]
                c.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
                note = c.fetchone()
                if note:
                    print(f"Current title: {note[1]}")
                    print("Current content:")
                    print(note[2])
                    print("\nEnter new content (Ctrl+D or Ctrl+Z to finish):")
                    content_lines = []
                    while True:
                        try:
                            line = input()
                            content_lines.append(line)
                        except EOFError:
                            break
                    new_content = '\n'.join(content_lines)
                    
                    c.execute("UPDATE notes SET content = ? WHERE id = ?",
                             (new_content, note_id))
                    conn.commit()
                    print(f"{Colors.SUCCESS}{Icons.SUCCESS} Note updated{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}{Icons.ERROR} Note not found{Colors.RESET}")
            
            conn.close()
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def calendar_cmd(arg):
        try:
            args = arg.split()
            now = datetime.now()
            
            if not args:
                # Показать календарь текущего месяца
                month = now.month
                year = now.year
            else:
                try:
                    month = int(args[0])
                    year = int(args[1]) if len(args) > 1 else now.year
                except ValueError:
                    print(f"{Colors.ERROR}{Icons.ERROR} Invalid month/year format{Colors.RESET}")
                    return
            
            # Получаем календарь
            cal_data = cal.monthcalendar(year, month)
            month_name = cal.month_name[month]
            
            # Форматируем вывод
            print(f"\n{Colors.SUCCESS}{month_name} {year}{Colors.RESET}")
            print("Mo Tu We Th Fr Sa Su")
            
            for week in cal_data:
                for day in week:
                    if day == 0:
                        print("  ", end=" ")
                    elif day == now.day and month == now.month and year == now.year:
                        print(f"{Colors.SUCCESS}{day:2d}{Colors.RESET}", end=" ")
                    else:
                        print(f"{day:2d}", end=" ")
                print()
            
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def timer(arg):
        try:
            args = arg.split()
            global timer_threads
            
            def countdown(duration):
                start_time = time.time()
                while time.time() - start_time < duration:
                    remaining = duration - (time.time() - start_time)
                    mins, secs = divmod(int(remaining), 60)
                    hours, mins = divmod(mins, 60)
                    timeformat = f"{hours:02d}:{mins:02d}:{secs:02d}"
                    print(f"\r{Colors.SUCCESS}Time remaining: {timeformat}{Colors.RESET}", end='')
                    time.sleep(1)
                print(f"\n{Colors.SUCCESS}{Icons.SUCCESS} Timer finished!{Colors.RESET}")
            
            if not args:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: timer <start|stop> [duration in seconds]{Colors.RESET}")
                return
            
            if args[0] == 'start':
                if len(args) < 2:
                    print(f"{Colors.ERROR}{Icons.ERROR} Please specify duration{Colors.RESET}")
                    return
                    
                duration = int(args[1])
                timer_thread = threading.Thread(target=countdown, args=(duration,))
                timer_thread.daemon = True
                timer_thread.start()
                timer_threads['timer'] = timer_thread
                
            elif args[0] == 'stop':
                if 'timer' in timer_threads:
                    # Timer threads are daemon threads and will be stopped automatically
                    timer_threads.pop('timer')
                    print(f"{Colors.SUCCESS}{Icons.SUCCESS} Timer stopped{Colors.RESET}")
                    
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

    def stopwatch(arg):
        try:
            global stopwatch_start
            
            if not arg:
                print(f"{Colors.ERROR}{Icons.ERROR} Usage: stopwatch <start|stop|lap>{Colors.RESET}")
                return
                
            if arg == 'start':
                stopwatch_start = time.time()
                print(f"{Colors.SUCCESS}{Icons.SUCCESS} Stopwatch started{Colors.RESET}")
                
            elif arg == 'stop':
                if stopwatch_start:
                    elapsed = time.time() - stopwatch_start
                    mins, secs = divmod(int(elapsed), 60)
                    hours, mins = divmod(mins, 60)
                    timeformat = f"{hours:02d}:{mins:02d}:{secs:02d}"
                    print(f"{Colors.SUCCESS}Total time: {timeformat}{Colors.RESET}")
                    stopwatch_start = None
                else:
                    print(f"{Colors.ERROR}{Icons.ERROR} Stopwatch not started{Colors.RESET}")
                    
            elif arg == 'lap':
                if stopwatch_start:
                    elapsed = time.time() - stopwatch_start
                    mins, secs = divmod(int(elapsed), 60)
                    hours, mins = divmod(mins, 60)
                    timeformat = f"{hours:02d}:{mins:02d}:{secs:02d}"
                    print(f"{Colors.SUCCESS}Lap time: {timeformat}{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}{Icons.ERROR} Stopwatch not started{Colors.RESET}")
                    
        except Exception as e:
            print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")

commandList = {
    'quit': commands.kill,
    'help': commands.helpme,
    'whoami': commands.whoami,
    'clear': commands.clear,
    'cls': commands.clear,
    'ver': commands.version,
    'echo': commands.echo,
    'parcel': commands.package,
    'fig': commands.cfiglet,
    '8ball': commands.cball,
    'cd': commands.cd,
    'ls': commands.ls,
    'pwd': commands.pwd,
    'calc': commands.calc,
    'time': commands.show_time,
    'logout': commands.logout,
    'adduser': commands.adduser,
    'deluser': commands.deluser,
    'edit': commands.edit,
    'uname': commands.uname,
    'cp': commands.cp,
    'mv': commands.mv,
    'rm': commands.rm,
    'mkdir': commands.mkdir,
    'touch': commands.touch,
    'cat': commands.cat,
    'find': commands.find,
    'tree': commands.tree,
    'ps': commands.ps,
    'kill': commands.kill_process,
    'top': commands.top,
    'df': commands.df,
    'free': commands.free,
    'uptime': commands.uptime,
    'netstat': commands.netstat,
    'ping': commands.ping_host,
    'zip': commands.zip_files,
    'unzip': commands.unzip_files,
    'tar': commands.tar_archive,
    'gzip': commands.gzip_file,
    'gunzip': commands.gunzip_file,
    'grep': commands.grep,
    'sort': commands.sort_file,
    'wc': commands.wc,
    'diff': commands.diff,
    'head': commands.head,
    'tail': commands.tail,
    'wget': commands.wget,
    'curl': commands.curl,
    'ifconfig': commands.ifconfig,
    'ssh': commands.ssh,
    'scp': commands.scp,
    'history': commands.history,
    'alias': commands.alias,
    'cron': commands.cron,
    'man': commands.man,
    'which': commands.which,
    'export': commands.export,
    'weather': commands.weather,
    'todo': commands.todo,
    'note': commands.note,
    'calendar': commands.calendar_cmd,
    'timer': commands.timer,
    'stopwatch': commands.stopwatch,
}

# Получение укороченного пути для prompt
def get_shortened_path():
    current = os.getcwd()
    home = os.path.expanduser("~")
    if current.startswith(home):
        current = f"{Icons.HOME}" + current[len(home):]
    if len(current) > 30:
        parts = current.split(os.sep)
        if len(parts) > 3:
            current = os.sep.join(['', '...'] + parts[-2:])
    return current

class NanoEditor:
    def __init__(self, filename):
        self.filename = filename
        self.content = ['']  # Инициализируем с пустой строкой
        self.current_line = 0
        self.current_col = 0
        self.offset_y = 0
        self.status_message = ""
        self.clipboard = []
        self.modified = False
        self.load_file()

    def load_file(self):
        try:
            if os.path.exists(self.filename):
                encodings = ['utf-8', 'cp1251', 'ascii', 'latin1']
                content = None
                for enc in encodings:
                    try:
                        with open(self.filename, 'r', encoding=enc) as f:
                            content = f.readlines()
                        break
                    except UnicodeDecodeError:
                        continue
                
                if content:
                    # Убеждаемся, что файл всегда содержит хотя бы одну строку
                    self.content = content if content else ['']
                    # Добавляем \n в конец строк, если их нет
                    self.content = [line if line.endswith('\n') else line + '\n' 
                                  for line in self.content]
            else:
                self.content = ['']
                self.status_message = "New File"
        except Exception as e:
            self.status_message = f"Error loading file: {str(e)}"
            self.content = ['']

    def save_file(self):
        try:
            with open(self.filename, 'w', encoding='utf-8', newline='') as f:
                f.writelines(self.content)
            self.status_message = "File saved successfully"
            self.modified = False
            return True
        except Exception as e:
            self.status_message = f"Error saving file: {str(e)}"
            return False

    def ensure_valid_position(self):
        """Проверяет и корректирует позицию курсора"""
        # Убеждаемся, что есть хотя бы одна строка
        if not self.content:
            self.content = ['']
        
        # Проверяем текущую строку
        self.current_line = max(0, min(self.current_line, len(self.content) - 1))
        
        # Проверяем текущую колонку
        current_line_length = len(self.content[self.current_line].rstrip('\n'))
        self.current_col = max(0, min(self.current_col, current_line_length))
        
        # Проверяем смещение
        max_offset = max(0, len(self.content) - 1)
        self.offset_y = max(0, min(self.offset_y, max_offset))

    def insert_char(self, char):
        if not self.content:
            self.content = ['']
        
        current = self.content[self.current_line]
        if not current.endswith('\n'):
            current += '\n'
        
        self.content[self.current_line] = (
            current[:self.current_col] + 
            char + 
            current[self.current_col:]
        )
        self.current_col += 1 if char != '\n' else 0
        self.modified = True
        self.ensure_valid_position()

    def handle_backspace(self):
        if self.current_col > 0:
            current = self.content[self.current_line]
            self.content[self.current_line] = current[:self.current_col-1] + current[self.current_col:]
            self.current_col -= 1
            self.modified = True
        elif self.current_line > 0:
            # Сохраняем текущую строку
            current = self.content.pop(self.current_line)
            self.current_line -= 1
            # Получаем предыдущую строку без \n
            prev_line = self.content[self.current_line].rstrip('\n')
            self.current_col = len(prev_line)
            # Объединяем строки
            self.content[self.current_line] = prev_line + current
            self.modified = True
        
        self.ensure_valid_position()

def run_editor(stdscr, filename):
    # Инициализация цветов
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
    
    # Настройка экрана для поддержки Unicode
    if os.name == 'nt':  # Для Windows
        os.system('chcp 65001')
    
    # Настройка экрана
    curses.curs_set(1)  # Показываем курсор
    stdscr.timeout(100)  # Таймаут для getch()
    
    editor = NanoEditor(filename)
    
    # Получаем размеры экрана
    max_y, max_x = stdscr.getmaxyx()
    
    # Создаем окна
    header = curses.newwin(1, max_x, 0, 0)
    main_win = curses.newwin(max_y-3, max_x, 1, 0)
    status = curses.newwin(1, max_x, max_y-2, 0)
    help_win = curses.newwin(1, max_x, max_y-1, 0)
    
    main_win.keypad(True)

    def safe_addstr(win, y, x, string, *args):
        """Безопасное добавление строки в окно"""
        try:
            # Преобразуем все специальные символы в безопасные ASCII
            safe_string = string.encode('ascii', 'replace').decode('ascii')
            win.addstr(y, x, safe_string, *args)
        except curses.error:
            pass
    
    def draw_interface():
        # Отрисовка заголовка
        header.bkgd(' ', curses.color_pair(2))
        safe_addstr(header, 0, 0, f" {filename} {' (modified)' if editor.modified else ''}")
        header.refresh()
        
        # Отрисовка статуса
        status.bkgd(' ', curses.color_pair(1))
        pos_info = f" Line: {editor.current_line+1}/{len(editor.content)}  Col: {editor.current_col+1} "
        safe_addstr(status, 0, 0, f" {editor.status_message:<{max_x-len(pos_info)-1}}{pos_info}")
        status.refresh()
        
        # Отрисовка помощи
        help_win.bkgd(' ', curses.color_pair(3))
        safe_addstr(help_win, 0, 0, "^X Exit | ^O Save | ^W Where Am I | ^K Cut Line | ^U Paste")
        help_win.refresh()
        
        # Отрисовка основного текста
        main_win.clear()
        for y, line in enumerate(editor.content[editor.offset_y:editor.offset_y + max_y-3]):
            if y >= max_y-3:
                break
            try:
                line_display = line.rstrip('\n')
                if len(line_display) > max_x:
                    line_display = line_display[:max_x-1] + '>'
                safe_addstr(main_win, y, 0, line_display)
            except curses.error:
                pass

        try:
            cur_y = editor.current_line - editor.offset_y
            cur_y = max(0, min(cur_y, max_y-4))
            main_win.move(cur_y, min(editor.current_col, max_x-1))
        except curses.error:
            pass
        
        main_win.refresh()

    # Один основной цикл редактора
    while True:
        try:
            editor.ensure_valid_position()
            draw_interface()
            
            ch = main_win.getch()
            
            if ch == 24:  # ^X
                if editor.modified:
                    editor.status_message = "Save modified buffer? (y/N)"
                    draw_interface()
                    confirm = main_win.getch()
                    if confirm in (ord('y'), ord('Y')):
                        if editor.save_file():
                            break
                        continue
                break
                
            elif ch == 15:  # ^O
                if editor.save_file():
                    editor.status_message = "File saved successfully"
                
            elif ch == 23:  # ^W
                editor.status_message = f"Line: {editor.current_line+1}/{len(editor.content)}  Col: {editor.current_col+1}"
            
            elif ch == curses.KEY_UP:
                if editor.current_line > 0:
                    editor.current_line -= 1
                    if editor.current_line < editor.offset_y:
                        editor.offset_y = max(0, editor.current_line)
            
            elif ch == curses.KEY_DOWN:
                if editor.current_line < len(editor.content) - 1:
                    editor.current_line += 1
                    if editor.current_line >= editor.offset_y + max_y - 3:
                        editor.offset_y += 1
            
            elif ch == curses.KEY_LEFT:
                if editor.current_col > 0:
                    editor.current_col -= 1
                elif editor.current_line > 0:
                    editor.current_line -= 1
                    editor.current_col = len(editor.content[editor.current_line].rstrip('\n'))
            
            elif ch == curses.KEY_RIGHT:
                line_len = len(editor.content[editor.current_line].rstrip('\n'))
                if editor.current_col < line_len:
                    editor.current_col += 1
                elif editor.current_line < len(editor.content) - 1:
                    editor.current_line += 1
                    editor.current_col = 0
            
            elif ch in (10, curses.KEY_ENTER, ord('\n')):  # Enter
                current = editor.content[editor.current_line]
                before = current[:editor.current_col]
                after = current[self.current_col:]
                editor.content[editor.current_line] = before + '\n'
                editor.content.insert(editor.current_line + 1, after)
                editor.current_line += 1
                editor.current_col = 0
                editor.modified = True
                if editor.current_line - editor.offset_y >= max_y - 3:
                    editor.offset_y += 1
            
            elif ch in (8, 127, curses.KEY_BACKSPACE):  # Backspace
                if editor.current_col > 0:
                    current = editor.content[self.current_line]
                    editor.content[self.current_line] = (
                        current[:self.current_col-1] + current[self.current_col:]
                    )
                    editor.current_col -= 1
                    editor.modified = True
                elif editor.current_line > 0:
                    current = editor.content.pop(editor.current_line)
                    editor.current_line -= 1
                    prev_line = editor.content[editor.current_line].rstrip('\n')
                    editor.current_col = len(prev_line)
                    editor.content[editor.current_line] = prev_line + current
                    editor.modified = True
                    if editor.offset_y > 0:
                        editor.offset_y -= 1
            
            elif ch == curses.KEY_DC:  # Delete
                current = editor.content[editor.current_line]
                if editor.current_col < len(current.rstrip('\n')):
                    editor.content[self.current_line] = (
                        current[:editor.current_col] + current[editor.current_col + 1:]
                    )
                    editor.modified = True
                elif editor.current_line < len(editor.content) - 1:
                    next_line = editor.content.pop(editor.current_line + 1)
                    editor.content[editor.current_line] = current.rstrip('\n') + next_line
                    editor.modified = True
            
            elif ch >= 32 and ch < 127:  # Печатные символы
                editor.insert_char(chr(ch))
                editor.modified = True
            
            editor.ensure_valid_position()
            
        except curses.error:
            continue
        except Exception as e:
            editor.status_message = f"Error: {str(e)}"
            continue

def edit_command(filename):
    if not filename:
        print(f"{Colors.ERROR}{Icons.ERROR} Usage: edit <filename>{Colors.RESET}")
        return
    
    old_codepage = None
    try:
        # Сохраняем и меняем кодировку консоли Windows
        if os.name == 'nt':
            try:
                import subprocess
                old_codepage = subprocess.check_output('chcp', shell=True).decode().split(':')[1].strip()
                os.system('chcp 65001 > nul')
            except:
                pass

        curses.wrapper(lambda stdscr: run_editor(stdscr, filename))
        print(f"{Colors.SUCCESS}{Icons.SAVE} Editor closed{Colors.RESET}")

    except Exception as e:
        print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")
    
    finally:
        # Восстанавливаем кодировку консоли Windows
        if os.name == 'nt' and old_codepage:
            try:
                os.system(f'chcp {old_codepage} > nul')
            except:
                pass

power = 'on'
login_user()  # Вызываем функцию входа перед основным циклом

while power == 'on':
    try:
        if not current_user:  # Если пользователь вышел, запрашиваем новый вход
            login_user()
            continue
            
        current_path = get_shortened_path()
        prompt = input(f'{Colors.USERNAME}{Icons.USER} {current_user}{Colors.RESET}'
                      f'{Colors.PROMPT}@{Cn}{Colors.RESET}'
                      f'{Colors.PATH} {current_path}{Colors.RESET}\n'
                      f'{Colors.INPUT}{Icons.PROMPT} {Colors.RESET}')
        
        if not prompt.strip():
            continue
        
        # Добавляем команду в историю
        command_history.append(prompt)
        
        commandInput = prompt.split()
        command = commandInput[0].lower()
        
        # Проверяем, является ли команда псевдонимом
        if command in aliases:
            alias_cmd = aliases[command].split()
            command = alias_cmd[0].lower()
            if len(alias_cmd) > 1:
                commandInput = alias_cmd[1:] + commandInput[1:]
            else:
                commandInput = commandInput[1:]
        
        if len(commandInput) > 1:
            arg = ' '.join(commandInput[1:])
        else:
            arg = ''
            
        if command in commandList:
            try:
                commandList[command](arg)
            except Exception as e:
                print(f"{Colors.ERROR}{Icons.ERROR} {localization.get_string('commands.error', 'Error executing command: {0}').format(str(e))}{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}{Icons.ERROR} {localization.get_string('commands.not_found', 'Command "{0}" not found.').format(command)}{Colors.RESET}")
    except KeyboardInterrupt:
        print('')
        continue
    except EOFError:
        print(f'\n{Colors.WARNING}{Icons.BACK} Use "quit" to exit.{Colors.RESET}')
        continue
    except Exception as e:
        print(f"{Colors.ERROR}{Icons.ERROR} Error: {str(e)}{Colors.RESET}")
        continue

# Запускаем планировщик задач в отдельном потоке
def run_scheduler():
    while power == 'on':
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()
