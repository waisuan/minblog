import praw

#
r = praw.Reddit(user_agent='Testing PRAW API (by /u/theNaus)')
posts = r.get_subreddit('all').get_hot(limit=10)
for p in posts:
    print p
