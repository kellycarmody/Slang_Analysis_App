#!/usr/bin/env python3

#The main task script for the slang analysis project. This script includes two
#celery(task scheduler) tasks. The first is celery_main, which pulls tweets using the tweepy API that include
#location data, cleans the data and uploads it to a dynamodb database, hosted
#on Amazon Web Services(AWS). The second celery task is analyze_main, which
#downloads the tweets from the dynamodb database and restructures them into
#dataframes to be used for analysis, creating histograms comparing the
#frequency of slang term use across different states. 

#Module dependencies to run tasks are tweepy_pull, upload_dynamodb,
#scan_dynamodb, combine_states, create_clean_data, create_dataframes, and
#create_histograms

#Task time is currently set to run every minute to pull in tweets from tweepy,
#every hour to analyze them, but this can be changed by changing the crontab
#schedule

from celery import Celery
from celery import group
from celery.schedules import crontab
import datetime
import tweepy
import json
import tweepyconfig as config
import boto3

from tweepy_pull import tweepy_setup, save_tweets
from upload_dynamodb import dynamo_setup, makeit, fill_list, fillit

from scan_dynamodb import create_state_placeholder, keyword_states_lists, scan_table
from combine_states import new_state_placeholder
from create_clean_data import make_df_list, write_df_list
from create_dataframes import create_df, prepare_df
from create_histograms import create_histogram


app = Celery('tasks.py', broker='redis://localhost:6379/0')

@app.task
def celery_main():
    '''Main celery task, pulls tweets from twitter and saves in json format in
    tweepy_pull.py, creates dynamodb database if not existing, formats tweets
    appropriately for dynamodb and batch writes tweets to dynamodb'''

    #From tweepy_pull.py
    cursor = tweepy_setup()
    save_tweets(cursor)
    clean_tweets = save_tweets(cursor)

    #From upload_dynamodb.py
    client_resource = dynamo_setup() 
    table = makeit(*client_resource) 
    fill_list(clean_tweets)
    filler_list = fill_list(clean_tweets)
    fillit(table, filler_list) 

@app.task
def analyze_main():
    '''Analysis task to create histograms. Downloads response from dynamodb
    database, scans database, translates data into json and puts data in
    dataframes, then creates histograms from dataframes'''

    #From scan_dynamodb.py
    two_lists = keyword_states_lists()
    response = scan_table()
    four_lists = create_state_placeholder(response, *two_lists)

    #From combine_states.py
    five_lists = new_state_placeholder(*four_lists)

    #From create_clean_data.py
    ready_list = make_df_list(*five_lists)
    make_df_list(*five_lists)
    write_df_list(ready_list)

    #From create_dataframes.py 
    df = create_df()
    df2 = prepare_df(df)
    
    #From create_histograms.py
    create_histogram(df2, 'lit')
    create_histogram(df2, 'adulting')
    create_histogram(df2, 'ratchet')
    create_histogram(df2, 'turnt')
    create_histogram(df2, 'tfw')
    create_histogram(df2, 'trill')
    create_histogram(df2, 'jomo')
    create_histogram(df2, 'respek')
    create_histogram(df2, 'fam')
    create_histogram(df2, 'hunty')
    create_histogram(df2, 'otp')


app.conf.update(
        CELERYBEAT_SCHEDULE={
         'populate-database-each-hour': {
            'task': 'tasks.celery_main',
           # 'schedule': crontab(hour="*/1"),
            'schedule': datetime.timedelta(seconds=60),
        },
        'produce-histogram-charts': {
            'task': 'tasks.analyze_main',
           # 'schedule': crontab(minute=0),
           'schedule': datetime.timedelta(seconds=60),
        },
    },
)

