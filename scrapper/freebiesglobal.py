from bs4 import BeautifulSoup
import logging
import time

import fetch
import util


async def get(session, url="https://freebiesglobal.com/dealstore/udemy"):
    link_card = set()
    links_udemy = set()
    start = time.time()
    num_calls = 1

    cont = await fetch.get_all(session, url)
    if cont:
        for html in cont:
            soup = BeautifulSoup(html, "html.parser")
            card = soup.find_all(
                "a", class_="img-centered-flex rh-flex-center-align rh-flex-justify-center")
            link_card = [course.get("href") for course in card]

    cont = await fetch.get_all(session, link_card)
    num_calls += len(link_card)
    if cont:
        for html in cont:
            link_udemy = util.coupon_extract(html=html)
            links_udemy.add(link_udemy)

    total_time = time.time() - start
    logging.getLogger('FreebiesGlobal Scraping').debug(
        "It took {} seconds to make {} calls. we get {} results".format(total_time, num_calls, len(links_udemy)))
    return links_udemy
