import asyncio
import logging
import time
import aiohttp
import db_controller
# local import
import util
from bot import reddit, telegram
from scrapper import discudemy, freebiesglobal, idownloadcoupon, tutorialbar


logging.basicConfig(filename="log.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")


async def main():
    """
    An asynchronous function that performs several tasks concurrently.
    It uses the aiohttp library to make HTTP requests and gather data from multiple websites.
    It also interacts with a database and sends messages using the Telegram and Reddit bots.
    """
    async with aiohttp.ClientSession(
        raise_for_status=True,
        connector=aiohttp.TCPConnector(limit=10),
        timeout=aiohttp.ClientTimeout(30)
    ) as session:
        # ASYNC SCRAPPING
        links_udemy = set()
        tasks = [
            idownloadcoupon.get(session),
            discudemy.get(session),
            freebiesglobal.get(session),
            tutorialbar.get(session)
        ]
        links = await asyncio.gather(*tasks)
        for link in links:
            links_udemy.update(link)

        # DATABASE
        connection = db_controller.create_connection("links.db")
        db_controller.create_table(connection)

        # ADD LINKS TO DB and RETURN the UPDATED ONE
        links = db_controller.add_items(connection, links_udemy)

        # Extract element from udemy links
        elements_udemy = await util.extract(session, links)

        # Telegram Bot
        await telegram.send_messages(session, elements_udemy)
        # Reddit Bot
        reddit.send_messages(elements_udemy)


if __name__ == '__main__':
    while True:
        asyncio.run(main())
        time.sleep(60*60)
