#!/usr/bin/env python3

#Appends keyword and state information to tweets and dumps tweets in json file,
#clean_data.json

import ast
import json
from scan_dynamodb import create_state_placeholder, keyword_states_lists, scan_table
from combine_states import new_state_placeholder



def make_df_list(*five_lists):
    '''Creates new list of tweets ready to be translated into dataframes,
    with isolated keyword and state of tweet added to tweet'''

    (new_statepl, valid_state, state_placeholder, states, keyword_list) = five_lists

    
    keyword_placeholder = []
    clean_list = []
    for keyword in keyword_list:
        for item in valid_state:
            if keyword in item:
                clean_list.append(item)
                keyword_placeholder.append(keyword)

    string_list = []
    for tweet in clean_list:
        string_list.append(ast.literal_eval(tweet))


    zipped_list = (zip(string_list, keyword_placeholder, new_statepl))


    ready_list = []
    for tweet in zipped_list:
        tweet[0].update({'Keyword' : tweet[1]})
        tweet[0].update({'State' : tweet[2]})
        ready_list.append(tweet[0])

    return ready_list

def write_df_list(ready_list):
    '''Writes final list of tweets with state and keyword information,
    ready_list, into clean_data.json, to then be converted into dataframes'''

    with open('clean_data.json', 'w') as write_file:
        #for item in valid_state:
        json.dump(ready_list, write_file)


