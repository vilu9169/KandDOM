#gcloud auth print-identity-token
from  langchain.embeddings.base import Embeddings
import subprocess
import requests
from typing import List


res = ""
while res == "":
    try :
        print("Trying to get token")
        res = subprocess.check_output("gcloud auth print-identity-token", shell=True, timeout=2)
    except subprocess.TimeoutExpired:
        res = ""
#Convert auth to string and remove last \r\n if on windows
if(res[-2] == 13):
    res = res.decode("utf-8")[:-2]
else:
    res = res.decode("utf-8")[:-1]
#Create a new class of embeddings called Own Embedder
class ownEmbedder(Embeddings):
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        str = "https://kanddomembedder-k2a2qapzpa-ew.a.run.app/encode?api_key=MyCustomerApiKey&texts=["
        for text in texts:
            str += "\"" + text + "\","
        str = str[:-1] + "]"
        #Create a http get request to the server, If no response within 1 second then retry
        print("Token: ", res)
        headers = {"Authorization" : "Bearer " + res, "Content-Type" : "application/json", "charset" : "utf-8"}
        #Send a get request to the server, if it times out after 2 sec retry
        response = ""
        while(response == ""):
            try:
                print("Trying to get response")
                response = requests.get(str, headers=headers, timeout=2)
            except requests.exceptions.Timeout:
                response = ""
        print(response.text)
        #Turn the string response to a list of lists of floats
        return response.json()
    def embed_query(self, texts: str) -> List[float]:
        str = "https://kanddomembedder-k2a2qapzpa-ew.a.run.app/encode?api_key=MyCustomerApiKey&texts=[" + "\"" + texts + "\"]"
        #Create a http get request to the server
        print("Token: ", res)
        headers = {"Authorization" : "Bearer " + res, "Content-Type" : "application/json", "charset" : "utf-8"}
        
        response = requests.get(str, headers=headers)
        #
        print(response.text)
        return response.json()[0]
output = ownEmbedder().embed_documents(["Hej", "Då"])
print(output)
output = ownEmbedder().embed_query("Hej")
print(output)