#!/usr/bin/env python3
from time import sleep
from random import randrange

import asyncio
import requests

loop = asyncio.get_event_loop()


def request_get(urls):
    tasks = []

    for url in urls:
        tasks.append(loop.run_in_executor(None, requests.get, url))

    return loop.run_until_complete(asyncio.gather(*tasks))


def fetch():
    tasks = []
    urls = [
        'https://www.python.org',
        'http://www.google.com',
        'http://www.google.co.uk',
        'https://stackoverflow.com'
    ]

    for response in request_get(urls):
        print(response.text)

    def sleeper(t):
        t = randrange(1, 10)
        sleep(t)
        print('slepped for', t)

    for url in urls:
        tasks.append(loop.run_in_executor(None, requests.get, url))

    for i in range(10):
        tasks.append(loop.run_in_executor(None, sleeper, i))

    # def r():
    #     raise ValueError('hi')
    # tasks.append(loop.run_in_executor(None, r))
    # print(tasks)
    return asyncio.gather(*tasks)


print('Calling main')
htmls = loop.run_until_complete(fetch())
# for html in htmls:
#     print(html.text)  # html.json()
print('After calling main')
