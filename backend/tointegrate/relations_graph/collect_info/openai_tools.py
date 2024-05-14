tools = {
    "spara_information_om_personer": {
        "type": "function",
        "function": {
            "name": "spara_information_om_personer",
            "description": "Använd för att lägga till information om personer genom att lägga in alla i en lista.",
            "parameters": {
                "type": "object",
                "properties": {
                    "list_med_personer": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "förnamn": {
                                    "type": "string",
                                    "description": "Namnet på personen",
                                },
                                "efternamn": {
                                    "type": "string",
                                    "description": "Efternamnet på personen, skriv 'okänd' om efternamnet inte är känt",
                                },
                                "description": {
                                    "type": "string",
                                    "description": "En text som innehåller informationen om personen",
                                },
                            },
                            "description": "En lista med namn och information om personer",
                            "required": ["namn", "information"],
                        },
                    },
                }
            }
        }
    },
    "spara_information_om_relationer": {
        "type": "function",
        "function": {
            "name": "spara_information_om_relationer",
            "description": "Använd för att registrera information om relationen mellan två personer, t. ex. åsikter, släktband, gemensamma upplevelser etc.",
            "parameters": {
                "type" : "object",
                "properties": {
                    "relationer": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "person1": {
                                    "type": "object",
                                    "properties": {
                                        "förnamn": {
                                            "type": "string",
                                            "description": "Namnet på personen",
                                        },
                                        "efternamn": {
                                            "type": "string",
                                            "description": "Efternamnet på personen, skriv 'okänd' om efternamnet inte är känt",
                                        },
                                    },
                                },
                                "person2": {
                                    "type": "object",
                                    "properties": {
                                        "förnamn": {
                                            "type": "string",
                                            "description": "Namnet på personen",
                                        },
                                        "efternamn": {
                                            "type": "string",
                                            "description": "Efternamnet på personen, skriv 'okänd' om efternamnet inte är känt",
                                        },
                                    },
                                },
                                "relation": {
                                    "type": "string",
                                    "description": "Relationen mellan personerna",
                                },
                            },
                            "required": ["person1", "person2", "beskrivning_av_relation"],
                            "description": "En relation med två personer och information om relationen",
                        },
                        "description": "En lista med information om relationer",
                    },
                }
            }
        }
    }
}
