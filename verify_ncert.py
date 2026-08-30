import json
import sys
import urllib.request
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

with open('all_ncert_books.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

print(f"Total books: {len(books)}")

# Group by Class
by_class = {}
for b in books:
    cls = b['class_name']
    by_class.setdefault(cls, []).append(b)

for cls, b_list in sorted(by_class.items(), key=lambda x: str(x[0])):
    print(f"\n--- {cls} ({len(b_list)} books) ---")
    subjects = {}
    for b in b_list:
        subjects.setdefault(b['subject'], []).append(b)
    for subj, subj_books in subjects.items():
        print(f"  [{subj}] ({len(subj_books)} books):")
        for b in subj_books[:3]:
            print(f"    - {b['book_title']} (code: {b['book_code']}, ch: {b['chapters_count']}, zip: {b['complete_book_zip']})")
        if len(subj_books) > 3:
            print(f"    - ... and {len(subj_books) - 3} more")

# Let's test a sample of URLs using curl -I to check HTTP status
sample_urls = [
    books[0]['complete_book_zip'],
    books[0]['chapters'][0]['url'] if books[0]['chapters'] else books[0]['prelims_pdf'],
    books[50]['complete_book_zip'],
    books[100]['complete_book_zip'],
    books[200]['chapters'][0]['url'] if books[200]['chapters'] else books[200]['prelims_pdf'],
]

print("\n=== Testing Sample URLs with curl ===")
for url in sample_urls:
    res = subprocess.run(['curl', '-s', '-I', '-A', 'Mozilla/5.0', url], capture_html=False, capture_output=True, text=True)
    first_line = res.stdout.splitlines()[0] if res.stdout else "No response"
    print(f"URL: {url} -> {first_line}")
