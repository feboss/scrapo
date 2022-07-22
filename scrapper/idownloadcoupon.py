import logging
import time
import fetch
import util


async def get(session, url="https://idownloadcoupon.com/product-category/100off/"):
    links_udemy = set()
    start = time.time()

    cont = await fetch.get_all(session, url)
    if cont:
        for html in cont:  # type: ignore
            links_udemy = util.coupon_extract_idc(html=html)

    num_calls = 1
    total_time = time.time() - start
    logging.getLogger('IdownloadCoupon Scraping').debug(
        "It took {} seconds to make {} calls. we get {} results".format(total_time, num_calls, len(links_udemy)))

    return links_udemy
