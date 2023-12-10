import praw
from dotenv import load_dotenv
from os import getenv

load_dotenv()

reddit_instance = praw.Reddit(
    client_id=getenv("CLIENT_ID"),
    client_secret=getenv("CLIENT_SECRET"),
    password=getenv("PASSWORD"),
    user_agent=getenv("USER_AGENT"),
    username=getenv("USERNAME")
)
target_subreddit = reddit_instance.subreddit(getenv("SUBREDDIT"))

REDDIT_MSG_FORMAT = """
>{subtitle}


* ⭐️: Rating {stars}/5 ({tot_rating})


* 👥: {students}


[Get Course]({url})
"""


def post_courses_to_subreddit(courses):

    for course in courses:
        target_subreddit.submit(
            title=course["title"],
            selftext=REDDIT_MSG_FORMAT.format(**course))
