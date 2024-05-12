from concurrent.futures import thread
from webbrowser import get
from pinecone import Pinecone, ServerlessSpec
import PyPDF2
import os
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.schema.document import Document
from pinecone import Pinecone, ServerlessSpec
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import CharacterTextSplitter
from timelinemaker import analyzefromstr
from time import sleep
from pdf2image import convert_from_bytes, convert_from_path
from vertexai.generative_models import GenerativeModel, Part, FinishReason, Image

from google.cloud import documentai
import io
import threading

def async_handle_chunk(chunk_num, chunk_size, num_pages, pdf_file, client, name, resstrings):
    while True:
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            break
        except Exception as e:
            print(e)
            sleep(5)
    pagenr = chunk_num * chunk_size
    start_page = chunk_num * chunk_size
    end_page = min((chunk_num + 1) * chunk_size, num_pages)
    print("Working with pages ", start_page, " to ", end_page)
    writer = PyPDF2.PdfWriter()
    for page_num in range(start_page, end_page):
        writer.add_page(reader.pages[page_num])
    response_bytes_stream = io.BytesIO()
    writer.write(response_bytes_stream)
    #Seek 0 to start reading
    response_bytes_stream.seek(0)
    # Read the file into memory
    with response_bytes_stream as image:
        image_content = image.read()
    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request, )
    #print("Result looks like ", result)

    # For a full list of Document object attributes,
    # please reference this page: https://googleapis.dev/python/documentai/latest/gapic/v1beta3/types.html#google.cloud.documentai.v1beta3.Document
    document = result.document
    # Read the text recognition output from the processor
    resstring = ""
    for page in document.pages:
        resstring += "{pagestart page "+ str(pagenr+1) + " in document "+pdf_file +" }"
        temp = ""
        for block in page.blocks:
            split = str(block.layout.text_anchor.text_segments).split("\n")
            if(len(split) > 2):
                temp += document.text[int(split[0][split[0].find(":") +2:]) : int(split[1][split[1].find(":") +2:])]
            else:
                temp += document.text[0: int(split[0][split[0].find(":") +2:])]
            #Check if temp is a candidate for being an image                
        resstring += temp
        #resstring += page.layout.text_anchor.content
        resstring +="{pageend page "+ str(pagenr+1)+ " in document "+pdf_file +"}"+str(chr(28))
        pagenr += 1
    resstrings[chunk_num] = resstring
    pass

def getraw(chunk_num, chunk_size, num_pages, pdf_file, num_chunks):
    reader = PyPDF2.PdfReader(pdf_file)
    start_page = chunk_num * chunk_size
    end_page = min((chunk_num + 1) * chunk_size, num_pages)
    docs = []
    writer = PyPDF2.PdfWriter()
    for page_num in range(start_page, end_page):
        writer.add_page(reader.pages[page_num])
    response_bytes_stream = io.BytesIO()
    writer.write(response_bytes_stream)
    #Seek 0 to start reading
    response_bytes_stream.seek(0)
    # Read the file into memory
    with response_bytes_stream as image:
        image_content = image.read()
    # Load Binary Data into Document AI RawDocument Object
    return image_content

def swifthandle(pdf_file, chunk, resind, client, name, resstrings, chunksize, images):
    raw_document = documentai.RawDocument(content=chunk, mime_type="application/pdf")
    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request, )
    # For a full list of Document object attributes,
    # please reference this page: https://googleapis.dev/python/documentai/latest/gapic/v1beta3/types.html#google.cloud.documentai.v1beta3.Document
    document = result.document
    # Read the text recognition output from the processor
    pagenr = chunksize*resind
    resstring = ""
    for page in document.pages:
        resstring += "{pagestart page "+ str(pagenr+1) + " in document "+pdf_file +" }"
        temp = ""
        for block in page.blocks:
            split = str(block.layout.text_anchor.text_segments).split("\n")
            if(len(split) > 2):
                temp += document.text[int(split[0][split[0].find(":") +2:]) : int(split[1][split[1].find(":") +2:])]
            else:
                temp += document.text[0: int(split[0][split[0].find(":") +2:])]                
        #Check if temp is a candidate for being an image
        if(piccand(temp)):
            model_name = "gemini-1.5-pro-preview-0409"
            generative_multimodal_model = GenerativeModel(model_name)
            instructions_text = """Dethär är en bild på en sida ur ett juridiskt dokument. Du ska återge innehållet på sidan. 
            Inehåller sidan text skall du bara återge texten. Innehåller sidan en tabell skall du återge tabellen som text. 
            Inehåller sidan en bild skall du beskriva bilden och vad den visar som text. Inehåller sidan en kombination av bilder, text och tabeller skall du återge allt.
            Svara bara med inehåll och beskrivningar av materialet. """
            img_byte_arr = io.BytesIO()
            images[pagenr].save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            response = generative_multimodal_model.generate_content([instructions_text, Image.from_bytes(img_byte_arr)])
            temp = response.candidates[0].text
            print("Image found")
            print("Image text: ", temp)
        resstring += temp
        
        #resstring += page.layout.text_anchor.content
        resstring +="{pageend page "+ str(pagenr+1)+ " in document "+pdf_file +"}"+str(chr(28))
        pagenr += 1
    resstrings[resind] = resstring
    pass

def piccand(page):
     return( ((len(page) < 150)  or  ("Skiss" in page) or("DNA Arbetsblad" in page) or  ("Foto" in page) or ("Kart" in page) or ("Figur" in page) or "Bild" in page))
def tablecand(page):
    return(("Tabell" in page or page.count("\n") > 0.04*len(page)) and not(piccand(page)))

#Same as before but no threads with pdf reader
def ocr_pdf(pdf_file, project_id, location, processor_id, images):
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = {"api_endpoint": "eu-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    name = client.processor_path(project_id, location, processor_id)
    # Split the document into chunks of 15 pages
    chunk_size = 15
    reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(reader.pages)
    if(num_pages%chunk_size == 0):
        num_chunks = num_pages//chunk_size
    else:
        num_chunks = num_pages//chunk_size + 1
        
    threads = []
    rawdata = []
    # Get the raw data
    #getraw 
    for chunkid in range(num_chunks):
        rawdata.append(getraw(chunkid, chunk_size, num_pages, pdf_file, num_chunks))
    resstrings = []
    for i in range(num_chunks):
        resstrings.append("")
        t = threading.Thread(target=swifthandle, args=(pdf_file, rawdata[i], i,  client, name, resstrings, chunk_size, images))
        threads.append(t)
        t.start()
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    resstring = ""
    for res in resstrings:
        resstring += res
    return resstring

#Takes a path to a pdf file and extracts contents for being used in the RAG
# def ocr_pdf_old(pdf_file, project_id, location, processor_id):
#     # You must set the api_endpoint if you use a location other than 'us'.
#     opts = {"api_endpoint": "eu-documentai.googleapis.com"}
#     client = documentai.DocumentProcessorServiceClient(client_options=opts)
#     name = client.processor_path(project_id, location, processor_id)
#     # Split the document into chunks of 15 pages
#     chunk_size = 15
#     reader = PyPDF2.PdfReader(pdf_file)
#     num_pages = len(reader.pages)
#     if(num_pages%chunk_size == 0):
#         num_chunks = num_pages//chunk_size
#     else:
#         num_chunks = num_pages//chunk_size + 1
#     #resstring = ""
#     resstrings = []
#     #Add a new string for each chunk
#     for i in range(num_chunks):
#         resstrings.append("")
        
#     threads = []
#     # Create and start threads
#     for i in range(num_chunks):
#         t = threading.Thread(target=async_handle_chunk, args=(i, chunk_size, num_pages, pdf_file, client, name, resstrings))
#         threads.append(t)
#         t.start()

#     # Wait for all threads to finish
#     for thread in threads:
#         thread.join()

    
#     resstring = ""
#     for res in resstrings:
#         resstring += res
#     return resstring

# def extract_text_from_pdf(pdf_file) -> str:
#     try:
#         with open(pdf_file, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             num_pages = len(reader.pages)
#             text = ""
#             #Separate pages so they start with { and end with }
#             for page_num in range(num_pages):
#                 text += "{pagestart page "+ str(page_num+1) + " in document "+pdf_file +" }"
#                 page = reader.pages[page_num]
#                 text += page.extract_text()
#                 text +="{pageend page "+ str(page_num+1)+ " in document "+pdf_file +"}"+str(chr(28))

#             return text
#     except FileNotFoundError:
#         print(f"Error: File '{pdf_file}' not found.")
#         return None
    
def text_to_rag(new_index_name, text):
    os.environ["PINECONE_API_KEY"] = "2e669c83-1a4f-4f19-a06a-42aaf6ea7e06"
    os.environ["PINECONE_ENV"] = "default"
    pc = Pinecone(api_key="2e669c83-1a4f-4f19-a06a-42aaf6ea7e06")
    #Try to create the index, if it already exists do nothing
    try:
        pc.create_index(
            name=new_index_name,
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws', 
                region='eu-west-1'
            ) 
        ) 
    except Exception as e:
        print("Index already exists")
    # Split documents
    text_splitter = CharacterTextSplitter(chunk_size=2, chunk_overlap =0,separator=str(chr(28)))
    splits = [Document(page_content=x) for x in text_splitter.split_text(text)]
    #splits = text_splitter.split_text(text)    
    embeddings = VertexAIEmbeddings(model_name="textembedding-gecko-multilingual@001")
    # initialize pinecone
    vectorstore = PineconeVectorStore(new_index_name, embeddings.embed_query, splits)
    # Vertex AI embedding model  uses 768 dimensions`
    vectorstore = vectorstore.from_documents(splits, embeddings, index_name=new_index_name)


#Sorts time events leaving those without a time at the beginning
def bettersort(theevents):
    if(type(theevents["title"]) == str):
        return 0
    else:
        return theevents["title"].timestamp()

def getimages(pdf_file):
    #Get the images from the pdf
    images = convert_from_path(pdf_file, fmt = "png")
    #Print the type of the images
    print(type(images))
    for image in images:
        print(type(image))
    return images

def handle_multi_pdfs(pdf_files, new_index_name):
    retarr = []
    #Handle all the pdf files
    for pdf_file in pdf_files:
        print("Processing ", pdf_file, "...")
        images = getimages(pdf_file)
        # Store Pdf with convert_from_path function
        print("Doing OCR...")
        text = ocr_pdf(pdf_file, "sunlit-inn-417922", "eu", "54cf154d8c525451", images)
        print("RAGING...")
        text_to_rag(new_index_name, text)
        #Find all candidates 

        #After text to rag run timelinemaker
        print("Analyzing...")
        retarr += analyzefromstr(text, pdf_file)
    retarr = sorted(retarr, key = lambda x: bettersort(x))
    
    for elem in retarr:
        try:
            elem["title"] = str(elem["title"].strftime("%d/%m/%Y %H:%M"))
        except Exception as e:
            print("Error parsing time: ", e)
    print(retarr)


pdf_files = []
while True:
    print("Name of the files to be processed using RAG(write \"end\" to end input): ")
    pdf_file = input()
    if(pdf_file == "end"):
        break
    else:
        pdf_files.append(pdf_file)
print("Name of the new index: ")
new_index_name = input()
handle_multi_pdfs(pdf_files, new_index_name)