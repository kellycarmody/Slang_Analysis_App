#!/usr/bin/env python3

#Pulls in tweets from tweepy API containing specified slang keywords, ensuring
#that tweets are paginated so as not to store the same tweet in another query,
#and cleaning list of tweets to remove all retweets

import tweepy
import json
import tweepyconfig as config
import oauth2


def tweepy_setup():
    '''Sets up tweepy API authorization using credentials from config file, kept
    separately. Uses tweepy cursor method with search method in order to
    paginate tweets to store for database, so same tweets will not be pulled
    again in repeated queries''' 

    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    query = 'lit OR ratchet OR adulting OR turnt OR TFW OR trill OR JOMO OR \
    respek OR ghosted OR fam OR hunty OR OTP'

    cursor = tweepy.Cursor(api.search, q=query, count=100, lang = "en") 

    return cursor 

def save_tweets(cursor):
    '''Stores tweets in json format in order to prepare them for being placed
    in dynamodb database, removes all retweets in order to produce clean data'''

    tweets = []
    item_count = 0
    for tweet in cursor.items():
        tweets.append(tweet._json)
        item_count +=1
        if item_count>=100:
            break

    clean_tweets = []
    for tweet in tweets:
        if not tweet['text'].startswith('RT '): 
            clean_tweets.append(tweet)

    return clean_tweets


