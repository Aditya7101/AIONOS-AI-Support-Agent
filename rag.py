import os
import re

KNOWLEDGE_BASE = "knowledge_base"


def search_knowledge_base(query):
    results = []

    # Convert the user's question into useful words
    query_words = set(
        re.findall(r"\b[a-zA-Z]{3,}\b", query.lower())
    )

    for filename in os.listdir(KNOWLEDGE_BASE):

        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(KNOWLEDGE_BASE, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        content_words = set(
            re.findall(r"\b[a-zA-Z]{3,}\b", content.lower())
        )

        # Count matching words
        score = len(query_words.intersection(content_words))

        if score > 0:
            results.append((score, filename, content))

    # Highest matching document first
    results.sort(reverse=True)

    if not results:
        return "No relevant document was found in the AIONOS knowledge base."

    # Return the best matching document
    best_match = results[0]

    return f"""
Document: {best_match[1]}

{best_match[2]}
"""