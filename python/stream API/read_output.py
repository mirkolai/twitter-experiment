__author__ = 'mirko'
# -*- coding: utf-8 -*-
import json
import glob
import gzip
import traceback


filelist = sorted(glob.glob("*.out.gz"))


for file in filelist:
    print(file)
    infile = gzip.open(file, 'rb')

    try:

        for row in infile:
            jsonTweet = json.loads(row)
            if 'text' in jsonTweet:
                print(jsonTweet['text'])
            else:
                print(json.dumps(jsonTweet))

    except Exception:
        print(traceback.format_exc())

