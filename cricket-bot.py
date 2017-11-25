from collections import defaultdict
import os
import sys

import praw
from praw.models import MoreComments
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client_id=os.environ['REDDIT_CLIENT_ID']
client_secret=os.environ['REDDIT_CLIENT_SECRET']
password=os.environ['REDDIT_PASSWORD']
username=os.environ['REDDIT_USERNAME']
user_agent='user-agent for /u/singlelinebot'

subreddit = 'Cricket'

def getSubComments(comment, allComments, verbose=True):
    allComments.append(comment)
    if not hasattr(comment, "replies"):
        replies = comment.comments()
    else:
        replies = comment.replies

    for child in replies:
        getSubComments(child, allComments, verbose=verbose)

if __name__ == "__main__":
    comments = []
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         password=password,
                         username=username,
                         user_agent=user_agent)

    if len(sys.argv) < 2:
        print("Give me a URL")
        sys.exit(1)

    url = sys.argv[1]
    scores = defaultdict(int)
    submission = reddit.submission(url=url)

    # Get all comments . https://stackoverflow.com/a/36377995/2610955
    commentsList = []
    for comment in submission.comments.list():
        getSubComments(comment, commentsList)

    i = 0
    # Calculate scores
    for comment in commentsList:
        if not isinstance(comment, MoreComments):
            user = comment.author.name
            score = comment.score
            scores[user] += score
            i += 1

    print("Calculated scores from {0} comments".format(i))
    for user, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        print("u/{user} {score}".format(user=user, score=score))
