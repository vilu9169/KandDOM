#from collection_tools import tools
from get_predictions import get_openai_prediction
from dotenv import load_dotenv

load_dotenv()

text : str

file_path = "KandDOM/fuppar_txt/schizzomord.txt"

with open(file_path, "r") as file:
    text = file.read()

pages = text.split(chr(28))


to_process = pages[0]


text : str


file_path = "KandDOM/fuppar_txt/schizzomord.txt"

with open(file_path, "r") as file:
    text = file.read()

