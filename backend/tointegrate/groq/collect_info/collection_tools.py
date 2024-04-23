tools = {
    "ny_info": {
        "type": "function",
        "function": {
            "name": "ny_information",
            "description": "Använd för att lägga till information om en person",
            "parameters": {
                "type": "object",
                "properties": {
                    "namn": {
                        "type": "string",
                        "description": "Namnet på personen",
                    },
                    "information": {
                        "type": "string",
                        "description": "En text som innehåller informationen om personen",
                    },
                },
                "required" : ["namn","information"],
            },
        },
    },
    "multiply": {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiply two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number",
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number",
                    },
                },
                "required": ["a", "b"],
            },
        },
    },
}
