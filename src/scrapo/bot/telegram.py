import json
import asyncio
from dotenv import load_dotenv
from os import getenv

# local import
from . import fetch

load_dotenv()

TELEGRAM_API_URL = f'https://api.telegram.org/bot{getenv("BOT_TOKEN")}/sendMessage'

TELEGRAM_MESSAGE_TEMPLATE = """
<a href="{url}">&#8288</a>
📚 <strong>{title}</strong>

⭐️: Rating  {stars}/5 ({total_ratings})

👥: {students}
"""


def prepare_telegram_messages(courses: list) -> list:
    messages = []
    for course in courses:
        message_text = TELEGRAM_MESSAGE_TEMPLATE.format(**course)
        messages.append({
            "chat_id": getenv("CHANNEL_ID"),
            "text": message_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": "False",
            "reply_markup": json.dumps({'inline_keyboard': [[{'text': "Get COURSE", 'url': course["url"]}]]})
        })
    return messages


async def send_telegram_messages(session, courses: list, url=TELEGRAM_API_URL):
    messages = prepare_telegram_messages(courses)
    # Create a list of tasks for sending messages with the bot.
    # We have a rate limit of 20 messages per minute
    # The retry backoff will take care of this
    tasks = [asyncio.create_task(
        fetch.post(session, url, data=message)) for message in messages]
    await asyncio.gather(*tasks)
