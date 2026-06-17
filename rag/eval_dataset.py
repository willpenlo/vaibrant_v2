EVAL_QUESTIONS = [
    {
        "question": "How does vAIbrant authenticate API requests?",
        "expected_keywords": ["api key", "x-api-key", "header"],
        "expected_source": "vaibrant_overview.txt"
    },
    {
        "question": "What database does vAIbrant use?",
        "expected_keywords": ["sqlite", "vaibrant.db"],
        "expected_source": "vaibrant_overview.txt"
    },
    {
        "question": "What risk levels does vAIbrant use?",
        "expected_keywords": ["low", "medium", "high", "critical"],
        "expected_source": "vaibrant_overview.txt"
    },
    {
        "question": "What is the capital of France?",
        "expected_keywords": [],
        "expected_source": None,
        "should_refuse": True
    }
]