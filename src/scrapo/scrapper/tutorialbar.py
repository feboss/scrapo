from logging import getLogger
import time
# local import
from scrapper import util

LOG = getLogger(__name__)


async def get(session, url="https://www.tutorialbar.com/") -> set:
    url_first_layer = set()
    links_udemy = set()
    start = time.time()

    url_first_layer = await util.get_links(session, url, "h3", inner="a")
    links_udemy = await util.get_links(session, url_first_layer, "a", {'class': 'btn_offer_block re_track_btn'}, limit=1)

    total_time = time.time() - start

    LOG.debug("Took a total of {} second".format(total_time))
    return links_udemy
