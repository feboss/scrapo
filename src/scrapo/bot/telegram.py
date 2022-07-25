import json
import asyncio
from dotenv import load_dotenv
from os import getenv

# local import
import fetch

load_dotenv()

API_URL = f'https://api.telegram.org/bot{getenv("BOT_TOKEN")}/sendMessage'

TELEGRAM_MSG_FORMAT = """
<a href="{url}">&#8288</a>
📚 <strong>{title}</strong>

⭐️: Rating  {stars}/5 ({tot_rating})

👥: {students}
"""


def prepare_message(elements: list) -> list:
    data = []
    for element in elements:
        text = TELEGRAM_MSG_FORMAT.format(**element)
        data.append({
                    "chat_id": getenv("CHANNEL_ID"),
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": "False",
                    "reply_markup": json.dumps({'inline_keyboard': [[{'text': "Get COURSE", 'url': element["url"]}]]})
                    })
    return data


async def send_messages(session, elements: list, url=API_URL):
    data = prepare_message(elements)
    # Create a list of task for send message with bot.
    # we have a rate limit of 20 message per minute
    # the retry backoff will take care
    tasks = [asyncio.create_task(
        fetch.get(session, url, params=parameter)) for parameter in data]
    await asyncio.gather(*tasks)
