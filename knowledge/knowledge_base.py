import os
import json

def load_kvkk_documents():
    docs = []
    for filename in os.listdir("knowledge/data"):
        if filename.endswith(".json"):
            with open(os.path.join("knowledge/data", filename), "r", encoding="utf-8") as f:
                data = json.load(f)
                for entry in data:
                    docs.append(entry["content"])
    return docs

def answer_kvkk_question(question, documents):
    question_lower = question.lower()
    question_words = question_lower.split()

    for doc in documents:
        doc_lower = doc.lower()

        # Doğrudan cümle eşleşmesi
        if question_lower in doc_lower:
            return doc[:1000]

        # Kelime bazlı eşleşme
        match_score = sum(word in doc_lower for word in question_words)
        if match_score >= 2:
            return doc[:1000]

    return "Üzgünüz, bu soruya dair bir bilgi bulunamadı."
