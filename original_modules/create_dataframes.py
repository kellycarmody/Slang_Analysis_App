#!/usr/bin/env python3

#Prepares dataframes for analysis from list of tweets in clean_data.json file

import ijson
import pandas as pd
from pandas import DataFrame
import json
import ast


def create_df():

    with open('clean_data.json') as json_data:
        data = ijson.items(json_data, 'item')
       

        list_tweets = []
        for tweet in data:
            list_tweets.append(tweet)

        df = pd.DataFrame.from_records(list_tweets) 

    return df

    #df1=df
    #df1['time']=pd.to_datetime(df1['created_at'], format='%a %b %d %H:%M:%S +%f \
    #%Y')
    #df1['time']=df1['time'].dt.round('60min')
    #df2=df1.groupby(['time', 'State', 'Keyword', 'location', 'text', 'user_id', \
    #    'tweet_id', 'lang'])
    #df2.columns = ['Time', 'State', 'Keyword', 'Word Count']

def prepare_df(df):

    df2 = df.set_index(['tweet_id'])
    df2 = df2.drop(['text', 'user_id', 'lang', 'location'],1)
    df2 = df2.groupby(['created_at', 'State', 'Keyword']).size().reset_index()
    df2.columns = ['created_at', 'State', 'Keyword', 'Word Count']

    return df2

