#Test server for google endpoint

from sentence_transformers import SentenceTransformer

import os
from flask import Flask, jsonify, request
#import json 
app = Flask(__name__)
model_path = "./sentence-bert-swedish-cased"
model = SentenceTransformer(model_path)

#If AIP_HEALTH_ROUTE is not defined, set it to default
if 'AIP_HEALTH_ROUTE' not in os.environ:
    os.environ['AIP_HEALTH_ROUTE'] = '/health'
#If AIP_PREDICT_ROUTE is not defined, set it to default
if 'AIP_PREDICT_ROUTE' not in os.environ:
    os.environ['AIP_PREDICT_ROUTE'] = '/predict'

@app.route(os.environ['AIP_HEALTH_ROUTE'], methods=['GET'])
def health_check():
   return {"status": "healthy"}


@app.route(os.environ['AIP_PREDICT_ROUTE'], methods=['POST'])
def add_income():
    request_json = request.json
    request_instances = request_json['instances']
    prediction=model.encode(request_instances)
    prediction = prediction.tolist()
    output = {'predictions':
                   [
                       {
                           'result' : prediction
                       }
                   ]
               }
    return jsonify(output)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google Cloud
    # Run, a webserver process such as Gunicorn will serve the app.
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))