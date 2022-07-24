import json
import asyncio

# local import
import fetch
import creds


API_URL = 'https://api.telegram.org/bot' + creds.BOT_TOKEN + '/sendMessage'


def prepare_message(elements):
    data = []
    for element in elements:
        text = f'<a href="{element["url"]}">' + "&#8288" + "</a>" + "\n" \
            + "📚" + "<strong>" + element["title"] + "</strong>" + "\n\n" \
                    + "⭐️: Rating  " + element["stars"] + "/5" \
                    + " (" + element["tot_rating"] + ")" + "\n\n" \
                    + "👥: " + element["students"] + "\n\n"
        data.append({
                    "chat_id": creds.CHANNEL_ID,
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": False,
                    "reply_markup": json.dumps({'inline_keyboard': [[{'text': "Get COURSE", 'url': element["url"]}]]})
                    })
    return data


async def send_messages(session, element, url=API_URL):

    data = prepare_message(element)
    # Create a list of task for send message with bot.
    tasks = [asyncio.create_task(
        fetch.get(session, url, params=parameter)) for parameter in data]
    await asyncio.gather(*tasks)
