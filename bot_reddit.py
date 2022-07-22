import praw
import creds

r = praw.Reddit(
    client_id=creds.client_id,
    client_secret=creds.client_secret,
    password=creds.password,
    user_agent=creds.user_agent,
    username=creds.username,
)

subreddit = r.subreddit(creds.subreddit)


def send_message(elements):
    for element in elements:
        text = ">"+element["subtitle"] + "\n\n\n" \
            + "* ⭐️: Rating  " + element["stars"] + "/5" + "(" + element["tot_rating"] + ")" + "\n\n" \
            + "* 👥:  " + element["students"] + "\n\n\n" \
            + "[Get Course](" + element["url"] + ")"
        subreddit.submit(title=element["title"], selftext=text)
