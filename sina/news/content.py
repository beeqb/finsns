# -*- coding: utf-8 -*-


import grequests
import asyncio
from aiohttp import ClientSession


def gcrawler(urls):
    rs = (grequests.get(u, timeout=10) for u in urls)
    return grequests.map(rs, size=1000)


class AsyncGetContents:
    def __init__(self, urls):
        self.urls = urls

    async def fetch(self, url, session):
        async with session.get(url) as response:
            return await response.read()

    async def run(self):
        tasks = []

        # Fetch all responses within one Client session,
        # keep connection alive for all requests.
        async with ClientSession() as session:
            for url in self.urls:
                task = asyncio.ensure_future(fetch(url, session))
                tasks.append(task)

        resps = await asyncio.gather(*tasks)
        return resps
        # you now have all response bodies in this variable


def aiocrawler(urls):
    agc = AsyncGetContents(urls)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(agc.run())
    loop.run_until_complete(future)
