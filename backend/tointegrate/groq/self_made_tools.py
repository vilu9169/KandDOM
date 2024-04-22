tools = {
    "NBA": {
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
    "weather": {
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
    "ny_person": {
        "type": "function",
        "function": {
            "name": "lägg_till_person",
            "description": "Använd för att registrera en tidigare inte känd person",
            "parameters": {
                "type": "object",
                "properties": {
                    "namn": {"type": "string", "description": "Namnet på personen, både förnamn och efternamn om tillgängligt"},
                    "information": {
                        "type": "string",
                        "description": "Sammanställ information om personen",
                    },
                },
            },
        },
    },
}
