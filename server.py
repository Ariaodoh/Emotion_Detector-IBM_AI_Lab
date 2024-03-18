''' Executing this function initiates the application of emotion
    detector to be executed over the Flask channel and deployed on
    localhost:5000.
'''
# Import Flask, render_template, request from the flask pramework package :
from flask import Flask, render_template, request
# Import the emotion_predictor function from the package created:
from EmotionDetection.emotion_detection import emotion_predictor

#Initiate the flask app :
app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emo_detect():
    ''' This code receives the text from the HTML interface and 
        runs emotion detection over it using emotion_predictor()
        function. The output returned shows the label and its confidence 
        score for the provided text.
    '''
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_predictor(text_to_analyze)
    anger = response['anger']
    disgust = response['disgust']
    fear = response['fear']
    joy = response['joy']
    sadness = response['sadness']
    dom_emo = response['dominant_emotion']

    if dom_emo is None:
        return "Invalid input ! Try again."

    response = (    f"For the given statement, the system response is:\n"
                    f"'anger': {anger},\n"
                    f"'disgust': {disgust},\n"
                    f"'fear': {fear},\n"
                    f"'joy': {joy},\n"
                    f"'sadness': {sadness}.\n"
                    f"The dominant emotion is {dom_emo}."
                )
    return response

@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    return render_template('index.html')

if __name__ == "__main__":
    #This functions executes the flask app and deploys it on localhost:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
