from collections import defaultdict
import os
import sys
import sqlite3

import praw
from praw.models import MoreComments
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client_id=os.environ['REDDIT_CLIENT_ID']
client_secret=os.environ['REDDIT_CLIENT_SECRET']
password=os.environ['REDDIT_PASSWORD']
username=os.environ['REDDIT_USERNAME']
user_agent='user-agent for /u/YourFavouriteBot'

subreddit = 'Cricket'

def getSubComments(comment, allComments):
    allComments.append(comment)
    if not hasattr(comment, "replies"):
        replies = comment.comments()
    else:
        replies = comment.replies

    for child in replies:
        getSubComments(child, allComments)

if __name__ == "__main__":
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
    submission_id = submission.id

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    table_name = 'match_{0}'.format(submission_id)
    create_table_stmt = 'create table {0} (id integer primary key autoincrement, submission text, comment_id text, username text, score integer, body text);'.format(table_name)
    insert_table_stmt = 'INSERT INTO {0} VALUES (NULL,?,?,?,?,?)'.format(table_name)
    c.execute(create_table_stmt)

    # Get all comments . https://stackoverflow.com/a/36377995/2610955
    commentsList = []
    for comment in submission.comments.list():
        getSubComments(comment, commentsList)

    i = 0
    # Calculate scores
    filename = 'comments_' + submission.id + '.txt'
    with open(filename, 'a+') as f:
        for comment in commentsList:
            try:
                if not isinstance(comment, MoreComments) and comment and comment.author and comment.author.name and comment.score is not None and comment.body:
                    username = comment.author.name
                    score = comment.score
                    body = comment.body
                    scores[username] += score
                    i += 1
                    data = [(submission_id, comment.id, username, score, comment.body)]
                    c.executemany(insert_table_stmt, data)
                    f.write(comment.body.lower())
            except Exception as e:
                print(e)
                pass # We may fail but we must move on

    conn.commit() # You don't have any data if you don't commit at all :)
    print("Calculated scores from {0} comments".format(i))
    for user, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        print("u/{user} {score}".format(user=user, score=score))
