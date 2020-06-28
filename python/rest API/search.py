import oauth2 as oauth
import time
import json
import traceback
import config as cfg


consumer = oauth.Consumer(key=cfg.twitter['consumer_key'], secret=cfg.twitter['consumer_secret'])
access_token = oauth.Token(key=cfg.twitter['access_token'], secret=cfg.twitter['access_token_secret'])
client = oauth.Client(consumer, access_token)

words = ["happy","music"]

for word in words:
    next_results = -1
    while next_results!=0:

        try:

            if next_results==-1:
                timeline_endpoint = "https://api.twitter.com/1.1/search/tweets.json?q="+word+"&count=100"
            else:
                timeline_endpoint = "https://api.twitter.com/1.1/search/tweets.json"+next_results


            response, data = client.request(timeline_endpoint)

            if response['status']=='200':

                data = json.loads(data)
                tweets = data['statuses']
                metadata = data['search_metadata']

                if 'next_results' in metadata:
                    next_results = metadata['next_results']
                    for tweet in tweets:
                        print(tweet['text'])
                else:
                    next_results=0

            elif response['status']=='400' or response['status']=='403' or response['status']=='404' or response['status']=='401':
                next_results=0
            else:
                next_results = -1

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
