import json
from detect_language import detect_language
from mlp_classifier import mlp_classifier
from pre_negative_intent_classifier import pre_level_classifier
from translation import translator

def create_json_object(pred):
    data = {
        "intent": pred       
    }
    json_object = json.dumps(data)
    return json_object


def lambda_classifier(user_input):
    # Set MPLCONFIGDIR to /tmp
    # os.environ['MPLCONFIGDIR'] = '/tmp'    

    # detect input language
    language = detect_language(user_input)
    
    # classify intent
    trans_user_input = user_input
    pre_intent = pre_level_classifier(trans_user_input)
    if pre_intent == "negative intent":
        pred = pre_intent
    else:        
        if language != "English":
            trans_user_input = translator(trans_user_input)
            trans_user_input = trans_user_input.replace("\n", " ")

        mlp_intent, confidence = mlp_classifier(trans_user_input)
        
        if confidence <= 0.18:
            pred = "negative intent"
        else:
            if mlp_intent == "hr partnership" and confidence <= 0.6:
                pred = "negative intent"
            else:                
                pred = mlp_intent
    
    return pred
        
    # deployment uses the following
    # json_obj = create_json_object(pred)
    


