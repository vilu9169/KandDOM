from process_text import process_text
from modify_people import Personhandler
from langchain_google_vertexai import VertexAIEmbeddings
from util import print_FAISS


text : str

file_path = "KandDOM/fuppar_txt/schizzomord.txt"

with open(file_path, "r") as file:
    text = file.read()

pages = text.split(chr(28))


to_process = pages[0]

embedder = VertexAIEmbeddings("textembedding-gecko-multilingual")

person_handler = Personhandler(embedder)

people, relations, groups = process_text(to_process, person_handler)


print_FAISS(people)

print_FAISS(groups)

for relation in relations.values():
    print()
    print(relation.person1)
    print(relation.person2)
    print("info:")
    print(relation.info)
