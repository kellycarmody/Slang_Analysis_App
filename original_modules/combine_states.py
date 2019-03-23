#!/usr/bin/env python3

#Combines state written out in full with state abbreviation, into one clean
#state abbreviation for charts

from scan_dynamodb import create_state_placeholder 


def new_state_placeholder(*four_lists):
    '''Creates a state placeholder list merging the two possible options for a
    state under location, (i.e. , AZ or Arizona) into one option (i.e. AZ) to be
    used in the final histogram'''

    valid_state, state_placeholder, states, keyword_list = four_lists

    new_statepl = []
    for state in state_placeholder:
        if state == ', AL':
            new_statepl.append('AL')
        elif state == 'Alabama':
            new_statepl.append('AL')
        elif state == ', AK':
            new_statepl.append('AK')
        elif state == 'Alaska':
            new_statepl.append('AK')
        elif state == ', AZ':
            new_statepl.append('AZ')
        elif state == 'Arizona':
            new_statepl.append('AZ')
        elif state == ', CA':
            new_statepl.append('CA')
        elif state == 'California':
            new_statepl.append('CA')
        elif state == ', CO':
            new_statepl.append('CO')
        elif state == 'Colorado':
            new_statepl.append('CO')
        elif state == ', CT':
            new_statepl.append('CT')
        elif state == 'Connecticut':
            new_statepl.append('CT')
        elif state == ', DE':
            new_statepl.append('DE')
        elif state == 'Delaware':
            new_statepl.append('DE')
        elif state == ', FL':
            new_statepl.append('FL')
        elif state == 'Florida':
            new_statepl.append('FL')
        elif state == ', GA':
            new_statepl.append('GA')
        elif state == 'Georgia':
            new_statepl.append('GA')
        elif state == ', HI':
            new_statepl.append('HI')
        elif state == 'Hawaii':
            new_statepl.append('HI')
        elif state == ', ID':
            new_statepl.append('ID')
        elif state == 'Idado':
            new_statepl.append('ID')
        elif state == ', IL':
            new_statepl.append('IL')
        elif state == 'Illinois':
            new_statepl.append('IL')
        elif state == ', IN':
            new_statepl.append('IN')
        elif state == 'Indiana':
            new_statepl.append('IN')
        elif state == ', IA':
            new_statepl.append('IA')
        elif state == 'Iowa':
            new_statepl.append('IA')
        elif state == ', KS':
            new_statepl.append('KS')
        elif state == 'Kansas':
            new_statepl.append('KS')
        elif state == ', KY':
            new_statepl.append('KY') 
        elif state == 'Kentucky':
            new_statepl.append('KY')
        elif state == ', LA':
            new_statepl.append('LA')
        elif state == 'Louisiana':
            new_statepl.append('LA')
        elif state == ', ME':
            new_statepl.append('ME')
        elif state == 'Maine':
            new_statepl.append('ME')
        elif state == ', MD':
            new_statepl.append('MD')
        elif state == 'Maryland':
            new_statepl.append('MD')
        elif state == ', MA':
            new_statepl.append('MA')
        elif state == 'Massachusetts':
            new_statepl.append('MA')
        elif state == ', MI':
            new_statepl.append('MI')
        elif state == 'Michigan':
            new_statepl.append('MI')
        elif state == ', MN':
            new_statepl.append('MN')
        elif state == 'Minnesota':
            new_statepl.append('MN')
        elif state == ', MS':
            new_statepl.append('MS')
        elif state == 'Mississippi':
            new_statepl.append('MS')
        elif state == ', MO':
            new_statepl.append('MO')
        elif state == 'Missouri':
            new_statepl.append('MO')
        elif state == ', MT':
            new_statepl.append('MT')
        elif state == 'Montana':
            new_statepl.append('MT')
        elif state == ', NE':
            new_statepl.append('NE')
        elif state == 'Nebraska':
            new_statepl.append('NE')
        elif state == ', NV':
            new_statepl.append('NV')
        elif state == 'Nevada':
            new_statepl.append('NV')
        elif state == ', NH':
            new_statepl.append('NH')
        elif state == 'New Hampshire':
            new_statepl.append('NH')
        elif state == ', NJ':
            new_statepl.append('NJ')
        elif state == 'New Jersey':
            new_statepl.append('NJ')
        elif state == ', NM':
            new_statepl.append('NM')
        elif state == 'New Mexico':
            new_statepl.append('NM')
        elif state == ', NY':
            new_statepl.append('NY')
        elif state == 'New York':
            new_statepl.append('NY')
        elif state == ', NC':
            new_statepl.append('NC')
        elif state == 'North Carolina':
            new_statepl.append('NC')
        elif state == ', ND':
            new_statepl.append('ND')
        elif state == 'North Dakota':
            new_statepl.append('ND')
        elif state == ', OH':
            new_statepl.append('OH')
        elif state == 'Ohio':
            new_statepl.append('OH')
        elif state == ', OK':
            new_statepl.append('OK')
        elif state == 'Oklahoma':
            new_statepl.append('OK')
        elif state == ', OR':
            new_statepl.append('OR')
        elif state == 'Oregon':
            new_statepl.append('OR') 
        elif state == ', PA':
            new_statepl.append('PA')
        elif state == 'Pennsylvania':
            new_statepl.append('PA')
        elif state == ', RI':
            new_statepl.append('RI')
        elif state == 'Rhode Island':
            new_statepl.append('RI')
        elif state == ', SC':
            new_statepl.append('SC')
        elif state == 'South Carolina':
            new_statepl.append('SC')
        elif state == ', SD':
            new_statepl.append('SD')
        elif state == 'South Dakota':
            new_statepl.append('SD')
        elif state == ', TN':
            new_statepl.append('TN')
        elif state == 'Tennessee':
            new_statepl.append('TN')
        elif state == ', TX':
            new_statepl.append('TX')
        elif state == 'Texas':
            new_statepl.append('TX')
        elif state == ', UT':
            new_statepl.append('UT')
        elif state == 'Utah':
            new_statepl.append('UT')
        elif state == ', VT':
            new_statepl.append('VT')
        elif state == 'Vermont':
            new_statepl.append('VT')
        elif state == ', VA':
            new_statepl.append('VA')
        elif state == 'Virginia':
            new_statepl.append('VA')
        elif state == ', WA':
            new_statepl.append('WA')
        elif state == 'Washington':
            new_statepl.append('WA')
        elif state == ', WV':
            new_statepl.append('WV')
        elif state == 'West Virginia':
            new_statepl.append('WV')
        elif state == ', WI':
            new_statepl.append('WI')
        elif state == 'Wisconsin': 
            new_statepl.append('WI')
        elif state == ', WY':
            new_statepl.append('WY')
        elif state == 'Wyoming':
            new_statepl.append('WY')

    five_lists = (new_statepl, valid_state, state_placeholder, states, keyword_list)

    return five_lists
