# -*- coding: utf-8 -*-


import grequests
import asyncio
from aiohttp import ClientSession


def gcrawler(urls):
    rs = (grequests.get(u, timeout=10) for u in urls)
    return grequests.map(rs, size=1000)


# def __init__(self, urls):
#         self.urls = urls

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()

async def run(urls):
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

    resps = await asyncio.gather(*tasks)
    return resps


def aiocrawler(urls):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(urls))
    return loop.run_until_complete(future)
