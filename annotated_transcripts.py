TEST_CASES = [
    {
        "transcript": """Rahul: Divya, can you review the budget report by next Tuesday?
Divya: Sure, I'll check it before then.
Rahul: Divya, can you review the budget report by next Tuesday?""",
        "expected": [
            {"owner": "Divya", "deadline": "next Tuesday"},
            {"owner": "Divya", "deadline": "Not specified"},
        ]
    },
    {
        "transcript": """Priya: Someone needs to call the vendor on the 15th.
Priya: I will send the invoice tomorrow.""",
        "expected": [
            {"owner": "Unknown", "deadline": "the 15th"},
            {"owner": "Priya", "deadline": "tomorrow"},
        ]
    },
    {
        "transcript": """Arjun: Meera, could you finalize the deck before Thursday?
Meera: Will do, I'll finish it by Thursday.
Kabir: We need to update the server logs next week.""",
        "expected": [
            {"owner": "Meera", "deadline": "Thursday"},
            {"owner": "Meera", "deadline": "Thursday"},
            {"owner": "Unknown", "deadline": "next week"},
        ]
    },
]