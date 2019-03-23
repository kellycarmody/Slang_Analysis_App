#!/usr/bin/env python3

#Sets up dynamodb table connection, prepares a dictionary of tweets to make
#them compatible with dynamodb format, and batch writes tweets to dynamodb

import json
import tweepyconfig as config
import boto3

from tweepy_pull import tweepy_setup, save_tweets


def dynamo_setup():
    '''Creates dynamodb resource to use for database table'''
    
    session = boto3.Session(profile_name='default')
    # Any clients created from this session will use credentials from the [default] section of ~/.aws/credentials.
    dev_s3_client = session.client('s3')
    # Get the service resource.

    dynamodb_resource = boto3.resource('dynamodb')
    dynamodb_client = boto3.client('dynamodb')

    client_resource = (dynamodb_client, dynamodb_resource)

    return client_resource

def makeit(*client_resource):
    '''Creates dynamodb table'''

    dynamodb_client, dynamodb_resource = client_resource

    table_exists = False
    try:
        table_description = dynamodb_client.describe_table(TableName='tweedata')
        table_exists = True


    except Exception as e:
        if "Requested resource not found: Table" in str(e):
                
            table = dynamodb_resource.create_table(
                TableName='tweedata',
                KeySchema=[
                    {
                        'AttributeName': 'tweet_id',
                        'KeyType': 'HASH'
                    },
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'tweet_id',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName='tweedata')
            table_exists = True
        else:
            raise
    table = dynamodb_resource.Table('tweedata')

    return table


def fill_list(clean_tweets):
    '''Creates a dictionary for selected components of each tweet (tweet_id,
    lang etc.) then combined all tweet dictionaries together in a list'''

    filler_list = []
    filler = dict()

    for x in range(len(clean_tweets)):
        filler = {}
        filler['tweet_id']= clean_tweets[x]['id_str']
        filler['lang'] = clean_tweets[x]['lang']
        filler['user_id'] = clean_tweets[x]['user']['id']
        filler['location'] = clean_tweets[x]['user']['location'].lower() if \
        clean_tweets[x]['user']['location'] else None
        filler['created_at'] = clean_tweets[x]['created_at']
        filler['text'] = clean_tweets[x]['text'].lower()
        filler_list.append(filler)

    for dynamo_dict in filler_list:
        for k, v in dynamo_dict.items():
            if v is None:
                dynamo_dict[k] = 'empty_string'
            elif type(v) == type(dynamo_dict):
                replace(v)
    print(filler_list)

    return filler_list


def fillit(table, filler_list):
    '''Adds all tweets to Dynamodb at the same time in a batch'''

    with table.batch_writer() as batch:
        for item in filler_list:
            batch.put_item(Item=item)





