from pymongo import MongoClient
from dotenv import load_dotenv
import os
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_mongodb import MongoDBAtlasVectorSearch
from vertexai.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models
from groq import Groq
from collect_info.collection_tools import tools

load_dotenv()

dbclient = MongoClient(os.environ.get("MONGO_DB_URI"))

db = dbclient["collected_info"]
collection = db["people"]
embedder = VertexAIEmbeddings("textembedding-gecko-multilingual")

#text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)

#docs = text_splitter.split_documents(data)

metadata = {"other" : "hi world"}

docs = [Document(page_content="I like you", metadata=metadata)]

print("docs:" ,docs[0])

# vector_search = MongoDBAtlasVectorSearch.from_documents(documents=docs, embedding=embedder, collection=collection,
#                                            index_name="vector_cosine_index") 

vector_search = MongoDBAtlasVectorSearch(embedding=embedder, collection=collection, index_name="vector_cosine_index")
query = "I love you"
results = vector_search.similarity_search(query)

for result in results:
    print("Results:", result.page_content, )
    try:
        print("metadata: "+result.metadata["other"])
    except:
        print("No metadata")
try:
    result = collection.delete_one({"text": "I like you"})
    print(result)
except:
    print("Could not delete")

#embedding = embedder.embed("Carl Persson")

# print(embedding[0])
# person = {
#     "name": "Carl Persson",
#     "age": 35,
#     "city": "Stockholm",
#     "vector" : embedding[0],
# }


# try:
#     collection.insert_one(person)
#     print("Person added")
# except Exception as e:
#     print(e)
#     print("Person not added")

info_instructions = """Du är en assistent som hanterar ett arkiv som sparar information om personer
Du har fått ny information om en person samt den tidigare kända informationen.
Din uppgift är att uppdatera den tidigare kända informationen med den nya informationen utan att
Tappa någon tidigare information. Du bör därför generera ett svar som är längre än den tidigare
informationen, men försök att sortera information så att sammanhängde information presenteras tillsammans
och eventuellt bygger på varandra.
"""

description_instructions = """
Du är en assistent som hanterar ett arkiv som sparar information om personer. För att identifiera
personer i arkivet används en kortfattad beskrivning av personen. Du har fått ny information om
personen samt den tidigare kända beskrivningen. Din uppgift är att avgöra om beskrivningen bör uppdateras.
Beskrivningen bör endast uppdateras då den nya informationen är relevant för att identifiera personen.
Exempel på relevant information är släktband till en annan person, en beskrivning utan namn eller att 
personen är med i en grupp eller organisation.
"""


rawdog = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
}


class Personhandler:
    def __init__(self):
        self.collection = MongoClient(os.environ.get("MONGO_DB_URI"))["collected_info"]["people"]
        self.searcher = MongoDBAtlasVectorSearch(embedding=embedder, collection=collection, index_name="vector_cosine_index")
        self.info_model = GenerativeModel("gemini-1.0-pro", system_instruction=[info_instructions], safety_settings=rawdog)
        self.description_model = Groq(api_key=os.environ.get("GROQ_API_KEY")).chat.completions
    def handle_ny_info_person(self,alias, new_info):
        person = self._get_current_info(alias)
        name = person["name"]
        old_info = person["info"]
        description = person["description"]
        self._update_info(old_info, new_info)
        self._
        

    def _get_current_info(self, name) -> Document:
        person = self.collection.find_one({"name": name})
        if person:
            return person
        else:
            nearest = self.searcher.similarity_search(name,k=1)[0]
            return nearest
        
    def _update_info(self, old_info, new_info):
        chat = self.info_model.start_chat()
        message = "**Tidigare känd information**\n "+old_info+"\n\n **ny information att inkludera**\n "+new_info
        response = chat.send_message(message)
        try:
            self.collection.update_one({"info": old_info}, {"$set": {"info": response.candidates[0].message.content}})
        except Exception as e:
            print(e)
            print("Could not update info")
    
    def _update_description(self, current_description, new_info):
        message = "**Nuvarande beskrivning**\n "+current_description+"\n\n **Ny information**\n "+new_info
        response = self.description_model.create(
            messages=[
                {
                    "role": "system",
                    "content": description_instructions,
                },
                {
                    "role": "user",
                    "content": message,
                }
            ],
            tools=[tools["ändra_beskrivning"], tools["sätt_namn"]],
            model="llama3-8b-8192",
        )
        try:
            description = response.choices[0].message.function_calls[0].parameters["ny_info"]
            try:
                self.collection.update_one({"description": current_description}, {"$set": {"description": description}})
            except Exception as e:
                print(e)
                print("Could not update description")
        except:
            pass