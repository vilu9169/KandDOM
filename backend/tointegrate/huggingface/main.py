from sentence_transformers import SentenceTransformer


model_path = "./sentence-bert-swedish-cased"

model = SentenceTransformer(model_path)

# Our sentences we like to encode
#toencode = "Hej mitt namn är David"

#Encode the sentence
#embeddings = model.encode(toencode, convert_to_tensor=True)
#print(embeddings)
#Print the embeddings
import os
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/encode', methods=['GET'])
def classify_review():
    texts = request.args.get('texts')
    #Convert the texts json array to a python list
    texts = texts[1:-1].replace("\"", "").split(",")
    api_key = request.args.get('api_key')
    if texts is None or api_key != "MyCustomerApiKey":
        return jsonify(code=403, message="bad request")
    res = []
    for text in texts:
        print("text: ", text)
        res.append(model.encode(text).tolist())
    return res


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google Cloud
    # Run, a webserver process such as Gunicorn will serve the app.
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))