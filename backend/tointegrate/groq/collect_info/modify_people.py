from pymongo import MongoClient
from dotenv import load_dotenv
import os
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_mongodb import MongoDBAtlasVectorSearch
from vertexai.generative_models import GenerativeModel, GenerationConfig
import vertexai.preview.generative_models as generative_models
from groq import Groq
from collection_tools import tools
import traceback
from typing import List

from util import print_tool_call, extract_args, gemini_unfiltered

from langchain_community import FAISS

load_dotenv()

dbclient = MongoClient(os.environ.get("MONGO_DB_URI"))

db = dbclient["collected_info"]
collection = db["people"]
embedder = VertexAIEmbeddings("textembedding-gecko-multilingual")

info_instructions = """Du är en assistent som hanterar ett arkiv som sparar information om personer
Du har fått ny information om en person samt den tidigare kända informationen.
Din uppgift är att uppdatera den tidigare kända informationen med den nya informationen utan att
Tappa någon tidigare information. Om den nya informationen är redan finns i den tidigare kända informationen
behöver du inte förändra något. Lägg aldrig till något som inte står bland den nya informationen.

Viktigt: Svara bara med den nya versionen av informationen, skriv INTE att du har uppdaterat informationen eller andra kommentarer, det förstör i arkivet!
"""

# depricated
description_instructions = """ 
Du är en assistent som hanterar ett arkiv som sparar information om personer. För att identifiera
personer i arkivet används en kortfattad beskrivning av personen. Du har fått ny information om
personen samt den tidigare kända beskrivningen. Din uppgift är att avgöra om beskrivningen bör uppdateras.
Beskrivningen bör endast uppdateras då den nya informationen är relevant för att identifiera personen.
Exempel på relevant information är släktband till en annan person, en beskrivning utan namn eller att 
personen är med i en grupp eller organisation.

Om personen saknar namn och du vet vad personen heter, använd verktyget "sätt_namn" för att ge personen ett namn.
"""

summarize_description_instructions = """
Du är en assistent som summerar information om en person för att skapa en kort text som identifierar personen. Inkludera alltid namn om 
namnet är kännt. Fokusera på hur personen förhåller sig till andra personer, grupper och händelser, lägg inte fokus på personens egenskaper.
"""





tell_if_new_instructions = """Du är en assistent som hjälper användare söka efter personer i ett arkiv.
Användaren har skickat in ett namn som inte var en exakt match bland tidigare namn. Din uppgift är att
avgöra om det nya namnet är en ny person som ska läggas till i arkivet eller om det är en person som redan
finns i arkivet. Du får upp till tre alternativ att välja mellan. Du ska sedan använda ett verktyg för att
förmedla till användaren om personen är ny eller inte.
"""



class Personhandler:
    def __init__(self):
        self.collection = MongoClient(os.environ.get("MONGO_DB_URI"))["collected_info"]["people"]
        self.vector_store = MongoDBAtlasVectorSearch(embedding=embedder, collection=collection, index_name="vector_cosine_index")
        generation_config=GenerationConfig(
                temperature=0.0,
                candidate_count=1,
            ),
        self.info_model = GenerativeModel("gemini-1.0-pro", system_instruction=[info_instructions], safety_settings=gemini_unfiltered)
        self.groq = Groq(api_key=os.environ.get("GROQ_API_KEY")).chat.completions

    def ny_info_person(self,alias, new_info):
        person = self._get_current_info(alias)
        name = person["name"]
        info = person["info"]
        description = person["text"]
        info = self._update_info(info, new_info)
        self._update_description(description, new_info, name, info)
        

    def _get_current_info(self, name) -> Document:
        person = self.collection.find_one({"name": name})
        if person:
            return person
        else:
            nearest = self.vector_store.similarity_search(name,k=3)
            corrected_name = self._check_if_new(name, nearest)
            return self.collection.find_one({"name": corrected_name})
        
    def _update_info(self, old_info, new_info):
        chat = self.info_model.start_chat()
        message = "**Tidigare känd information**\n "+old_info+"\n\n **ny information att inkludera**\n "+new_info
        print("Old info: \n"+old_info)
        response = chat.send_message(message).candidates[0].content.text
        print("Updated info: \n"+response)
        try:
            self.collection.update_one({"info": old_info}, {"$set": {"info": response}})
            return response
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print("Could not update info")
    
    # def _update_description(self, current_description, new_info, name, info):
    #     message = "Nuvarande namn: "+name+"\n"+"**Nuvarande beskrivning**\n "+current_description+"\n\n **Ny information**\n "+new_info
    #     response = self.groq.create(
    #         messages=[
    #             {
    #                 "role": "system",
    #                 "content": description_instructions,
    #             },
    #             {
    #                 "role": "user",
    #                 "content": message,
    #             }
    #         ],
    #         tools=[tools["ändra_beskrivning"], tools["uppdatera_namn"]],
    #         model="llama3-70b-8192",
    #     )
    #     try:
    #         args = extract_args(response.choices[0].message.tool_calls[0])
    #         description = args["ny_beskrivning"]
    #         print_tool_call(response.choices[0].message.tool_calls[0])
    #         metadata = {"name": name, "info": info}
    #         new_person = Document(page_content=description, metadata=metadata)
    #         try:
    #             deletion = self.collection.delete_one({"text": current_description})
    #             self.vector_store.add_documents([new_person])
    #         except Exception as e:
    #             print(e)
    #             print(traceback.format_exc())
    #             print("Could not update description")
    #     except:
    #         try: 
    #             print("Tool was not used to change name or description, text output:")
    #             print(response.choices[0])
    #         except Exception as e:
    #             print(e)
    #             print(traceback.format_exc())

    def _update_description(self, current_description, new_info, name, info):
        message = "Nuvarande namn: "+name+"\n"+"**Information om person**\n"
        try:
            args = extract_args(response.choices[0].message.tool_calls[0])
            description = args["ny_beskrivning"]
            print_tool_call(response.choices[0].message.tool_calls[0])
            metadata = {"name": name, "info": info}
            new_person = Document(page_content=description, metadata=metadata)
            try:
                deletion = self.collection.delete_one({"text": current_description})
                self.vector_store.add_documents([new_person])
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                print("Could not update description")
        except:
            try: 
                print("Tool was not used to change name or description, text output:")
                print(response.choices[0])
            except Exception as e:
                print(e)
                print(traceback.format_exc())


    def _check_if_new(self, name, nearest : List[Document]):
        prompt = "Sökning: "+name+"\nAlternativ: "
        for i, option in enumerate(nearest):
            prompt += str(i+1)+". Namn: "+option.metadata["name"]+"Beskrivning: "+option.page_content+"\n"
        response = self.groq.create(
            messages=[
                {
                    "role": "system",
                    "content": tell_if_new_instructions,
                },
                {
                    "role": "user",
                    "content": name,
                }
            ],
            tools=[tools["identifiera_person"]],
            model="llama3-70b-8192",
        )
        try:
            args = extract_args(response.choices[0].message.tool_calls[0])
            print_tool_call(response.choices[0].message.tool_calls[0])
            if not args["finns_sedan_tidigare"]:
                print("User was not found before")
                name = args["namn"]
                metadata = {"name": name, "info": ""}
                new_person = Document(page_content=args["beskrivning_av_ny_person"], metadata=metadata)
                self.vector_store.add_documents([new_person])
            else:
                print("User was identied as "+args["namn"])
            return args["namn"]
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print("Did not classify person")