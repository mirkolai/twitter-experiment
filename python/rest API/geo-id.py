__author__ = 'mirko'
import sys
import time
import oauth2 as oauth
import json
import traceback
import config as cfg


consumer = oauth.Consumer(key=cfg.twitter['consumer_key'], secret=cfg.twitter['consumer_secret'])
access_token = oauth.Token(key=cfg.twitter['access_token'], secret=cfg.twitter['access_token_secret'])
client = oauth.Client(consumer, access_token)

place_ids=['419060023b8455e1','a0d0ed9497e5eb19','9e3a733ab37b91b0']

for place_id in place_ids:

    try:
            place_endpoint = "https://api.twitter.com/1.1/geo/id/"+place_id+".json"
            response, data = client.request(place_endpoint)

            if response['status']=='200':

                result=json.loads(data)
                codes = result['attributes']['174368:admin_order_id']
                print(codes)

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
