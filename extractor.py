import spacy

nlp = spacy.load("en_core_web_trf")

action_phrases = ["i'll", "i will", "can you", "could you", "needs to", "need to", "will"]

def extract_action_items(transcript_text):
    lines = transcript_text.split("\n")

    results = []
    seen_tasks = set()

    for line in lines:
        line = line.strip()
        if ":" not in line:
            continue

        speaker, text = line.split(":", 1)
        speaker = speaker.strip()
        text = text.strip()

        text_lower = text.lower()
        is_action = any(phrase in text_lower for phrase in action_phrases)

        if not is_action:
            continue

        task_key = text_lower
        if task_key in seen_tasks:
            continue
        seen_tasks.add(task_key)

        doc = nlp(text)

        if text_lower.startswith("i ") or "i'll" in text_lower or "i will" in text_lower:
            owner = speaker
        else:
            people_mentioned = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
            owner = people_mentioned[0] if people_mentioned else "Unknown"

        dates_mentioned = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
        deadline = dates_mentioned[0] if dates_mentioned else "Not specified"

        owner_score = 50 if owner != "Unknown" else 10
        deadline_score = 50 if deadline != "Not specified" else 10
        confidence = owner_score + deadline_score

        status = "CONFIDENT" if confidence >= 70 else "NEEDS REVIEW"

        results.append({
            "task": text,
            "owner": owner,
            "deadline": deadline,
            "confidence": confidence,
            "status": status
        })

    return results