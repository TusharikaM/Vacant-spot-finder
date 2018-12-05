import boto3
BUCKET = ' your bucket name' #input your bucket name
KEY = ' My file' #input your json file



    
    
    # --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    
    # --------------- Functions that control the skill's behavior ------------------

def get_help_response(userID): 
    
        
        #if (text == "{\"Occupied\": \"true\"}" ) {alexa respose should be no vacant spot} else {alexa response is there is vacant spot}
        
    client = boto3.client('s3',
                       aws_access_key_id=' "Enter your AWS Access Key"',
                       aws_secret_access_key=' "Enter your AWS secret access key" '
                     )
    result = client.get_object(Bucket=BUCKET, Key=KEY)
    # Read the object (not compressed):
    text = result["Body"].read().decode()
    if (text.find('true') != -1 ) :
        status = "Sit tight! searching a spot for you. Oops, I am sorry there is no spot available at this time."
    else:
        status = "Sit tight! Searching a a spot for you. Found it! There is a spot available."
    
    session_attributes = {}
    card_title = "Help"
    speech_output = status 
    should_end_session = True
    reprompt_text = "Are you still there? All the seats might be gone"
    return build_response(session_attributes, build_speechlet_response(
    card_title, speech_output, reprompt_text, should_end_session))
    
def get_welcome_response(userID):
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "I can help you find a spot"
    should_end_session = False
    reprompt_text = "Are you still there? All the seats might be gone"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
        
# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    userID = session['user']['userId']

    # Dispatch to your skill's launch
    return get_welcome_response(userID)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    userID = session['user']['userId']

    if intent_name == "READFILE": #Input your intent name
        return get_help_response(userID)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request(userID)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response(userID)
    else:
         raise ValueError("Invalid intent")        


#-----------------Main Handler---------------
def lambda_handler(event, context):
    
    if ('session' in event):
        print("event.session.application.applicationId=" +
              event['session']['application']['applicationId'])
        if event['session']['new']:
            on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
        if ('request' in event):                       
            if event['request']['type'] == "LaunchRequest":
                return on_launch(event['request'], event['session'])
            elif event['request']['type'] == "IntentRequest":
                return on_intent(event['request'], event['session'])
            elif event['request']['type'] == "SessionEndedRequest":
                return on_session_ended(event['request'], event['session'])
    