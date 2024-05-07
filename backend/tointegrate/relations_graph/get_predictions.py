from openai import OpenAI
from openai.types.chat import ChatCompletion
from groq import Groq
from groq.types.chat import ChatCompletion as GroqChatCompletion
from vertexai.generative_models import GenerativeModel, GenerationConfig
from anthropic import Anthropic
from anthropic.types import Message
from collect_info.util import gemini_unfiltered

from dotenv import load_dotenv
import os

load_dotenv()

def _get_model_prediction(prompt, system,  model, tools=[], previous_messages=None, client = None):
    messages=[
            {
                "role": "system",
                "content": system,
            },
        ],
    for message in previous_messages:
        messages.append({
            message
        })
    messages.append({
        "role": "user",
        "content": prompt,
    })
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        tools=tools,
    )
    return response


def get_openai_prediction(prompt, system, model="gpt-3.5-turbo-0125", tools= [], previous_messages=None, client : OpenAI =  None) -> ChatCompletion:
    if client == None:
        client = OpenAI()

    return _get_model_prediction(prompt, system, model, tools, previous_messages, client)   


def get_groq_prediction(prompt, system, model="llama3-70b-8192", tools= [], previous_messages=None, client : Groq =  None) -> GroqChatCompletion:
    if client == None:
        client = Groq(os.environ.get("GROQ_API_KEY"))

    return _get_model_prediction(prompt, system, model, tools, previous_messages, client)



def get_claude_prediction(prompt, system, model="claude-3-haiku@20240307", tools= [], previous_messages=None, client : Anthropic =  None) -> Message:
    if client == None:
        client = Anthropic()

    return _get_model_prediction(prompt, system, model, tools, previous_messages, client)


def get_gemini_prediction(prompt, system, model="gemini-1.5-pro-preview-0409", tools= [], previous_messages=None, config = {}, safety_settings = gemini_unfiltered) -> ChatCompletion:
    if client == None:
        client = GenerativeModel(model, generation_config=config, safety_settings=safety_settings)
    contents = [system]
    for message in previous_messages:
        contents.append(message)
    contents.append(prompt)
    return client.generate_content(contents=contents, tools=tools)
    