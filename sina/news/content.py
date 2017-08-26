# -*- coding: gb2312 -*-


import grequests


def gcrawler(urls):
    rs = (grequests.get(u) for u in urls)
    return grequests.map(rs, size=1000)


# class AsyncGetContents:
#     def __init__(self, urls):
#         self.urls = urls

#     async def fetch(self, url, session):
#         async with session.get(url) as response:
#         return await response.read()

#     async def run(r):
#         tasks = []

#         # Fetch all responses within one Client session,
#         # keep connection alive for all requests.
#         async with ClientSession() as session:
#             for url in self.urls:
#                 task = asyncio.ensure_future(fetch(url, session))
#                 tasks.append(task)

#         responses = await asyncio.gather(*tasks)
#         # you now have all response bodies in this variable

#     def print_responses(result):
#         print(result)

# loop = asyncio.get_event_loop()
# future = asyncio.ensure_future(run(4))
# loop.run_until_complete(future)
