from process_text import process_text
from modify_people import Personhandler
from langchain_google_vertexai import VertexAIEmbeddings
from util import print_FAISS
from people import use_tools_on_summary

text : str

file_path = "KandDOM/fuppar_txt/schizzomord.txt"

with open(file_path, "r") as file:
    text = file.read()

pages = text.split(chr(28))


to_process = pages[0]


embedder = VertexAIEmbeddings("textembedding-gecko-multilingual")

person_handler = Personhandler(embedder, "REPLACE")


summary = """
##Grupper
Bandidos
Bandidos är en kriminell organisation med 7000 medlemmar i Sverige, däribland Björn och Rikard.
"""

#use_tools_on_summary(summary)

people, relations, groups = process_text(to_process, person_handler)

# person_handler.move_to_db()


# print_FAISS(people)

# print_FAISS(groups)

# for relation in relations.values():
#     print()
#     print(relation.person1)
#     print(relation.person2)
#     print("info:")
#     print(relation.info)
