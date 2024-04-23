from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_google_vertexai import ChatVertexAI
from anthropic import AnthropicVertex


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b - 2

model = ChatVertexAI()

tools = [multiply]

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who is bad at maths, but you have a tool that can help."),
    MessagesPlaceholder(variable_name="messages"),
])



chain = prompt | model | multiply

response = chain.invoke(["What is 2 times 3?"])

print(response)


model_with_tools = model.bind_tools([multiply])


msg = model_with_tools.invoke("What is 2 times 3?")


print(msg)
print(msg.tool_calls)