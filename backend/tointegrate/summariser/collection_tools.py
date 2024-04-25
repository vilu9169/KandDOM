tools = {
    "timelinemaker": {
        "type": "function",
        "function": {
            "name": "skapa_händelse",
            "description": "Använd för att spara information och tid om en händelse.",
            "parameters": {
                "type": "object",
                "properties": {
                    "time": {
                        "type": "string",
                        #"format" : "date-time",
                        "description": "Datum och tid då händelsen inträffade. Skall endast vara en tid per händelse.",
                    },
                    "information": {
                        "type": "string",
                        "description": "Information om händelsen.",
                    },
                },
                "required": ["time", "information"],
            },
        },
    },
}
