import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('all_ncert_books.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

c10_books = [b for b in books if b['class_name'] == 'Class X' or b['class_id'] == '10']

print(f"Total Class 10 books found: {len(c10_books)}")

with open('class10_books.json', 'w', encoding='utf-8') as f:
    json.dump(c10_books, f, indent=2, ensure_ascii=False)

# Let's group by subject
by_subj = {}
for b in c10_books:
    by_subj.setdefault(b['subject'], []).append(b)

for subj, b_list in by_subj.items():
    print(f"\n### {subj} ({len(b_list)} books)")
    for b in b_list:
        print(f"- **{b['book_title']}** (Code: `{b['book_code']}`, Chapters: {b['chapters_count']})")
        print(f"  ZIP: {b['complete_book_zip']}")
        print(f"  Web: {b['web_url']}")
