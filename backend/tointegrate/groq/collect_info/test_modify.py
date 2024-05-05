from modify_people import Personhandler
from langchain_google_vertexai import VertexAIEmbeddings
from util import print_FAISS

embedder = VertexAIEmbeddings("textembedding-gecko-multilingual")


handler = Personhandler(embedder)




handler.ny_information_om_relation("eric Walström", "Anna", "Eric och Anna är gifta med varandra")

handler.ny_info_person("eric Walström", "eric är en hårt arbetande person som är väldigt smart. Han har tre barn och är gift med Anna") 
handler.ny_info_person("Anna", "Anna är gift med Eric och har tre barn")




handler.ny_info_person("Johan", "Johan är en god vän till Eric")
handler.ny_info_person("Eric W", "eric är gift med Anna, han har en kompis som heter Johan")



print("\nprinting faiss store:")
print_FAISS(handler.people_store)

print("\nprinting relations:")
for relation in handler.relations_struct.values():
    print()
    print(relation.person1)
    print(relation.person2)
    print("info:")
    print(relation.info)