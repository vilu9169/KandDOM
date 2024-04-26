tools = {
    "ny_information_om_person": {
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
                        "description": "Namn på personerna och hur de är kopplade till varandra t. ex. 'Person1 är moder till person2' eller 'Person1 och Person2 åkte till Paris tillsammans 2019'",
                    },
                },
                "required": ["person1", "person2", "beskrivning av relation"],
            },
        },
    },


    "ny_gruppering": {
        "type": "function",
        "function": {
            "name": "ny_gruppering",
            "description": "Använd för att registrera en gruppering av personer som nämns i texten, t. ex. en familj, företag, organisation etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "gruppering": {
                        "type": "string",
                        "description": "Namnet eller beskrivning av grupperingen",
                    },
                    "personer": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                        "description": "En lista med namn på personer som tillhör grupperingen",
                    },
                },
                "required" : ["gruppering", "personer"],
            },
        },
    },


    "sök_material" : {
        "type": "function",
        "function": {
            "name": "sök_material",
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
    },
    "ändra_beskrivning": {
        "type": "function",
        "function": {
            "name": "ändra_beskrivning",
            "description": "Använd för att ändra beskrivning av en person, den nya beskrivningen skriver över den gamla",
            "parameters": {
                "type": "object",
                "properties": {
                    "ny_beskrivning": {
                        "type": "string",
                        "description": "Den nya fullständiga beskrivningen",
                    },
                },
                "required": ["ny_beskrivning"],
            },
        },
    },
    "uppdatera_namn" : {
        "type": "function",
        "function": {
            "name": "sätt_namn",
            "description": "Använd för att sätta namn på en person som tidigare inte har ett namn, eller som har fel namn",
            "parameters": {
                "type": "object",
                "properties": {
                    "namn": {
                        "type": "string",
                        "description": "Namnet på personen",
                    },
                },
                "required": ["namn"],
            },
        },
    },
    "identifiera_person": {
        "type": "function",
        "function": {
            "name": "identifiera_person",
            "description": "Använd för att klassificera om en person finns i arkivet eller inte och ange dess namn",
            "parameters": {
                "type": "object",
                "properties": {
                    "finns_sedan_tidigare" : {
                        "type": "boolean",
                        "description": "Om personen finns i arkivet sedan tidigare",
                    },
                    "namn": {
                        "type": "string",
                        "description": "Namnet på den identifierade personen",
                    },
                    "beskrivning_av_ny_person": {
                        "type": "string",
                        "description": "Kort identifierande text",
                    },
                },
                "required": ["finns_sedan_tidigare", "namn", "beskrivning_av_ny_person"],
            },
        },
    },
}
