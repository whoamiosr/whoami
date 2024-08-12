import sys
import os
from time import sleep
from random import choice
from colorama import Fore
import fade
from tqdm import tqdm
import subprocess

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
                                                 
 v1.0.3 beta!
'''

    _dockBanner = '''⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⡀
⠀⠀⠀⢲⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⣦⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⣶⠀⠀⠀⠀⢸⠁
⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⡇⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⢸⡆
⠀⠀⠀⣿⡀⢀⠀⠀⣸⣇⢀⠀⠤⢠⣿⠄⡄⢀⡠⣼⡤⣀⠀⡄⢸⣧⠠⡀⢠⢤⣿⡤⡄⠠⠔⣾⡗⠢
⠀⠀⠀⣿⠁⠀⠀⠀⢻⡏⠀⠀⠀⢠⣿⠀⠀⠀⠀⣿⡇⠀⠀⠀⢸⣿⠀⠀⠀⠘⣿⠃⠀⠀⠀⣿⡇
⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠘⣿⠀⠀⠀⠀⣿⡇⠀⠀⠀⢸⡿⠀⠀⠀⢀⣿⡀⠀⠀⠀⣿⡇
⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⣿⡇⠀⠀⠀⢸⡇⠀⠀⠀⠈⣿⠁⠀⠀⠀⣿⡇
⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⢸⠁⠀⠀⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⣿⡇
⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⢸⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⣿⡇
⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⢸⣿⠀⠀⠀⠀⢸⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⣿⡇
⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠸⣿⠀⠀⠀⠀⢸⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⢻⡇
⠀⠀⠀⠈⠀⠀⠀⠀⠘⠃⠀⠀⠀⠀⠋⠀⠀⠀⠀⠸⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀⠉⠀⠀⠀⠀⠘⠁
          by whoami дэнчик йоу
   ⣶⣶⣶⣶⣾⡷⢿⣶⣶⡾⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣾⣿⣿'''



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
 Также убедитесь что номер начинается на +7 или +998 (Россия и Узбекистан соответственно)
                
3. Утилита неисправна или работает неккоректно.
 Обновите, переустановите или ждите, пока дядя разработчик всё пофиксит.

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
        print(Fore.GREEN + "Атака запущена! (надеюсь)" + Fore.RED +"\nВ случае, если атака не запустилась - читайте инструкцию.")
        
        change_config('attack', 'True')
        try:
            while True:
                start_async_attacks(number, 1)
        except KeyboardInterrupt:
            print(Fore.RED + "Атака остановлена пользователем.")
        finally:
            change_config('attack', 'False')
            print(Fore.RED + "Атака завершена.")

    def checking_values():
        clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
        clear()
        subprocess.call('clear' if os.name != 'nt' else 'cls', shell=True)
        '''Проверка вводимых данных'''
        print(fade.fire(_dockBanner))
        number = input(Fore.RED + "Введите атакующий номер (без + и пробелов): ").strip()
        if number.isdigit():
            start_attack(number)
        else:
            print(Fore.RED + "Введите корректный номер!")



    while True:
        clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
        clear()
        subprocess.call('clear' if os.name != 'nt' else 'cls', shell=True)
        print(fade.purplepink(_banner))
        print(fade.fire('если я узнаю что этот бомбер куда-то сливался, то я \nсделаю запуск по токенам и хуй вам черти ебаные'))
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
                print(Fore.GREEN + "Бомбер успешно обновлён. Перезапустите его.")
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
