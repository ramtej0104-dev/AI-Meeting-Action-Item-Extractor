action_phrases = ["i'll", "i will", "can you", "could you", "needs to", "need to", "will"]
known_names = ["Sarah", "Mark", "Priya", "John"]
time_words = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "tomorrow", "today", "next week"]

with open("sample_transcript.txt", "r") as f:
    lines = f.readlines()

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

    if "i'll" in text_lower or "i will" in text_lower:
        owner = speaker
    else:
        mentioned_names = [name for name in known_names if name in text and name != speaker]
        owner = mentioned_names[0] if mentioned_names else "Unknown"

    found_deadlines = [word for word in time_words if word in text_lower]
    deadline = found_deadlines[0].capitalize() if found_deadlines else "Not specified"

    if owner != "Unknown" and deadline != "Not specified":
        status = "CONFIDENT"
    else:
        status = "NEEDS REVIEW"

    print(f"Task: {text}")
    print(f"  Owner: {owner}")
    print(f"  Deadline: {deadline}")
    print(f"  Status: {status}")
    print()