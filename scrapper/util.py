from logging import getLogger
import time
from urllib.parse import unquote, urlparse
from bs4 import BeautifulSoup
# local import
import fetch

LOG = getLogger(__name__)


async def get_links(session, url, *atrs, limit=None, inner=None) -> set:
    start = time.time()
    num_calls = 0
    cont = None
    cont = await fetch.get_all(session, url)
    num_calls += len(cont)
    result = set()
    if cont:
        for html in cont:
            if html:
                soup = BeautifulSoup(html, "html.parser")
                card = soup.find_all(*atrs, limit=limit)
                if inner:
                    result.update({course.find(inner).get("href")
                                  for course in card})
                else:
                    result.update({course.get("href") for course in card})

    total_time = time.time() - start

    LOG.debug("Result: {} It took {} seconds for {} calls. we get {} results".format(
        result, total_time, num_calls, len(result)))

    return result


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
