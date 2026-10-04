from extractor import extract_action_items
from annotated_transcripts import TEST_CASES

total_items = 0
correct_owner = 0
correct_deadline = 0

for i, case in enumerate(TEST_CASES, start=1):
    results = extract_action_items(case["transcript"])
    expected = case["expected"]

    print(f"--- Transcript {i} ---")
    print(f"Expected {len(expected)} action item(s), extractor found {len(results)}.")

    for j, exp in enumerate(expected):
        total_items += 1
        if j >= len(results):
            print(f"  MISSED item {j+1}: expected owner={exp['owner']}, deadline={exp['deadline']}")
            continue

        got = results[j]
        owner_ok = got["owner"] == exp["owner"]
        deadline_ok = got["deadline"] == exp["deadline"]

        if owner_ok:
            correct_owner += 1
        if deadline_ok:
            correct_deadline += 1

        print(f"  Task: {got['task']}")
        print(f"    Owner    -> expected: {exp['owner']:12} got: {got['owner']:12} {'OK' if owner_ok else 'WRONG'}")
        print(f"    Deadline -> expected: {exp['deadline']:14} got: {got['deadline']:14} {'OK' if deadline_ok else 'WRONG'}")
    print()

print(f"Owner accuracy:    {correct_owner}/{total_items} = {correct_owner/total_items*100:.0f}%")
print(f"Deadline accuracy: {correct_deadline}/{total_items} = {correct_deadline/total_items*100:.0f}%")