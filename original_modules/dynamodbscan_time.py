#from __future__ import print_function # Python 2/3 compatibility

#Downloads dynamodb table from AWS as a response object, converts it to a JSON
#object and creates a list of tweets with only clean, accessible state names to
#be used for analysis

import boto3
import json
import decimal
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
import ast
import pandas as pd
from pandas import DataFrame
import ijson

def keyword_states_lists():
    '''List of all possible states and state abbreviations that will be found
    in tweets, and all possible keywords'''

    states = [", AK", ", AL", ", AR", ", AZ", ", CA", ", CO", ", CT", ", DE", ", FL", ", GA", ", HI", ", IA", ", ID",
     ", IL", ", IN", ", KS", ", KY", ", LA", ", MA", ", MD", ", ME", ", MI", ", MN", ", MO", ", MS", ", MT", ", NC",
     ", ND", ", NE", ", NH", ", NJ", ", NM", ", NV", ", NY", ", OH", ", OK", ", OR", ", PA", ", RI", ", SC", ", SD",
     ", TN", ", TX", ", UT", ", VA", ", VT", ", WA", ", WI", ", WV", ", WY",
     "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
     "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
     "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
     "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
     "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
     "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
     "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
     "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
     "West Virginia", "Wisconsin", "Wyoming"]


    keyword_list = ['lit', 'ratchet', 'adulting', 'turnt', 'tfw', 'trill', 'jomo',
    'respek', 'ghosted', 'fam', 'hunty', 'otp']

    two_lists = (states, keyword_list)
    
    return two_lists


keyword_list = ['lit', 'ratchet', 'adulting', 'turnt', 'tfw', 'trill', 'jomo',
'respek', 'ghosted', 'fam', 'hunty', 'otp']



# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

#def scan_table():
#    '''Pulls dynamodb response object from AWS platform, and scans table'''

dynamodb_resource = resource('dynamodb')
table = dynamodb_resource.Table('tweedata')
response = table.scan()
data = response['Items']

while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])


#def create_time_json(response):

time_json = []
for item in response['Items']:
    time_json.append(json.dumps(item, cls=DecimalEncoder))
print(len(time_json))



keyword_placeholder = []
clean_list = []
for keyword in keyword_list:
    for item in time_json:
        if keyword in item:
            clean_list.append(item)
            keyword_placeholder.append(keyword)


string_list = []
for tweet in clean_list:
    string_list.append(ast.literal_eval(tweet))


zipped_list = (zip(string_list, keyword_placeholder))


ready_list = []
for tweet in zipped_list:
    tweet[0].update({'Keyword' : tweet[1]})
    ready_list.append(tweet[0])


#def write_df_list(ready_list):
#'''Writes final list of tweets with state and keyword information,
#ready_list, into clean_data.json, to then be converted into dataframes'''

with open('clean_time.json', 'w') as write_file:
    #for item in valid_state:
    json.dump(ready_list, write_file)


def create_state_placeholder(response, *two_lists):
    '''Loops through tweets from database and creates a new list of only those
    tweets with clear, accessible state names under location (i.e. , AZ or
    Arizona) and creates a placeholder list to later be zipped into final tweet
    list'''

    states, keyword_list = two_lists 

    valid_state = []
    state_placeholder = []
    for item in response['Items']:
        for state in states:
            if state.lower() in item['location']:
                valid_state.append(json.dumps(item, cls=DecimalEncoder))
                state_placeholder.append(state)

    four_lists = (valid_state, state_placeholder, states, keyword_list)
    return four_lists



#def create_df():

with open('clean_data.json') as json_data:
    data = ijson.items(json_data, 'item')
   

    list_tweets = []
    for tweet in data:
        list_tweets.append(tweet)

    df = pd.DataFrame.from_records(list_tweets) 


df1=df
df1['time']=pd.to_datetime(df1['created_at'], format='%a %b %d %H:%M:%S +%f \
%Y')
df1['time']=df1['time'].dt.hour
bins = [0,6,12,18,24]
df1['time'] = pd.cut(df1['time'],bins)
#print(df1['time'])
df2=df1.groupby(['time', 'State', 'Keyword', 'location', 'text', 'user_id', \
'tweet_id', 'lang'])
df2.columns = ['Time', 'State', 'Keyword', 'Word Count']


#def prepare_df(df):

df2 = df.set_index(['tweet_id'])
df2 = df2.drop(['text', 'user_id', 'lang', 'location'],1)
df2 = df2.groupby(['time', 'Keyword']).size().reset_index()
df2.columns = ['Time', 'Keyword', 'Word Count']
print(df2)

import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from create_dataframes import create_df, prepare_df 

#def create_histogram(df2, keyword):
#Word Count for Lit

df3=df2[df2['Keyword']== 'lit']
df3=df3.groupby(['Time'])[['Word Count']].sum().reset_index()
df3.hist()
df3.set_index('Time')[['Word Count']].plot.bar(figsize=(20, 5))
plt.title('Words Count For "'+ 'lit' +'" Word')
plt.ylabel('Words Count')
plt.savefig('lit' + 'time' + '.png')


df3=df2[df2['Keyword']== 'adulting']
df3=df3.groupby(['Time'])[['Word Count']].sum().reset_index()
df3.hist()
df3.set_index('Time')[['Word Count']].plot.bar(figsize=(20, 5))
plt.title('Words Count For "'+ 'adulting' +'" Word')
plt.ylabel('Words Count')
plt.savefig('adulting' + 'time' + '.png')


df3=df2[df2['Keyword']== 'fam']
df3=df3.groupby(['Time'])[['Word Count']].sum().reset_index()
df3.hist()
df3.set_index('Time')[['Word Count']].plot.bar(figsize=(20, 5))
plt.title('Words Count For "'+ 'fam' +'" Word')
plt.ylabel('Words Count')
plt.savefig('fam' + 'time' + '.png')






