from logging import getLogger
import time
# local import
from scrapper import util

LOG = getLogger(__name__)


async def get(session, url="https://www.discudemy.com/all/1") -> set:
    url_first_layer = set()
    url_second_layer = set()
    links_udemy = set()
    start = time.time()

    url_first_layer = await util.get_links(session, url, 'a', {'class': 'card-header'})

    url_second_layer = await util.get_links(session, url_first_layer, 'a', {'class': 'ui big inverted green button discBtn'}, limit=1)

    links_udemy = await util.get_links(session, url_second_layer, 'a', {'id': 'couponLink'}, limit=1)

    total_time = time.time() - start

    LOG.debug("Took a total of {} second".format(total_time))
    # remove "/" before ?couponCode
    # for link_udemy in links_udemy:
    #     slash_index = link_udemy.find("?couponCode")-1
    #     if (link_udemy[slash_index] == "/"):
    #         links_udemy.add(link_udemy[:slash_index] + link_udemy[slash_index+1:])

    return links_udemy
