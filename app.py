import os
import time
from random import random
from twython import Twython
import headlines

CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']
TWEET_LENGTH = 140
TWEET_URL_LENGTH = 21
USERNAME = 'DicedOnionBot'

RUN_EVERY_N_SECONDS = 60*10 # e.g. 60*5 = tweets every five minutes

def twitter_handle():
    return Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def submit_tweet(message, handle=None):
    if not handle:
        handle = twitter_handle()
    handle.update_status(status=message)

def list_of_tweets(handle, count=200, username=USERNAME):
    user_timeline = handle.get_user_timeline(screen_name=username, \
        count=count)
    return [tweet['text'] for tweet in user_timeline]

def get_message(mdl, corpus, handle):
    """
    Generate message from Markov model
    """
    said_before = True
    while said_before:
        msg = headlines.get_msg(mdl, max_length=TWEET_LENGTH-2, \
            text=corpus)
        # check if it's been said already
        said_before = msg in list_of_tweets(handle)
    assert len(msg) <= TWEET_LENGTH
    return '"' + msg + '"'

def main():
    handle = twitter_handle()
    mdl, corpus = headlines.get_model(infile=headlines.DATAFILE_ONION)
    while True:
        message = get_message(mdl, corpus, handle)
        print message
        submit_tweet(message, handle)
        time.sleep(RUN_EVERY_N_SECONDS)

if __name__ == '__main__':
    main()
