import json
from collections import OrderedDict

'''
Format

Intent
Intent
Intent
Intent, Name, Type, Name, Type, ...
'''


def make_intents(file):
    f = open(file,'r')
    intent_list = []
    intents = f.read().split('\n')
    intents.append('AMAZON.HelpIntent')
    intents.append('AMAZON.StopIntent')
    intents.append('AMAZON.CancelIntent')
    for i in intents:
        i_dict = OrderedDict()
        i_info = i.split(',')
        i_dict['intent'] = i_info[0]
        if len(i_info) > 1:
            i_dict['slots'] = []
            
            if (len(i_info)-1) % 2 != 0:
                print 'Invalid number of fields'
                return
            
            for x in xrange(1,len(i_info)-1,2):
                slot = OrderedDict()
                slot['name'] = i_info[x]
                slot['type'] = i_info[x+1]
                i_dict['slots'].append(slot)
        intent_list.append(i_dict)
    f.close()

    intents_wrap = {}
    intents_wrap['intents'] = intent_list
    
    with open('intents.json','w') as dt:
        json.dump(intents_wrap,dt)


make_intents('intents.txt')
