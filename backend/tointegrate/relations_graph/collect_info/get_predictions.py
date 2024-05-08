from openai import OpenAI
from openai.types.chat import ChatCompletion
from groq import Groq
from groq.types.chat import ChatCompletion as GroqChatCompletion
from vertexai.generative_models import GenerativeModel, GenerationConfig
from anthropic import Anthropic
from anthropic.types import Message
from anthropic import AnthropicVertex
import boto3
import json
import time

from util import gemini_unfiltered


from dotenv import load_dotenv
import os

load_dotenv()


def _get_model_prediction(
    prompt, system, model, tools=[], client=None, max_tokens=512,
):
    messages = [
        {
            "role": "system",
            "content": system,
        },
    ]

    messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        tools=tools,
        max_tokens=max_tokens,
    )
    return response


def get_openai_prediction(
    prompt,
    system,
    model="gpt-3.5-turbo-0125",
    tools=[],
    client: OpenAI = None,
    max_tokens=512,
) -> ChatCompletion:
    if client == None:
        client = OpenAI()

    return _get_model_prediction(
        prompt, system, model, tools, client, max_tokens
    )


def get_groq_prediction(
    prompt,
    system,
    model="llama3-70b-8192",
    tools=[],
    client: Groq = None,
    max_tokens=512,
) -> GroqChatCompletion:
    if client == None:
        client = Groq(os.environ.get("GROQ_API_KEY"))

    return _get_model_prediction(
        prompt, system, model, tools, client, max_tokens
    )




def get_claude_prediction_tools(prompt,
    system,
    model="claude-3-haiku@20240307",
    tools=[],
    max_tokens=512):
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    user_message = {"role": "user", "content": prompt}
    return client.beta.tools.messages.create(messages=[user_message], model=model, system=system, tools=tools, max_tokens=max_tokens)


def get_claude_prediction_string(
    prompt,
    system,
    model="claude-3-haiku@20240307",
    use_aws=False,
    max_tokens=512,
):
    try:
        result =  _get_vertex_claude_prediction(
            prompt, system, mode, max_tokens=max_tokens
        )
        return result.content[0].text
    except Exception as vertex_e:
        print(vertex_e)
        print("Switching to anthropic")
        try:
            result =  _get_anthropic_prediction(
            prompt, system, model, tools, max_tokens
        ).content[0].text
        except Exception as anthro_e:
            if use_aws:
                print(anthro_e)
                print("Switching to AWS")
                result = _get_AWS_claude_prediction(
                    prompt, system, max_tokens
                )
            else:
                time.sleep(1)
                print("trying to use claude again")
                result = get_claude_prediction_string(
                    prompt, system, model, use_aws, max_tokens
                )
    return result

def get_gemini_prediction(
    prompt,
    system,
    model="gemini-1.5-pro-preview-0409",
    tools=[],
    config={},
    safety_settings=gemini_unfiltered,
) -> ChatCompletion:
    if client == None:
        client = GenerativeModel(
            model, generation_config=config, safety_settings=safety_settings, system_instruction=system
        )
    return client.generate_content(contents=[{"type" : "user", "text" : prompt}], tools=tools)






def _get_anthropic_prediction(prompt,
    system,
    model="claude-3-haiku@20240307",
    tools=[],
    max_tokens=512):
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    user_message = {"role": "user", "content": prompt}
    return client.messages.create(messages=[user_message], model=model, system=system, max_tokens=max_tokens)




def _get_AWS_claude_prediction(prompt,
    system, max_tokens = 512):
    client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")
    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "system": system,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}],
                    }
                ],
            }
        ),
    )

    return json.loads(response.get("body").read()).get("content", [])[0]["text"]




def _get_vertex_claude_prediction(prompt,
    system,
    model="claude-3-haiku@20240307",
    max_tokens=512,
    ):
    client = AnthropicVertex(region="europe-west4", project_id="robust-summit-417910")
    message = client.messages.create(
                max_tokens=max_tokens,
                system=system,
                messages=[{
                    "role": "user",
                    "content": prompt,
                }],
                model=model,
            )
    return message