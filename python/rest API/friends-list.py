import oauth2 as oauth
import time
import json
import traceback
import config as cfg


consumer = oauth.Consumer(key=cfg.twitter['consumer_key'], secret=cfg.twitter['consumer_secret'])
access_token = oauth.Token(key=cfg.twitter['access_token'], secret=cfg.twitter['access_token_secret'])
client = oauth.Client(consumer, access_token)

screen_names=['jack','biz','noah','crystal','jeremy']

for screen_name in screen_names:

    next_cursor=-1
    while next_cursor!=0:
        try:

            if next_cursor<0:
                timeline_endpoint = "https://api.twitter.com/1.1/friends/ids.json?count=5000&cursor=-1&screen_name=" + screen_name

            else:
                timeline_endpoint = "https://api.twitter.com/1.1/friends/ids.json?count=5000&cursor=" + str(next_cursor) +"&screen_name=" + screen_name

            response, data = client.request(timeline_endpoint)

            print(response['status'])
            if response['status']=='200':

                dataResult = json.loads(data)

                next_cursor = dataResult['next_cursor']

                for userFollower in dataResult['ids']:
                    print(userFollower)

            elif response['status']=='400' or response['status']=='403' or response['status']=='404' or response['status']=='401':
                next_cursor=0
            else:
                next_cursor=-1

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
