import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('all_ncert_books.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

by_class = {}
for b in books:
    cls = b['class_name']
    by_class.setdefault(cls, []).append(b)

class_order = [
    "Class I", "Class II", "Class III", "Class IV", "Class V", "Class VI",
    "Class VII", "Class VIII", "Class IX", "Class X", "Class XI", "Class XII",
    "Class XI & XII Combined"
]

print("| Class | Total Books | Major Subjects | Example Book & Code |")
print("| :--- | :--- | :--- | :--- |")

for cls in class_order:
    b_list = by_class.get(cls, [])
    subjects = set(b['subject'] for b in b_list)
    ex = b_list[0] if b_list else None
    ex_str = f"`{ex['book_code']}` ({ex['book_title']})" if ex else "N/A"
    subj_sample = ", ".join(list(subjects)[:4]) + ("..." if len(subjects) > 4 else "")
    print(f"| **{cls}** | {len(b_list)} | {subj_sample} | {ex_str} |")
