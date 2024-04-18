from pinecone import Pinecone, ServerlessSpec
import PyPDF2
# pdf_file = "gbg_mordforsok.pdf"
# output_file = "output.pdf"
import os
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.schema.document import Document
from pinecone import Pinecone, ServerlessSpec
from langchain.text_splitter import RecursiveCharacterTextSplitter
from google.cloud import documentai
import io

def ocr_pdf(pdf_file, project_id, location, processor_id):
    
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = {"api_endpoint": "eu-documentai.googleapis.com"}

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor, e.g.:
    # projects/project_id/locations/location/processor/processor_id
    # You must create new processors in the Cloud Console first
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with io.open(pdf_file, "rb") as image:
        image_content = image.read()

    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    print("Sending request to the processor service")
    result = client.process_document(request=request, )

    # For a full list of Document object attributes,
    # please reference this page: https://googleapis.dev/python/documentai/latest/gapic/v1beta3/types.html#google.cloud.documentai.v1beta3.Document
    document = result.document

    # Read the text recognition output from the processor
    resstring = ""
    for paragraph in document.text:
        resstring += paragraph
    print("Resstring",resstring)
    return resstring

def extract_text_from_pdf(pdf_file) -> str:
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            text = ""
            #Separate pages so they start with { and end with }
            for page_num in range(num_pages):
                text += "{pagestart nr "+ str(page_num+1) +"}"
                page = reader.pages[page_num]
                text += page.extract_text()
                text +="{pageend nr "+ str(page_num+1) +"}"

            return text
    except FileNotFoundError:
        print(f"Error: File '{pdf_file}' not found.")
        return None
    
def text_to_rag(new_index_name, text):
    os.environ["PINECONE_API_KEY"] = "2e669c83-1a4f-4f19-a06a-42aaf6ea7e06"
    os.environ["PINECONE_ENV"] = "default"
    pc = Pinecone(api_key="2e669c83-1a4f-4f19-a06a-42aaf6ea7e06")
    pc.create_index(
        name=new_index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-west-2'
        ) 
    ) 
    # Split documents
    #text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    #splits = [Document(page_content=x) for x in text_splitter.split_text(text)]
    text_splitter = RecursiveCharacterTextSplitter(separators=["{pagestart", "{pageend"], chunk_overlap = 150)
    splits = [Document(page_content=x) for x in text_splitter.split_text(text)]
    #splits = text_splitter.split_text(text)    
    embeddings = VertexAIEmbeddings(model_name="textembedding-gecko-multilingual@001")
    # initialize pinecone
    vectorstore = PineconeVectorStore(new_index_name, embeddings.embed_query, splits)
    # Vertex AI embedding model  uses 768 dimensions`
    vectorstore = vectorstore.from_documents(splits, embeddings, index_name=new_index_name)
    
def mainfunk(pdf_file, new_index_name):
    #text = extract_text_from_pdf(pdf_file)
    text = ocr_pdf(pdf_file, "sunlit-inn-417922", "eu", "54cf154d8c525451")
    text_to_rag(new_index_name, text)

print("Name of the file to be converted to RAG: ")
pdf_file = input()
print("Name of the new index: ")
new_index_name = input()
mainfunk(pdf_file, new_index_name)