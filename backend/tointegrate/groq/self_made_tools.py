tools = {
    "NBA" : {
            "type": "function",
            "function": {
                "name": "get_game_score",
                "description": "Get the score for a given NBA game",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "team_name": {
                            "type": "string",
                            "description": "The name of the NBA team (e.g. 'Golden State Warriors')",
                        }
                    },
                    "required": ["team_name"],
                },
            },
        },

    "weather" : {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the weather for a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The location for which to get the weather (e.g. 'San Francisco')",
                        }
                    },
                    "required": ["location"],
                },
            },
        },
}