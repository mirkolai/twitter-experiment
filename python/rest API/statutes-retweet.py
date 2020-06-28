__author__ = 'mirko'
import oauth2 as oauth
import time
import json
import traceback
import config as cfg


consumer = oauth.Consumer(key=cfg.twitter['consumer_key'], secret=cfg.twitter['consumer_secret'])
access_token = oauth.Token(key=cfg.twitter['access_token'], secret=cfg.twitter['access_token_secret'])
client = oauth.Client(consumer, access_token)

ids_str=['20','21','22','23','25','26']

for id_str in ids_str:

    max_id=-1
    while max_id!=0:

        if max_id<0:

            timeline_endpoint = "https://api.twitter.com/1.1/statuses/retweets/"+id_str+".json"
        else:
            timeline_endpoint = "https://api.twitter.com/1.1/statuses/retweets/"+id_str+".json?max_id="+str(max_id)

        try:
            response, data = client.request(timeline_endpoint)
            print(response['status'])
            if response['status']=='200':
                max_id = 0
                tweets = json.loads(data)
                for tweet in tweets:
                    if max_id==0:
                        max_id=int(tweet['id'])-1
                    elif max_id>int(tweet['id']):
                        max_id=int(tweet['id'])-1
                    print(tweet['created_at'])


            elif response['status']=='400' or response['status']=='403' or response['status']=='404' or response['status']=='401':
                max_id=0
            else:
                max_id=-1


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


