from logging import getLogger
import time
from scrapper import util

LOG = getLogger(__name__)


async def get(session, url="https://idownloadcoupon.com/product-category/100off/") -> set:
    url_with_ad = set()
    links_udemy = set()
    start = time.time()

    url_with_ad = await util.get_links(session, url, "a", {"class": "button product_type_external"})
    links_udemy = util.idc_strip_and_clean(url_with_ad)

    total_time = time.time() - start
    LOG.debug("Took a total of {} second".format(total_time))
    return links_udemy
