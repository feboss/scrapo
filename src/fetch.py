import asyncio
import logging
import random
import aiohttp
from fake_useragent import UserAgent


async def get(session, url, retries=4, backoff_in_seconds=2, pow=2, params=None):

    try:
        logging.getLogger('aiohttp.client').debug(
            f'Request starting at <{url}>')
        elapsed = asyncio.get_event_loop().time()

        async with session.get(url, data=params, headers= {'User-Agent': UserAgent().random}) as response:
            elapsed = asyncio.get_event_loop().time() - elapsed
            logging.getLogger('aiohttp.client').debug(
                "Request ended in {} - URL= {} - status: {}".format(elapsed, response.url, response.status))
            return await response.text()

    except aiohttp.ClientResponseError as e:
        logging.getLogger('aiohttp.client').warning(
            f"Request error: {e} - Retry")
        # BACKOFF
        if retries > 0:
            sleep = (backoff_in_seconds * 2 ** pow +
                     random.uniform(0, 1))
            await asyncio.sleep(sleep)
            await get(session, url, retries=retries-1, pow=pow+1, params=params)


async def get_all(session, urls, params=None):
    if type(urls) is str:
        urls = [urls]
    tasks = [asyncio.create_task(
        get(session, url, params=params)) for url in urls]
    results = await asyncio.gather(*tasks)
    return results
