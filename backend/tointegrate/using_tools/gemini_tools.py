import vertexai
from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)


async def generate_function_call(prompt: str, project_id: str, location: str) -> tuple:
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    # Initialize Gemini model
    model = GenerativeModel("gemini-1.0-pro")

    # Specify a function declaration and parameters for an API request
    add_to_diary = FunctionDeclaration(
        name="add_to_diary",
        description="Add a specific entry as well as todays date to the user's diary",
        # Function parameters are specified in OpenAPI JSON schema format
        parameters={
            "type": "object",
            "properties": {"diary_entry": {"type": "string", "description": "diary entry to add"}, "date" : {"type": "string", "description": "date of the diary entry"}},
        },
    )

    # Define a tool that includes the above get_current_weather_func
    diary_tool = Tool(
        function_declarations=[add_to_diary],
    )

    # Define the user's prompt in a Content object that we can reuse in model calls
    user_prompt_content = Content(
        role="user",
        parts=[
            Part.from_text(prompt),
        ],
    )

    # Send the prompt and instruct the model to generate content using the Tool that you just created
    response = await model.generate_content_async(
        user_prompt_content,
        generation_config=GenerationConfig(temperature=0),
        tools=[diary_tool],
    )
    response_function_call_content = response.candidates[0].content

    # Check the function name that the model responded with, and make an API call to an external system
    if (
        response.candidates[0].content.parts[0].function_call.name
        == "add_to_diary"
    ):
        # Extract the arguments to use in your API call
        entry = (
            response.candidates[0].content.parts[0].function_call.args["diary_entry"]+response.candidates[0].content.parts[0].function_call.args["date"]
        )

        with open("KandDOM/backend/tointegrate/using_tools/diary.txt", "a") as f:
            f.write(entry + "\n")
       # api_response = "Diary entry added successfully"
        api_response = """{ "location": "Boston, MA", "temperature": 38, "description": "Partly Cloudy",
                         "icon": "partly-cloudy", "humidity": 65, "wind": { "speed": 10, "direction": "NW" } }"""
        
    response = model.generate_content(
        [
            user_prompt_content,  # User prompt
            response_function_call_content,  # Function call response
            Content(
                parts=[
                    Part.from_function_response(
                        name="get_current_weather",
                        response={
                            #"content": api_response,  # Return the API response to Gemini
                        },
                    )
                ],
            ),
        ],
        tools=[diary_tool],
    )
    # Get the model summary response
    summary = response.candidates[0].content.parts[0].text

    return summary, response

import asyncio

result = asyncio.run(generate_function_call("Add a diary entry: 'Went for a walk in the park', todays date is march 3rd", "robust-summit-417910", "us-central1"))

print("summary: " ,result[0])
print("response: ", result[1])