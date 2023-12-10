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


async def scraping_cycle():
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
        # Initialize a set to store unique udemy links
        udemy_links = set()
        tasks = [
            idownloadcoupon.get(session),
            discudemy.get(session),
            freebiesglobal.get(session),
            tutorialbar.get(session)
        ]
        links = await asyncio.gather(*tasks)
        # Combine all fetched links into a single set
        for link in links:
            udemy_links.update(link)

        # DATABASE
        connection = db_controller.create_connection("links.db")
        db_controller.create_table(connection)

        # ADD LINKS TO DB and RETURN the UPDATED ONE
        # Add fetched links to the database, ignoring duplicates
        links = db_controller.add_items(connection, udemy_links)

        # Extract element from udemy links
        elements_udemy = await util.extract(session, links)

        # Telegram Bot
        await telegram.send_messages(session, elements_udemy)
        # Reddit Bot
        reddit.send_messages(elements_udemy)


if __name__ == '__main__':
    asyncio.run(scraping_cycle())

async def main_loop():
    while True:
        await scraping_cycle()
        await asyncio.sleep(3600)  # Wait for an hour before running again
