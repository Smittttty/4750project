import sys
sys.path.insert(0, 'praw/')
sys.path.insert(0, 'pickle/')
import praw
import pickle

p = praw.Reddit(user_agent='NLP Comment Scraper by /u/Smitttttty', client_id='1zFadZX5W60eXw', client_secret='TVSU9vn1wCzZKeum9qTCFUqpJB0')

subreddit = p.subreddit("funny+news+AskReddit")

#i will code something with this tomorrow
f = open("test.txt", "w");
for comment in subreddit.stream.comments():
    if(len(comment.body) > 0):
        f.write(comment.body + "\r\n")
f.close();
