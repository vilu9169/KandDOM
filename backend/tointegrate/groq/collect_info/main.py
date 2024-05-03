from process_text import process_text
from modify_people import Personhandler


text : str

file_path = ""

with open(file_path, "r") as file:
    text = file.read()


person_handler = Personhandler()


