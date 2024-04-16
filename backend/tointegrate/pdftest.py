import subprocess
import PyPDF2

def convert_pdf_to_text(pdf_file, output_file):
    try:
        subprocess.run(['ocrmypdf',"--redo-ocr" ,'--language', 'swe', pdf_file, output_file], check=True)
        
        
        print("PDF converted to text successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error converting PDF to text: {e}")

# Specify the input PDF file and output text file
pdf_file = "fuppar/Uppsala TR B 2613-23 Aktbil 21.pdf"
output_file = "fuppar_ocr/ocr_Uppsala TR B 2613-23 Aktbil 21.pdf"
# Call the function to convert the PDF to text
#convert_pdf_to_text(pdf_file, output_file)

def extract_text_from_pdf(pdf_file):
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            text = ""
            #Separate pages so they start with { and end with }
            for page_num in range(num_pages):
                text += "{Sida "+str(page_num)+" börjar\n"
                page = reader.pages[page_num]
                text += page.extract_text()
                text += " Sida "+str(page_num)+" slut}"
            return text
    except FileNotFoundError:
        print(f"Error: File '{pdf_file}' not found.")
        return None

#Specify the input PDF file
pdf_file = "fuppar_ocr/ocr_Uppsala TR B 2613-23 Aktbil 21.pdf"

#Call the function to extract text from the PDF
text = extract_text_from_pdf(pdf_file)

# Specify the output text file
output_text_file = "KandDOM/fuppar_txt/mordbrand.txt"

# Write the extracted text to the output text file, needs to be able to handle scandinavian characters
with open(output_text_file, 'w', encoding='utf-8') as file:
    file.write(text)

print("Text written successfully!")