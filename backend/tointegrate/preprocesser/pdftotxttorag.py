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
import time

def ocr_pdf(pdf_file, project_id, location, processor_id):
    
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = {"api_endpoint": "eu-documentai.googleapis.com"}

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor, e.g.:
    # projects/project_id/locations/location/processor/processor_id
    # You must create new processors in the Cloud Console first
    name = client.processor_path(project_id, location, processor_id)
    # Create a working directory
    working_dir = "./working_directory"
    os.makedirs(working_dir, exist_ok=True)

    # Split the document into chunks of 20 pages
    chunk_size = 15
    reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(reader.pages)
    num_chunks = num_pages//chunk_size + 1
    resstring = ""
    pagenr = 0
    for chunk_num in range(num_chunks):
        start_page = chunk_num * chunk_size
        end_page = min((chunk_num + 1) * chunk_size, num_pages)
        #Previously created new file for each chunk
        chunk_file = os.path.join(working_dir, f"writteto.pdf")
        #Calculate time it takes to generate the chunk
        starttime = time.time()
        # Extract the pages and save them as a new PDF file
        writer = PyPDF2.PdfWriter()
        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])
            
        with open(chunk_file, "wb") as f:
            writer.write(f)
        
        # Read the file into memory
        with io.open(chunk_file, "rb") as image:
            image_content = image.read()
        print("Time to generate chunk: ", time.time()-starttime)
        # Load Binary Data into Document AI RawDocument Object
        raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")

        # Configure the process request
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)
        print("Sending request to the processor service")
        result = client.process_document(request=request, )
        #print("Result looks like ", result)

        # For a full list of Document object attributes,
        # please reference this page: https://googleapis.dev/python/documentai/latest/gapic/v1beta3/types.html#google.cloud.documentai.v1beta3.Document
        document = result.document
        # Read the text recognition output from the processor
        for page in document.pages:
            resstring += "{pagestart nr "+ str(pagenr+1) +"}"
            for block in page.blocks:
                # Block content: [start_index: 15448
                # end_index: 15463
                # ]
                print(f"Block content: {block.layout.text_anchor.text_segments}")
                split = str(block.layout.text_anchor.text_segments).split("\n")
                print("splitlen", len(split))
                if(len(split) > 2):
                    resstring += document.text[int(split[0][split[0].find(":") +2:]) : int(split[1][split[1].find(":") +2:])]
                # if not("start_index" in str(block.layout.text_anchor.text_segments)):
                #     #Extract end_index using string slicing
                    
                #     resstring += document.text[: str(block.layout.text_anchor.text_segments)]
                # else:
                #     
                
            #resstring += page.layout.text_anchor.content
            resstring +="{pageend nr "+ str(pagenr+1) +"}"
            pagenr += 1
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
mainfunk("../output.pdf", "googlesown2")