from langchain_community.vectorstores import FAISS, DistanceStrategy
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter

text = "hej, jag är glad"

text1 = "Jag är arg"

text2 = "Jag är förbannad"

text3 = "I was in Paris"

text4 = "dsadsaiofsadsa"

text5 = "I am happy"

print(text)


texts = [text, text1, text3, text4, text5]

print(texts)

embedder = VertexAIEmbeddings("textembedding-gecko-multilingual")

db = FAISS.from_texts(["init"], embedder, distance_strategy=DistanceStrategy.COSINE, ids=["init"])




db.index_to_docstore_id


metadata = {"name" : "eric", "info": "eric är dum"}

doc = Document(page_content="hehehe", metadata=metadata)
db.add_documents()

db.delete

result  = db.delete(["init"])


print("FAISSING")
db.add_texts(texts)

print(db.distance_strategy)
print(db.index.ntotal)
print("FAISS DONE")

results = db.similarity_search_with_score(text2,10)



for result in results:
    doc , score = result
    print(doc.page_content)
    print("Score:", score)