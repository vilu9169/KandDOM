tools = {
    "ny_person": {
        "type": "function",
        "function": {
            "name": "lägg_till_person",
            "description": "Använd för att registrera en tidigare inte känd person",
            "parameters": {
                "type": "object",
                "properties": {
                    "namn": {
                        "type": "string",
                        "description": "Namnet på personen, både förnamn och efternamn om tillgängligt",
                    },
                    "information": {
                        "type": "string",
                        "description": "Sammanställ information om personen",
                    },
                },
            },
        },
    },
    "ny_info": {
        "type": "function",
        "function": {
            "name": "ny_information",
            "description": "Använd för att lägga till information om en person som tidigare inte var registrerat",
            "parameters": {
                "type": "object",
                "properties": {
                    "namn": {
                        "type": "string",
                        "description": "Namnet på personen, både förnamn och efternamn om tillgängligt",
                    },
                    "information": {
                        "type": "string",
                        "description": "Den nya informationen som ska registreras",
                    },
                },
            },
        },
    },
}
