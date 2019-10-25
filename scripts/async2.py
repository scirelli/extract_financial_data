#!/usr/bin/env python3
# pylint: disable=import-error
import asyncio
import aiohttp


async def fetch(session, url):
    async with session.get(url, allow_redirects=True) as response:
        return await response.text()


async def main():
    urls = [
        'https://www.python.org',
        'http://www.google.com',
        'http://www.google.co.uk',
        'https://stackoverflow.com'
    ]
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))

        htmls = await asyncio.gather(*tasks)

        for html in htmls:
            print(html[:100])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
