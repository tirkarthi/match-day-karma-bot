# match-day-karma-bot

A simple Reddit bot to caculate comment Karma in Cricket match threads

## Installation

* Create a virtualenv with `python -m venv cricket-env`
* Activate the virtualenv with `source cricket-env/bin/activate`
* `pip install -r requirements.txt`
* Make a `.env` file in the same directory with environment variables for the script
* `python cricket-bot.py <MATCH_URL>`

## Top 5 users for the match with the number of comments

```bash
(cricket-env) ubuntu@localhost:~/match-day-karma-bot$ sqlite3 data.db
SQLite version 3.11.0 2016-02-15 17:29:24
Enter ".help" for usage hints.
sqlite> .mode column
sqlite> .header on
sqlite> select count(*) as number_of_comments, username as username, sum(score) as karma from match_7fb2og group by (username) order by sum(score) desc limit 20;
number_of_comments  username        karma
------------------  --------------  ----------
10                  jezfromthebush  411
10                  xxx-treme       272
7                   GaryGronk       252
6                   Bangkok_Dave    211
15                  CornDogMillion  198
```

## Wordcloud of comments for 1st Ashes (Day 3 2017)

Use the body column of the table or comments.txt and use this library https://github.com/amueller/word_cloud (Thanks to the @amueller)

![wordcloud](wordcloud.png)

## LICENSE

Copyright © 2017 Karthikeyan S

Distributed under the MIT License
