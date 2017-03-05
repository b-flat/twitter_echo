import os
import sys
import time
import json

import datetime

import tweepy



NUMBER_OF_QUERIES = 150 #int(sys.argv[1])
QUERY = "amazon echo" #sys.argv[2]
OUTPUT_FILE_NAME = 'amazon_twitter.json'


consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def query_data(n, query):
    search_results = api.search(q=query, since_id=0, count = 100)
    print 'Initial number of search results: ', len(search_results)
    twitter_json = map(lambda tweepy_status: tweepy_status._json, search_results)
    twitter_json_all = twitter_json

    for i in xrange(n):
        print "Number of iteration: ", i, ' @ ' ,datetime.datetime.now()
        try:
            ids = map(lambda tweepy_status: tweepy_status.id, search_results)
            search_results = api.search(q=query, max_id=min(ids), count = 100)
            print 'Number of search results: ', len(search_results)
            twitter_json = map(lambda tweepy_status: tweepy_status._json, search_results)
            twitter_json_all += twitter_json
            print 'Total number of tweets: ',len(twitter_json_all)
        except:
            print 'Sleeping for 15 min ... '
            time.sleep(60 * 15)
            print 'Done Sleeping Continuing ...'
            continue
    return twitter_json_all

twitter_json_all = query_data(NUMBER_OF_QUERIES, QUERY)

with open(OUTPUT_FILE_NAME, 'wb+') as f:
    f.write(json.dumps(twitter_json_all))

