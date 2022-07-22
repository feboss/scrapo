import logging
import time
from bs4 import BeautifulSoup
# local import
import fetch
import util


async def get(session, url="https://www.tutorialbar.com/"):
    link_card = set()
    links_udemy = set()
    start = time.time()
    num_calls = 1

    cont = await fetch.get_all(session, url)
    if cont:
        for html in cont:  # type: ignore
            soup = BeautifulSoup(html, "html.parser")
            links = soup.find_all("h3")
            link_card = [link.find("a").get("href") for link in links]
    cont = await fetch.get_all(session, link_card)
    num_calls += len(link_card)
    if cont:
        for html in cont:  # type: ignore
            link_udemy = util.coupon_extract(html=html)
            links_udemy.add(link_udemy)

    total_time = time.time() - start
    logging.getLogger('TutorialBar Scraping').debug(
        "It took {} seconds to make {} calls. we get {} results".format(total_time, num_calls, len(links_udemy)))
    return links_udemy
