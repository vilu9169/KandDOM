from pinecone import Pinecone, ServerlessSpec
import PyPDF2
import os
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.schema.document import Document
from pinecone import Pinecone, ServerlessSpec
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import CharacterTextSplitter

from google.cloud import documentai
import io
import threading

linebreaks = []
numchars = []
def pagestats(pageinfo):
    #Count the number of linebreaks
    linebreaks.append(pageinfo.count("\n"))
    #Count the number of characters
    numchars.append(len(pageinfo))
    
def pageconclusion(pages,linebreaks, numchars):
    #Calculate average number of linebreaks
    avglinebreaks = sum(linebreaks)/len(linebreaks)
    #Calculate average number of characters
    avgchars = sum(numchars)/len(numchars)
    print("Average number of linebreaks: ", avglinebreaks)
    print("Average number of characters: ", avgchars)
    #Find standard deviations for each
    stdlinebreaks = 0
    stdchars = 0
    for i in range(len(linebreaks)):
        stdlinebreaks += (linebreaks[i] - avglinebreaks)**2
        stdchars += (numchars[i] - avgchars)**2
    stdlinebreaks = (stdlinebreaks/len(linebreaks))**0.5
    stdchars = (stdchars/len(numchars))**0.5    
    pics = []
    #Find all pages with 1.5 standard deviations below the average number of characters
    numpiccands = 0
    for i in range(len(pages)):
        #if((numchars[i] < 300 and not("Bildbilaga" in pages[i])) or ("Figur" in pages[i]) or ("Tabell" in pages[i]) or ("Bild" in pages[i])):
        if( ((numchars[i] < 150)  or  ("Skiss" in pages[i]) or("DNA Arbetsblad" in pages[i]) or  ("Foto" in pages[i]) or ("Kart" in pages[i]) or ("Figur" in pages[i]) or "Bild" in pages[i])):
            numpiccands += 1
            print("Page ", i+1, " is a picture candidate.")
            pics.append(i)
    print("Number of picture candidates: ", numpiccands)
    numtabellcands = 0
    for i in range(len(linebreaks)):
        if(("Tabell" in pages[i] or linebreaks[i]> 0.035*numchars[i]) and not(i in pics)):
            print("Page ", i+1, " is a table.")
            numtabellcands += 1
    print("Number of table candidates: ", numtabellcands)


def ocr_pdf(text):
    #Read all text from the txt file
    # text = ""
    # with open(file, 'r') as txt_file:
    #     text = txt_file.read()
    #Merge the strings into one array
    mergedarr = text.split(chr(28))
    for i in range(len(mergedarr)):
        pagestats(mergedarr[i])
    pageconclusion(mergedarr, linebreaks, numchars)

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
                text +="{pageend nr "+ str(page_num+1) +"}"+str(chr(28))

            return text
    except FileNotFoundError:
        print(f"Error: File '{pdf_file}' not found.")
        return None
        
def mainfunk(file): #, new_index_name):
    text = ""
    with open(file, 'r') as txt_file:
        text = txt_file.read()    
    ocr_pdf(text)
    #text_to_rag(new_index_name, text)

print("Textfile: ")
pdf_file = input()
#print("Name of the new index: ")
#new_index_name = input()
mainfunk(pdf_file) #, new_index_name)