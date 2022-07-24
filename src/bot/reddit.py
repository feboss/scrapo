import praw
import creds

r = praw.Reddit(
    client_id=creds.CLIENT_ID,
    client_secret=creds.CLIENT_SECRET,
    password=creds.PASSWORD,
    user_agent=creds.USER_AGENT,
    username=creds.USERNAME,
)
subreddit = r.subreddit(creds.SUBREDDIT)


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
