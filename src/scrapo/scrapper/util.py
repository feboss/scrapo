from logging import getLogger
import time
from urllib.parse import unquote, urlparse
from bs4 import BeautifulSoup
# local import
import fetch

LOG = getLogger(__name__)


async def fetch_links(session, url, *selectors, limit=None, inner=None) -> set:
    start_time = time.time()
    responses = await fetch.get_all(session, url)
    num_requests = len(responses)
    links = set()

    if responses:
        for response in responses:
            if response:
                soup = BeautifulSoup(response, "html.parser")
                elements = soup.find_all(*selectors, limit=limit)
                if inner:
                    links.update({element.find(inner).get("href") for element in elements})
                else:
                    links.update({element.get("href") for element in elements})

    elapsed_time = time.time() - start_time

    LOG.debug(f"Result: {links} It took {elapsed_time} seconds for {num_requests} requests. We got {len(links)} results")

    return links


def idc_strip_and_clean(links) -> set:
    # example link:
    # https://ad.admitad.com/g/05dgete24s54a912f9f1b3e3b7aadc/?i=10&ulp=https%3A%2F%2Fwww.udemy.com%2Fcourse%2Flssbb-lean-six-sigma-black-belt-practice-exams%2F%3FcouponCode%3DFB2B4597C61AD35051B0
    # we strip the udemy link and uniform the link

    result = set()
    for link in links:
        lin = unquote(link)
        lin = urlparse(lin)
        lin = lin.query
        result.add(lin[9:])
    return result


def uniform_link(links):
    pass
def uniform_link(links):
    uniform_links = set()
    for link in links:
        uniform_links.add(link.lower())
    return uniform_links
