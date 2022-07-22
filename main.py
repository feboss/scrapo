import logging
import aiohttp
import asyncio
# local import
from scrapper import idownloadcoupon
from scrapper import tutorialbar
from scrapper import freebiesglobal
from scrapper import discudemy
import bot_telegram
import bot_reddit
import db_controller
import util


logging.basicConfig(filename="log.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")


async def main():

    async with aiohttp.ClientSession(raise_for_status=True, connector=aiohttp.TCPConnector(limit=100)) as session:
        # ASYNC SCRAPPING
        links_udemy = set()
        tasks = []
        tasks.append(asyncio.create_task(idownloadcoupon.get(session)))
        tasks.append(asyncio.create_task(discudemy.get(session)))
        tasks.append(asyncio.create_task(freebiesglobal.get(session)))
        tasks.append(asyncio.create_task(tutorialbar.get(session)))
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
        await bot_telegram.send_messages(session, elements_udemy)
        # Reddit Bot
        bot_reddit.send_message(elements_udemy)


if __name__ == '__main__':
    asyncio.run(main())
