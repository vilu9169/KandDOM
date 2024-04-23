tools = {
    "ny_info_person": {
        "type": "function",
        "function": {
            "name": "ny_information_om_person",
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
                "required": ["namn", "information"],
            },
        },
    },
    "ny_info_relation": {
        "type": "function",
        "function": {
            "name": "ny_information_om_relation",
            "description": "Använd för att registrera information om relationen mellan två personer, t. ex. åsikter, släktband, gemensamma upplevelser etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "person1": {
                        "type": "string",
                        "description": "Namnet på den ena personen",
                    },
                    "person2": {
                        "type": "string",
                        "description": "Namnet på den andra personen",
                    },
                    "beskrivning av relation": {
                        "type": "string",
                        "description": "Namn på personerna och hur de är kopplade till varandra",
                    },
                },
                "required": ["person1", "person2", "beskrivning av relation"],
            },
        },
    },
    "sök_material" : {
        "type": "function",
        "function": {
            "name": "sök_i_material",
            "description": "Använd för att söka i materialet, för att reda ut oklarheter",
            "parameters": {
                "type": "object",
                "properties": {
                    "fråga": {
                        "type": "string",
                        "description": "Frågan som ska redas ut",
                    },
                },
                "required": ["fråga"],
            },
        },
    }
}
