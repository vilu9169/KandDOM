from langchain_pinecone import PineconeVectorStore
from embedding import get_image_embeddings

index_name = "image-bank"


def similarity_search(file_path):
    image_embeddings = get_image_embeddings("robust-summit-417910", "europe-west4", file_path)
    pinecone = PineconeVectorStore(index_name)
    return pinecone.similarity_search(image_embeddings.image_embedding)


