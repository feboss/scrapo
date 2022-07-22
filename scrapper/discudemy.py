import logging
import time
from bs4 import BeautifulSoup
# local import
import fetch
import util


async def get(session, url="https://www.discudemy.com/all/1"):
    link_card = set()
    links_udemy = set()
    start = time.time()
    num_calls = 1
    links_second_screen = set()

    cont = await fetch.get_all(session, url)
    if cont:
        for html in cont:
            soup = BeautifulSoup(html, "html.parser")
            card = soup.find_all(
                "a", class_="card-header")
            link_card = [course.get("href") for course in card]

    cont = await fetch.get_all(session, link_card)
    num_calls += len(link_card)
    if cont:
        for html in cont:
            soup = BeautifulSoup(html, "html.parser")
            card = soup.find(
                "a", class_="ui big inverted green button discBtn")
            links_second_screen.add(card.get("href"))  # type: ignore

    cont = await fetch.get_all(session, links_second_screen)
    num_calls += len(links_second_screen)
    if cont:
        for html in cont:
            # soup = BeautifulSoup(html, "html.parser")
            # card = soup.find("a", {"id" : "couponLink"})
            link_udemy = util.coupon_extract(html=html)
            links_udemy.add(link_udemy)  # type: ignore

    total_time = time.time() - start
    num_calls += 1 + len(link_card)
    logging.getLogger('DiscUdemy Scraping').debug(
        "It took {} seconds to make {} calls. we get {} results".format(total_time, num_calls, len(links_udemy)))

    return links_udemy
