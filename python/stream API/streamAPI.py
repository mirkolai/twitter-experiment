__author__ = 'mirko'

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import traceback
import gzip
from datetime import datetime
import time
import config as cfg

def start_stream():

    while True:
        try:

            l = StdOutListener()
            auth = OAuthHandler(cfg.twitter["consumer_key"], cfg.twitter["consumer_secret"])
            auth.set_access_token(cfg.twitter["access_token"], cfg.twitter["access_token_secret"])
            stream = Stream(auth, l)
            stream.filter(track=['music'])
            # http://docs.tweepy.org/en/latest/streaming_how_to.html

        except Exception:

            print(traceback.format_exc())
            time.sleep(60)
            continue


class StdOutListener(StreamListener):

    def on_data(self, tweet):

        try:

            jsonTweet=json.loads(tweet)

            if 'text' in jsonTweet:
                print(jsonTweet['text'])
            else:
                print(json.dumps(jsonTweet))

            """
            each tweet is saved in a new line of a file out.gz
            the tweet is saved in the file corresponding to the day it was gathered
            YYYYY-MM-DD 00:00:00.out.gz
            """
            date = datetime.now()
            date = date.replace(hour=0,minute=0, second=0, microsecond=0)
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            file = gzip.open(date+'.out.gz', "ab")

            file.write(bytes(tweet, 'UTF-8'))
            file.close()

            return True

        except Exception:
            print(traceback.format_exc())
        pass

    def on_error(self, status):
        print(traceback.format_exc())

if __name__ == '__main__':

    try:
        start_stream()
    except Exception:
        print(traceback.format_exc())
