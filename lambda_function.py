from vc_check import *
import time, datetime

app_id = 'amzn1.ask.skill.9c45de62-65e3-41f2-bd27-8486d1cb1949'

def lambda_handler(event, context):
    if event['session']['application']['applicationId'] != app_id:
        raise ValueError('Invalid Application ID')
    
    if event['session']['new']:
        on_session_started({'requestId':event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == 'LaunchRequest':
        return on_launch(event['request'], event['session'])
    if event['request']['type'] == 'IntentRequest':
        return handle_intent(event['request'], event['session'])
    if event['request']['type'] == 'SessionEndedRequest':
        return on_session_ended(event['request'], event['session'])


#-------------Start and Launch-----------------
    
def on_session_started(request_id, session):
    pass
    
def on_launch(launch_request, session):
    return get_welcome_response()

def get_welcome_response():
    title = "Welcome"
    text = "Welcome to VC Checker. " \
           "You can ask for the price of a virtual currency. " \
           "Say \"Tell me the price of\"" \
           " currency to get the price"
    reprompt_text = "Say \"Tell me the price of\"" \
                    " currency to get the price"
    should_end_session = False
    statement = build_statement(title,text,reprompt_text, should_end_session)
    return build_response(statement,{})

#------------Intent Requests--------------------

def handle_intent(intent_request, session):
    intent = intent_request['intent']

    if intent['name'] == 'GetPrice':
        return get_price(intent, session)
    elif intent['name'] == 'AMAZON.HelpIntent':
        return help_intent()
    elif intent['name'] == 'AMAZON.CancelIntent':
        return cancel_intent()
    elif intent['name'] == 'AMAZON.StopIntent':
        return stop_intent()
    else:
        raise ValueError('Invalid intent: %s' % (intent['name']))

#---------Custom Intent Requests-------------

def get_price(intent, session):

    title = intent['name']
    text = 'Error occurred. Please try again'
    should_end_session = False

    if 'Currency' in intent['slots'] and 'value' in intent['slots']['Currency']:
        speech = intent['slots']['Currency']['value']
        currency = speech_to_currency(speech.lower())
        if currency != None:
            res = call_api(currency)
            if res != None:
                #text = 'The price of 1 %s as of %s is $%s' % (speech, get_date_from_epoch(res['last_updated']), res['price_usd'])
                text = 'The price of 1 %s is $%s. You can ask for another price or say "I\'m done" to close this skill' % (speech, res['price_usd'])
        else:
            text = 'That virtual currency is not supported by this skill. Sorry!'    

    statement = build_statement(title,text,None,should_end_session)
    return build_response(statement,{})


def get_date_from_epoch(seconds):
    seconds = int(seconds)
    num_to_month = [None, 'January','February','March','April','May','June','July','August','September','October','November','December']
    date = datetime.datetime.fromtimestamp(seconds)
    return '%s %d, %d %s' % (num_to_month[date.month], date.day, date.year, time.strftime('%I:%M:%S%p', time.localtime(seconds)))

#--------Required Intent Requests---------------

def help_intent():
    return get_welcome_response()
    
def cancel_intent():
    return session_end_request()

def stop_intent():
    return session_end_request()

def session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using the VC Checker skill. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response(build_statement(
        card_title, speech_output, None, should_end_session),{})


def on_session_ended(request,session):
    pass


#-----------------Builders-----------------

def build_statement(title, text, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': text
        },
        'card': {
            'type': "Simple",
            'title': title,
            'content': text
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(statement, session_attributes):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': statement
    }
