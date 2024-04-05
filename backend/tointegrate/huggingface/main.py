from sentence_transformers import SentenceTransformer


model_path = "./sentence-bert-swedish-cased"

model = SentenceTransformer(model_path)
#Runt with -d
# Our sentences we like to encode
#toencode = "Hej mitt namn är David"

#Encode the sentence
#embeddings = model.encode(toencode, convert_to_tensor=True)
#print(embeddings)
#Print the embeddings
import os
from flask import Flask, jsonify, request
import json 
app = Flask(__name__)


@app.route('/encode', methods=['POST'])
def classify_review():
    #texts = request.args.get('texts')
    #Get texts from the body of the request
    #Convert the texts json array to a python list
    #Input text is a comma separated list of texts as strings, convert to a list of strings
    texts = request.get_json()
    texts = json.loads(texts)
    print("\"texts\": ", texts)
    #Texts look like texts = ["Jag har en allergi. Kan jag vaccinera mig?"] and are comma separated, convert to a list of strings
    
    #Convert this to a json array
    #Get text from the body of the request
    #texts = request.get_json()
    if texts is None:
        return jsonify(code=403, message="bad request")
    res = []
    for text in texts["texts"]:
        print("text in texts is : ", text)
        res.append(model.encode(text).tolist())
    return res


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google Cloud
    # Run, a webserver process such as Gunicorn will serve the app.
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))