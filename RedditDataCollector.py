import sys
sys.path.insert(0, 'praw/')

import praw
from getFrequencies import generate_ngram_string
import pickle
import threading
import thread
import time

nGram = [{} for i in range(0, 7)]
alive = True

for i in range(2, 7):
    nGram[i] = {}

lock = threading.Lock()

def reddit_farm(reddits, nGram_Array):
    p = praw.Reddit(user_agent='NLP Comment Scraper by /u/Smitttttty', client_id='1zFadZX5W60eXw',
                    client_secret='TVSU9vn1wCzZKeum9qTCFUqpJB0')

    subreddit = p.subreddit(reddits)

    lock.acquire()
    for comment in subreddit.stream.comments():
        for i in range(2, 7):
            generate_ngram_string(i, comment.body, nGram[i]);
            pickle.dump(nGram[i], open(reddits.replace("+", "") + "_" + str(i) + ".ng", "wb"))
        print comment.body
    lock.release()

thread.start_new(reddit_farm, ("funny+askreddit", nGram))

while True:
    time.sleep(1000)