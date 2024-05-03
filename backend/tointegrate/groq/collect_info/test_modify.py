from modify_people import Personhandler
from langchain_google_vertexai import VertexAIEmbeddings
from util import print_FAISS

embedder = VertexAIEmbeddings("textembedding-gecko-multilingual")


handler = Personhandler(embedder)



handler.ny_info_person("eric", "eric är dum")
handler.ny_info_person("eric", "eric är smart")

print_FAISS(handler.people_store)