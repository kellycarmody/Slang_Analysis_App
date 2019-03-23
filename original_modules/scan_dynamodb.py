#from __future__ import print_function # Python 2/3 compatibility

#Downloads dynamodb table from AWS as a response object, converts it to a JSON
#object and creates a list of tweets with only clean, accessible state names to
#be used for analysis

import boto3
import json
import decimal
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr




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



# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def scan_table():
    '''Pulls dynamodb response object from AWS platform, and scans table'''

    dynamodb_resource = resource('dynamodb')
    table = dynamodb_resource.Table('tweedata')
    response = table.scan()

    return response


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
