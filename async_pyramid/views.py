""" Cornice services.
"""
import asyncio
import aiohttp
import time
from cornice import Service


hello = Service(name='hello', path='/', description="Simplest app")

extern = Service(name='extern', path='/extern')


@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    return {'Hello': 'World'}


async def get_url(session, url):
    async with session.get(url) as response:
        return await response.json()



async def coordinator():
    async with aiohttp.ClientSession() as session:
        values = await asyncio.gather(*[get_url(session, 'http://httpbin.org/delay/{}'.format(i)) for i in range(1,5)])
        return [x['url'] for x in values]



@extern.get()
def get_external(request):
    start = time.time()
    result = asyncio.run(coordinator())
    elapsed = time.time() - start
    return {'elapsed': elapsed, 'urls': result}
