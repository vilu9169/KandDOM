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

from langchain_community.vectorstores import FAISS

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

create_description_instructions = """
Du är en assistent som summerar information om en person för att skapa en kort text som identifierar personen. Inkludera alltid namn om 
namnet är kännt. Fokusera på hur personen förhåller sig till andra personer, grupper och händelser, lägg inte fokus på personens egenskaper.
"""





tell_if_new_person_instructions = """Du är en assistent som hjälper användare söka efter personer i ett arkiv.
Användaren har skickat in ett namn som inte var en exakt match bland tidigare namn. Din uppgift är att
avgöra om det nya namnet är en ny person som ska läggas till i arkivet eller om det är en person som redan
finns i arkivet. Du får upp till tre alternativ bland tidigare kända personer att välja mellan. Du ska sedan använda ett verktyg för att
förmedla till användaren om personen är ny eller inte.
"""


tell_if_new_group_instructions = """
Du är en assistent som hjälper användare söka efter grupper i ett arkiv. Användaren har skickat in en beskrivning av en grupp som inte var en exakt match bland tidigare grupper. 
Din uppgift är att avgöra om den nya gruppen är en ny grupp som ska läggas till i arkivet eller om det är en grupp som redan finns i arkivet. 
Du får upp till tre alternativ bland tidigare kända grupper att välja mellan. Om gruppen finns i arkivet sedan tidigare ska du lägga till den nya informationen om gruppen 
till den existerande gruppen samt lägga till de medlemmar som inte är med i gruppen sedan tidigare. Om gruppen är ny ska du skapa en ny grupp med den nya informationen."""


class Personhandler:
    def __init__(self):
        self.people_collection = MongoClient(os.environ.get("MONGO_DB_URI"))["collected_info"]["people"]
        self.relations_collection = MongoClient(os.environ.get("MONGO_DB_URI"))["collected_info"]["relations"]
        self.groups_collection = MongoClient(os.environ.get("MONGO_DB_URI"))["collected_info"]["groups"]
        self.people_store = MongoDBAtlasVectorSearch(embedding=embedder, collection=self.people_collection, index_name="vector_cosine_index")
        self.groups_store = MongoDBAtlasVectorSearch(embedding=embedder, collection=self.groups_collection, index_name="vector_cosine_index")
        config=GenerationConfig(
                temperature=0.0,
                candidate_count=1,
            ),
        self.info_model = GenerativeModel("gemini-1.0-pro", system_instruction=[info_instructions], safety_settings=gemini_unfiltered, generation_config=config)
        self.groq = Groq(api_key=os.environ.get("GROQ_API_KEY")).chat.completions
        self.description_model = GenerativeModel("gemini-1.0-pro", system_instruction=[summarize_description_instructions], safety_settings=gemini_unfiltered, generation_config=config)

    def ny_info_person(self,alias, new_info):
        person = self._get_current_info(alias)
        name = person["name"]
        info = person["info"]
        description = person["text"]
        info = self._update_info(info, new_info)
        self._update_description(description, new_info, name, info)
        

    def _get_current_info(self, name) -> Document:
        person = self.people_collection.find_one({"name": name})
        if person:
            return person
        else:
            nearest = self.people_store.similarity_search(name,k=3)
            corrected_name = self._check_if_new_person(name, nearest)
            return self.people_collection.find_one({"name": corrected_name})
        
    def _update_info(self, old_info, new_info):
        chat = self.info_model.start_chat()
        message = "**Tidigare känd information**\n "+old_info+"\n\n **ny information att inkludera**\n "+new_info
        print("Old info: \n"+old_info)
        response = chat.send_message(message).candidates[0].content.text
        print("Updated info: \n"+response)
        try:
            self.people_collection.update_one({"info": old_info}, {"$set": {"info": response}})
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
    #             deletion = self.people_collection.delete_one({"text": current_description})
    #             self.people_store.add_documents([new_person])
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


    def _generate_description(self, info):
        self.description_model.generate_content(info)



        response = self.info_model.generate_content(info)
        try:
            args = extract_args(response.choices[0].message.tool_calls[0])
            description = args["ny_beskrivning"]
            print_tool_call(response.choices[0].message.tool_calls[0])
            metadata = {"name": name, "info": info}
            new_person = Document(page_content=description, metadata=metadata)
            try:
                deletion = self.people_collection.delete_one({"text": current_description})
                self.people_store.add_documents([new_person])
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


    def _check_if_new_person(self, name, nearest : List[Document]):
        prompt = "Sökning: "+name+"\nAlternativ: "
        for i, option in enumerate(nearest):
            prompt += str(i+1)+". Namn: "+option.metadata["name"]+"Beskrivning: "+option.page_content+"\n"
        response = self.groq.create(
            messages=[
                {
                    "role": "system",
                    "content": tell_if_new_person_instructions,
                },
                {
                    "role": "user",
                    "content": prompt,
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
                self.people_store.add_documents([new_person])
            else:
                print("User was identied as "+args["namn"])
            return args["namn"]
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print("Did not classify person")


    def ny_information_om_relation(self, name1, name2, relation):
        person1 = self._check_if_new_person(name1)
        person2 = self._check_if_new_person(name2)

        filter = {"person1": person1, "person2": person2}
        update = {"$concat": {"info": relation}}

        self.relations_collection.update_one(filter, update)


    def ny_information_om_gruppering(self, name  : str, members : List[str], info : str):
        group_string = "**Gruppnamn: "+name+"**\nMedlemmar:\n"
        for person in members:
            group_string += person+"\n"
        group_string += "Information om gruppen:"+info
        self._check_if_new_group(group_string, info)
        

    def _check_if_new_group(self, group_string, info):
        options = self.groups_store.similarity_search(group_string, k=3)
        prompt = "Sökning: "+group_string+"\nAlternativ: "
        for i, option in enumerate(options):
            prompt += str(i+1)+". Grupp: "+option.metadata["name"]+"Medlemmar: "+option.page_content+"\n"
        response = self.groq.create(
            messages=[
                {
                    "role": "system",
                    "content": tell_if_new_group_instructions,
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            tools=[tools["lägg_till_info_om_existerande_gruppering"], tools["skapa_gruppering"]],
            model="mixtral-8x7b-32768",
        )
        try:
            name = response.choices[0].message.tool_calls[0].function.name
            if name == "skapa_gruppering":
                print_tool_call(response.choices[0].message.tool_calls[0])
                args = extract_args(response.choices[0].message.tool_calls[0])
                name = args["namn"]
                members = args["members"]
                metadata = {"name": name, "members" : members, "info": info}
                new_group = Document(page_content=args["beskrivning_av_ny_gruppering"], metadata=metadata)
                self.groups_store.add_documents([new_group])
                return name, members
            elif name == "lägg_till_info_om_existerande_gruppering":
                print_tool_call(response.choices[0].message.tool_calls[0])
                args = extract_args(response.choices[0].message.tool_calls[0])
                name = args["namn"]
                members = args["members"]
                if len(members) > 0:
                    self.groups_collection.update_one({"name": name}, {"$push": {"members": members}})
                self.groups_collection.update_one({"name": name}, {"$concat": {"info": info}})
            else:
                print("Group was identied as "+args["namn"])
            return args["namn"]
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print("Did not classify group")
