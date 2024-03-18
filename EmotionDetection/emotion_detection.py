import requests
import json

def emotion_predictor(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    myobj = { "raw_document": { "text": text_to_analyse } }
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    response = requests.post(url, json = myobj, headers=header)

    #create a json formatted response
    formatted_response = json.loads(response.text)

    #error handling with status code
    if response.status_code != 200:
        return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
               }

    # Extracting values for anger, disgust, fear, joy, and sadness
    emotion_predictions = formatted_response.get('emotionPredictions', [])
    if emotion_predictions:
        emotions = emotion_predictions[0].get('emotion', {})
        anger_score = emotions.get('anger', 0)
        disgust_score = emotions.get('disgust', 0)
        fear_score = emotions.get('fear', 0)
        joy_score = emotions.get('joy', 0)
        sadness_score = emotions.get('sadness', 0)

    #get the dominant emotion by finding the highest number
    highest = max(anger_score, disgust_score, fear_score, joy_score, sadness_score)

    # Initialize variables to store the key and maximum value
    max_key = None
    max_value = float('-inf')  # Start with negative infinity as initial maximum value

    # Iterate over dictionary items
    for key, value in emotions.items():
        # Check if the current value is greater than the current maximum value
        if value > max_value:
            max_key = key  # Update the key with the maximum value
            max_value = value  # Update the maximum value

    #return data in specified structure for task
    if max_value == highest:
        return {
                    'anger': anger_score,
                    'disgust': disgust_score,
                    'fear': fear_score,
                    'joy': joy_score,
                    'sadness': sadness_score,
                    'dominant_emotion': max_key
                }
