__author__ = 'mirko'
import oauth2 as oauth
import time
import json
import traceback
import config as cfg


consumer = oauth.Consumer(key=cfg.twitter['consumer_key'], secret=cfg.twitter['consumer_secret'])
access_token = oauth.Token(key=cfg.twitter['access_token'], secret=cfg.twitter['access_token_secret'])
client = oauth.Client(consumer, access_token)

myList = ['20','21','22','23','25','26']

while len(myList) > 0:
        parameter = ','.join(myList[0:100]) #max 100 id per request
        myList[0:100] =[]
        try:
            place_endpoint ="https://api.twitter.com/1.1/statuses/lookup.json?id="+parameter+"&tweet_mode=extended"
            response, data = client.request(place_endpoint)

            if response['status']=='200':

                jsonTweet=json.loads(data)
                for tweet in jsonTweet:
                    print(json.dumps(tweet))

            if 'x-rate-limit-limit' in response:
                print("wait for ",(15*60)/int(response['x-rate-limit-limit'])," seconds")
                time.sleep((15*60)/int(response['x-rate-limit-limit']))
            else:
                print(response)
                print("wait for ",(15*60)," seconds")
                time.sleep((15*60))

        except Exception:
            print(traceback.format_exc())
            time.sleep(60)
