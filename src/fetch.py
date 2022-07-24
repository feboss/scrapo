import asyncio
import logging
import random
import aiohttp


async def get(session, url, retries=4, backoff_in_seconds=2, pow=2, params=None, headers=None, sleep=0):

    try:
        logging.getLogger('aiohttp.client').debug(
            f'Request starting at <{url}>')
        elapsed = asyncio.get_event_loop().time()
        async with session.get(url, data=params, headers=headers) as response:
            elapsed = asyncio.get_event_loop().time() - elapsed
            logging.getLogger('aiohttp.client').debug(
                "Request ended in {} - URL= {} - status: {}".format(elapsed, response.url, response.status))

            r = await response.text()
            # fix for "Response payload is not completed"
            await asyncio.sleep(0)
            return r

    except aiohttp.ClientResponseError as e:
        logging.getLogger('aiohttp.client').warning(
            f"Request error: {e} - Retry")
        # BACKOFF
        if retries > 0:
            sleep = (backoff_in_seconds * 2 ** pow +
                     random.uniform(0, 1))
            await asyncio.sleep(sleep)
            await get(session, url, retries=retries-1, pow=pow+1, params=params)
    except Exception as e:
        print(e)


async def get_all(session, urls, params=None, headers={}, sleep=0):
    if type(urls) is str:
        urls = [urls]
    tasks = [asyncio.create_task(
        get(session, url, params=params, headers=headers, sleep=sleep)) for url in urls]
    results = await asyncio.gather(*tasks)
    return results
