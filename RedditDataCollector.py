import praw


p = praw.Reddit(user_agent='NLP Comment Scraper by /u/Smitttttty', client_id='1zFadZX5W60eXw', client_secret='TVSU9vn1wCzZKeum9qTCFUqpJB0')

subreddit = p.subreddit("funny+news+AskReddit")

#i will code something with this tomorrow
for comment in subreddit.stream.comments():
    print comment.body
