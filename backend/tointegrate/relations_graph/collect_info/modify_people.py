from pymongo import MongoClient
from dotenv import load_dotenv
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_mongodb import MongoDBAtlasVectorSearch
from vertexai.generative_models import GenerativeModel, GenerationConfig
import vertexai.preview.generative_models as generative_models
from groq import Groq
from collection_tools import tools
import traceback
from typing import List
from langchain_core.vectorstores import VectorStore
from anthropic import AnthropicVertex
from openai import OpenAI
from openai.types.chat import ChatCompletion

from util import print_tool_call, extract_args, gemini_unfiltered

from langchain_community.vectorstores import FAISS, DistanceStrategy
from get_predictions import get_openai_prediction, get_groq_prediction, get_claude_prediction_string

import threading
import time

load_dotenv()

dbclient = MongoClient(os.environ.get("MONGO_DB_URI"))

db = dbclient["collected_info"]
collection = db["people"]

info_instructions = """Du är en assistent som hanterar ett arkiv som sparar information om personer
Du har fått ny information om en person samt den tidigare kända informationen.
Din uppgift är att uppdatera den tidigare kända informationen med den nya informationen utan att
Tappa någon tidigare information. Om den nya informationen är redan finns i den tidigare kända informationen
behöver du inte förändra något. Lägg aldrig till något som inte står bland den nya informationen.

Viktigt: Svara bara med den nya versionen av informationen, skriv INTE att du har uppdaterat informationen eller andra kommentarer, det förstör i arkivet!
"""

# depricated, not used
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
Använd endast information som står i texten, din sammanfattning om personen bör vara strikt kortare än texten du sammanfattar.
"""





tell_if_new_person_instructions = """Du är en assistent som hjälper användare söka efter personer i ett arkiv.
Användaren har skickat in ett namn som inte var en exakt match bland tidigare namn. Din uppgift är att
avgöra om det nya namnet är en ny person som ska läggas till i arkivet eller om det är en person som redan
finns i arkivet. Du får upp till tre alternativ bland tidigare kända personer att välja mellan. Du ska sedan använda ett verktyg för att
förmedla till användaren om personen är ny eller inte. Tänk på att personen kan ha olika stavningar på sitt namn.
"""


tell_if_new_group_instructions = """
Du är en assistent som hjälper användare söka efter grupper i ett arkiv. Användaren har skickat in en beskrivning av en grupp som inte var en exakt match bland tidigare grupper. 
Din uppgift är att avgöra om den nya gruppen är en ny grupp som ska läggas till i arkivet eller om det är en grupp som redan finns i arkivet. 
Du får upp till tre alternativ bland tidigare kända grupper att välja mellan. Om gruppen finns i arkivet sedan tidigare ska du lägga till den nya informationen om gruppen 
till den existerande gruppen samt lägga till de medlemmar som inte är med i gruppen sedan tidigare. Om gruppen är ny ska du skapa en ny grupp med den nya informationen."""


def init_FAISS(embedder):
    db = FAISS.from_texts(["init"], embedder, distance_strategy=DistanceStrategy.COSINE, ids=["init"])
    db.delete(["init"])
    return db


class Relation:
    def __init__(self, person1, person2, info):
        self.person1 = person1
        self.person2 = person2
        self.info = info





class Personhandler:
    def __init__(self, embedder, rag_vector_store : VectorStore):
        self.embedder = embedder
        self.rag_store = rag_vector_store
        self.people_collection = MongoClient(os.environ.get("MONGO_DB_URI"))["collected_info"]["people"]
        self.relations_collection = MongoClient(os.environ.get("MONGO_DB_URI"))["collected_info"]["relations"]
        self.groups_collection = MongoClient(os.environ.get("MONGO_DB_URI"))["collected_info"]["groups"]
        self.people_store = init_FAISS(self.embedder)#MongoDBAtlasVectorSearch(embedding=embedder, collection=self.people_collection, index_name="vector_cosine_index")
        self.people_dict : dict[str, Document] = {}
        self.groups_store = init_FAISS(self.embedder)#MongoDBAtlasVectorSearch(embedding=embedder, collection=self.groups_collection, index_name="vector_cosine_index")
        self.groups_dict : dict[str, Document] = {}
        self.relations_struct : dict[str, Relation] = {}
        config=GenerationConfig(temperature=0.0, candidate_count=1)
        self.info_model = GenerativeModel("gemini-1.0-pro", system_instruction=[info_instructions], safety_settings=gemini_unfiltered, generation_config=config)
        self.groq = Groq(api_key=os.environ.get("GROQ_API_KEY")).chat.completions
        self.description_model = GenerativeModel("gemini-1.0-pro", system_instruction=[create_description_instructions], safety_settings=gemini_unfiltered, generation_config=config)
        self.anthropic = AnthropicVertex(region="europe-west4", project_id="robust-summit-417910")
        self.creatingPerson = ""
        self.creatingGroup = ""

    def ny_info_person(self, alias, new_info):
        person = self._get_current_info(alias, new_info)
        name = person.metadata["name"]
        info = person.metadata["info"]
        description = person.page_content
        info += "\n "+new_info #self._update_info(new_info)
        metadata = {"name": name, "info": info}
        updated_person = Document(page_content=description, metadata=metadata)
        self._generate_update_description(updated_person)
        

    def _get_current_info(self, name, new_info) -> Document:
        search_result = self.people_store.similarity_search(name,k=3)
        if search_result and search_result[0].metadata["name"] == name:
            return search_result[0]
        else:
            corrected_name = self._check_if_new_person(name, new_info, search_result)
            return self.people_dict[corrected_name]
    
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

    def _generate_update_description(self, person : Document):
        info = person.metadata["info"]
        name = person.metadata["name"]
        prompt = "Namn: "+name+" \nInformation: "+info
        new_description = self.description_model.generate_content(prompt).candidates[0].content.text
        metadata = {"name": name, "info": info}
        new_person = Document(page_content=new_description, metadata=metadata)
        deletion = self.people_store.delete([name])
        if not deletion:
            print("ERROR: no deletion during update")
        self.people_store.add_documents([new_person], ids=[name])
        self.people_dict.update({name : new_person})

    def _generate_description(self, person : Document):
        instructions = """
        Du är en assistent som skapar en kort sammanfattning av en person för att identifiera personen. Du får frågor om en personer samt utdrag ur ett förundersökningprotokoll
        som innehåller information om personen. Du ska skapa en kort sammanfattning av personen som fokuserar på personens inblandning i rättsfallet samt relationer 
        till andra personer och grupper. Frågan ställs av en användare som bara har tillgång till en liten del av dokumentet och behöver hjälp att identifiera personen.
        I frågan får du personens "namn" (kan vara ett alias eller annan beskrivning som 'bror till den åtalade') samt information om personen som stod i delen av dokumentet som 
        användaren har tillgång till.

        Svara endast med sammanfattningen, inga övriga kommentarer. Du behöver häller inte förklara att informationen kommer från ett förundersökningsprotokoll, det är underförstått.
        """
        prompt = "Vem är "+person.metadata["name"]+"? Här är lite information om personen"+person.metadata["info"]
        description = self.prompt_with_rag(prompt, instructions)
        metadata = {"name": person.metadata["name"], "info": person.metadata["info"]}
        new_person = Document(page_content=description, metadata=metadata)
        self.people_store.add_documents([new_person], ids=[person.metadata["name"]])

    def prompt_with_rag(self, prompt, instructions):
        context = instructions
        index = 0
        prepend = ""
        append = ""
        for rag in self.rag_store.as_retriever(search_kwargs = ({"k" : 40, })).invoke(prompt):
        #The first 10 documents are prepended to the context
        #The last 10 documents are appended to append
            if index < 10:
                prepend += rag.page_content
            elif index >10 and index < 20:
                append = rag.page_content + append
            else:
                prepend += rag.page_content
            index += 1

        context += prepend + append
        return get_claude_prediction_string(prompt, context)


    tell_if_new_instructions = """
    Du är en assistent som hjälper användare söka efter personer iblandade i ett rättsfall.
    Användaren har skickat in ett namn som inte var en exakt match bland tidigare namn. Din uppgift är att
    avgöra om det nya namnet är en ny person inte registrerats sedan tidigare eller om det är en person som redan
    finns sparad. Du får upp till tre alternativ bland tidigare kända personer att välja mellan. Avgör om personen är samma som ett av de namn som står som alternativ, 
    om personen endast nämns i beskrivningen av andra personen är de mycket sannolikt inte registrerade sedan tidigare. Utgå endast från information som står i texten, inte från egna antaganden.
    
    Resonera kring varför personen är ny eller inte, och välj det alternativ som anses vara mest sannolikt.
    Återge ordagrant det alternativ som anses vara mest sannolikt. Samt skriv uttryckligen "Alternativ 'nummer på alternativ'"
    """
    tell_if_new_person_instructions = """
    Du har fått en analys av personsökning, ditt jobb är att registrera analysen med hjälp av verktyget "identifiera_person". Läs slutsatsen och skriv sedan in den i verktyget.
    """

    def _check_if_new_person(self, name, info, nearest : List[Document]):
        if self.creatingPerson != "":
                print("Waiting for "+self.creatingPerson+" to be created before identifying "+name)
                time.sleep(1)
                self._check_if_new_person(name, info, nearest)
        search = "Namn: "+name+" Information: "+info
        nearest_names = [doc.metadata["name"] for doc in nearest]
        prompt = "Här är personen som ska matchas samt lite information: "+search+"\nHär är de möjliga alternativen för vem personen kan vara: "
        if len(nearest) == 0:
            prompt += "\n1. Inga tidigarer kända personer hittades, personen måste vara ny"
        else:
            for i, option in enumerate(nearest):
                prompt += str(i+1)+". Namn: "+option.metadata["name"]+"\n Information om "+option.metadata["name"]+ ": "+option.page_content+"\n"
            prompt += "Här är alltså de möjliga alternativen för vem "+name+" kan vara, välj det som verkar mest troligt:\n"
            for i, option in enumerate(nearest):
                prompt += str(i+1)+". "+name+" är samma person som "+option.metadata["name"]+" \n"
            prompt += str(len(nearest)+1)+". "+name+" är en annan person än"
            for i, option in zip(range(len(nearest)-1),nearest):
                prompt += " "+option.metadata["name"]+","
            if len(nearest) > 1:
                prompt += "eller "+nearest[-1].metadata["name"]
            else:
                prompt += " "+nearest[0].metadata["name"]
        print(prompt)

        response = get_claude_prediction_string(prompt, self.tell_if_new_person_instructions)
        
        print("Model response: ")
        print(response)

        tools=[tools["identifiera_person"]]
        response = get_openai_prediction(prompt, self.tell_if_new_person_instructions,tools=tools)
        tool_use = response.choices[0].message.tool_calls
        try:
            args = extract_args(tool_use.choices[0].message.tool_calls[0])
            print_tool_call(tool_use.choices[0].message.tool_calls[0])
            if args["Siffra_på_alternativ"] == len(nearest)+1:
                if self.creatingPerson != "":
                    print("Waiting for "+self.creatingPerson+" to be created before identifying "+name)
                    time.sleep(1)
                    if self._check_if_search_changed(name, nearest):
                        print("Search changed, restarting")
                        return self._check_if_new_person(name, info, nearest)
                self.creatingPerson = name
                print("User was not found before")
                metadata = {"name": name, "info": ""}
                new_person = Document(page_content="init", metadata=metadata)
                self.people_store.add_documents([new_person], ids=[name])
                self.people_dict.update({name : new_person})
                self.creatingPerson = ""
                # self._generate_update_description(new_person)
                return name
            else:
                option = args["Siffra_på_alternativ"]
                corrected_name = nearest_names[option-1]
                print("User was identied as "+corrected_name)
                return corrected_name
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print("Did not classify person")


    def _check_if_search_changed(self, search, old_results : list[Document]):
        new_result = self.people_store.similarity_search(search,k=3)
        new_names = [doc.metadata["name"] for doc in new_result]
        old_names = [doc.metadata["name"] for doc in old_results]
        search_changed = False
        for new_name in new_names:
            if new_name not in old_names:
                same_search = True
                return same_search
        return same_search

    def ny_information_om_relation(self, name1, name2, relation):
        person1 = self.people_dict.get(name1)
        person2 = self.people_dict.get(name2)
        if not person1:
            search_result = self.people_store.similarity_search(name1, k=3)
            person1 = self._check_if_new_person(name1, relation, search_result)
        if not person2:
            search_result = self.people_store.similarity_search(name2, k=3)
            person2 = self._check_if_new_person(name2, relation, search_result)

        in_order1, in_order2 = sorted([name1, name2])
        names_string = in_order1+in_order2
        result = self.relations_struct.get(names_string)
        if result:
            result.info += "\n"+relation
        if not result:
            self.relations_struct.update({names_string : Relation(name1, name2, relation)})


    def ny_information_om_gruppering(self, name  : str, members : List[str], info : str):
        group_string = "**Gruppnamn: "+name+"**\nMedlemmar:\n"
        for person in members:
            group_string += person+"\n"
        group_string += "Information om gruppen:"+info
        self._check_if_new_group(group_string, info)
        

    def _check_if_new_group(self, group_string, info):
        if self.creatingGroup != "":
            print("Waiting for "+self.creatingGroup+" to be created, before identifying "+group_string)
            time.sleep(1)
            self._check_if_new_group(group_string, info)
        options = self.groups_store.similarity_search(group_string, k=3)
        prompt = "Sökning: "+group_string+"\nAlternativ: "
        for i, option in enumerate(options):
            prompt += str(i+1)+". Grupp: "+option.metadata["name"]+"Medlemmar: "+option.page_content+"\n"

        tool_list = [tools["lägg_till_info_om_existerande_gruppering"], tools["skapa_gruppering"]]
        model = "gpt-4o-2024-05-13"
        system = tell_if_new_group_instructions
        prompt = prompt
        response = get_openai_prediction(prompt, tool_list, model, system)
        try:
            name = response.choices[0].message.tool_calls[0].function.name
            if name == "skapa_gruppering":
                self.creatingGroup = name
                print_tool_call(response.choices[0].message.tool_calls[0])
                args = extract_args(response.choices[0].message.tool_calls[0])
                name = args["namn"]
                members = args["members"]
                metadata = {"name": name, "members" : members, "info": info}
                new_group = Document(page_content=args["beskrivning_av_ny_gruppering"], metadata=metadata)
                self.groups_store.add_documents([new_group], ids=[name])
                self.groups_dict.update({name : new_group})
                self.creatingGroup = ""
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

    def move_to_db(self):
        people = self.people_store.similarity_search(".", k=self.people_store.index.ntotal)
        relations = self.relations_struct.values()
        groups = self.groups_store.similarity_search(".", k=self.groups_store.index.ntotal)
        people_db_store = MongoDBAtlasVectorSearch(embedding=self.embedder, collection=self.people_collection, index_name="vector_cosine_index")
        groups_db_store = MongoDBAtlasVectorSearch(embedding=self.embedder, collection=self.groups_collection, index_name="vector_cosine_index")
    
        people_db_store.add_documents([people])
        groups_db_store.add_documents([groups])
        relations_to_insert = []
        for relation in relations:
            self.description_model.generate_content(relation.info)
            relations_to_insert.append({"person1": relation.person1, "person2": relation.person2, "info": relation.info})
        self.relations_collection.insert_many(relations_to_insert)