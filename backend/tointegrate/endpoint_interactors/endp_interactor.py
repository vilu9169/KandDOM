#Program that interacts with a deployed custom google vertex ai endpoint
#Think this is garbage and replaced by endpoint_test
import requests
import json

def interact_with_endpoint(texts, endpoint):
    #Make a request to the endpoint
    url = endpoint
    data = json.dumps({"instances": texts})
    headers = {"Content-Type": "application/json", "Authorization": "Bearer "}
    response = requests.post(url, headers=headers, data=data)
    #Return the response
    print(response)
    return response.json()

#Test the function
texts = ["Jag har en allergi. Kan jag vaccinera mig?"]
print(interact_with_endpoint(texts, "http://34.141.162.207:8080/predict"))#"http://localhost:8080/predict"))