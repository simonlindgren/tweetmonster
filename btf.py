#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
BACK TO FUTURE TWEET COLLECTOR
'''

import glob
import sqlite3
import sys
import datetime
import tweepy
from tweepy.auth import OAuthHandler
import time
import re
import json
from concurrent.futures import ThreadPoolExecutor

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--project", default = "btf")
parser.add_argument("-l", "--language", default = "all")
parser.add_argument("-q", "--query", default = "coffee OR tea")
parser.add_argument("-d", "--days", default = 10)
args = parser.parse_args()

def main():
    create_databases(args.project)    
    dual_launcher()  
    
def create_databases(projectname):
    global dbs_to_create
    dbs_to_create = [str(args.project)+"_hist.db",str(args.project)+"_live.db"]
    for dbname in dbs_to_create:
        if not dbname in glob.glob("*"):
            conn = sqlite3.connect(dbname)
            c = conn.cursor()
            c.execute("""CREATE TABLE tweets (
            id TEXT,
            created_at TEXT,
            author TEXT,
            author_location TEXT,
            author_followers INT,
            author_friends INT,
            hashtags TEXT,
            tweet TEXT,
            in_reply_to TEXT,
            lang TEXT,
            method TEXT,
            UNIQUE(id))
            """)
            conn.close()
            print("Created database: " + dbname)
        else:
            print("Databases already exist with this project name!")
            sys.exit()
            
def backward_collector(back_query,days_back):
    from credentials import consumer_key, consumer_secret, access_token_secret, access_token    
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    conn = sqlite3.connect(dbs_to_create[0])
    conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    
    start = str(datetime.date.today() - datetime.timedelta(days=days_back))
    
    c = tweepy.Cursor(api.search,
                      q=back_query,
                      since = start,
                      wait_on_rate_limit = True,
                      wait_on_rate_limit_notify=True).items()
    while True:
        try:
            tweet = c.next()
            json_tweet = tweet._json

            try:
                tweet_id = json_tweet['id_str']
                #print(tweet_id)
                tweet_created_at = json_tweet['created_at']
                tweet_author = json_tweet['user']['screen_name']
                author_location = json_tweet['user']['location']
                author_followers = json_tweet['user']['followers_count'] if not None else 0
                author_friends = json_tweet['user']['friends_count'] if not None else 0
                hashtags = json_tweet['entities']['hashtags']
                tweet_hashtags = []
                for hashtag in hashtags:
                    tweet_hashtags.append(hashtag['text'])
                tweet_hashtags = ",".join(tweet_hashtags)
                #print(tweet_hashtags)
                tweet_text = re.sub("\n"," ",json_tweet['text'])               
                to_whom = json_tweet['in_reply_to_screen_name']
                tweet_lang = json_tweet['lang']
                conn.execute('INSERT INTO tweets (id, created_at, author, author_location, author_followers, author_friends, hashtags, tweet, in_reply_to, lang, method) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (tweet_id, tweet_created_at, tweet_author, author_location, author_followers, author_friends, tweet_hashtags, tweet_text, to_whom, tweet_lang, "SearchAPI"))
                conn.commit()
                time.sleep(2) # sleep 2 seconds to go softer on the rate limit (15 min * 60 = 900 secs, and 900/2 = 450 requests per 15 min)

            except KeyError:
                pass
            
            except sqlite3.IntegrityError:
                pass
            
        except IOError:
            time.sleep(60*5)
            continue
        except StopIteration:
            break
            
def forward_collector(forward_query):
    from credentials import consumer_key, consumer_secret, access_token_secret, access_token  
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    conn = sqlite3.connect(dbs_to_create[1])
    conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
       
    class MyStreamListener(tweepy.StreamListener):
        def on_data(self, data):
            data = json.loads(data)
            tweet_id = int(data['id'])
            #print(tweet_id)
            tweet_created_at = data['created_at']
            tweet_author = data['user']['screen_name']
            author_location = data['user']['location']
            author_followers = data['user']['followers_count'] if not None else 0
            author_friends = data['user']['friends_count'] if not None else 0
            hashtags = data['entities']['hashtags']
            tweet_hashtags = []
            for hashtag in hashtags:
                tweet_hashtags.append(hashtag['text'])
            tweet_hashtags = ",".join(tweet_hashtags)
            tweet_text = data['text']
            in_reply_to = data['in_reply_to_screen_name']
            tweet_lang = data['lang']
            conn.execute('INSERT INTO tweets (id, created_at, author, author_location, author_followers, author_friends, hashtags, tweet, in_reply_to, lang, method) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (tweet_id, tweet_created_at, tweet_author, author_location, author_followers, author_friends, tweet_hashtags, tweet_text, in_reply_to, tweet_lang, "StreamingAPI"))
            conn.commit()
            
    # Create a stream
    twitter_stream = tweepy.Stream(auth, MyStreamListener())

    # Start streaming and check for errors
    while True:
        try:
            if args.language is "all":
                twitter_stream.filter(track=forward_query)
            else:
                twitter_stream.filter(track=forward_query, languages=[str(args.language)])   
        except KeyError:
            pass
        except sqlite3.IntegrityError: # skip duplicate tweet ids
            pass
            
             
def dual_launcher():
  
    # Set up querystring for backwards search (SearchAPI)
    back_query = args.query
    if args.language is not "all":
        back_query = back_query + " lang:" + str(args.language) 
    
    # Set up querystring for forwards streaming (StreamingAPI)
    forward_query = args.query
    
       
    # Launch
    pool = ThreadPoolExecutor(max_workers = 2)
    pool.submit(backward_collector, back_query,args.days)
    pool.submit(forward_collector, forward_query)
    
    #backward_collector(back_query,args.days)
    #forward_collector(forward_query)
    
    print("Collections are now running.")
    
    
if __name__ == '__main__':
    main()