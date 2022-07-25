import praw
from dotenv import load_dotenv
from os import getenv

load_dotenv()

r = praw.Reddit(
    client_id=getenv("CLIENT_ID"),
    client_secret=getenv("CLIENT_SECRET"),
    password=getenv("PASSWORD"),
    user_agent=getenv("USER_AGENT"),
    username=getenv("USERNAME")
)
subreddit = r.subreddit(getenv("SUBREDDIT"))

REDDIT_MSG_FORMAT = """
>{subtitle}


* ⭐️: Rating {stars}/5 ({tot_rating})


* 👥: {students}


[Get Course]({url})
"""


def send_messages(elements):

    for element in elements:
        subreddit.submit(
            title=element["title"],
            selftext=REDDIT_MSG_FORMAT.format(**element))
