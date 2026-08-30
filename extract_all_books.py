import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('s17.js', 'r', encoding='utf-8', errors='ignore') as f:
    s17 = f.read()

# Let's remove block comments /* ... */ first so we don't pick up commented books,
# but let's also be careful about single line comments //
def clean_js(js_code):
    # Remove block comments
    js_no_block = re.sub(r'/\*.*?\*/', '', js_code, flags=re.DOTALL)
    # Filter lines that start with // (ignoring leading whitespace)
    clean_lines = []
    for line in js_no_block.split('\n'):
        line_s = line.strip()
        if line_s.startswith('//'):
            continue
        # If line has inline comment, remove it
        if '//' in line:
            line = line.split('//')[0]
        clean_lines.append(line)
    return '\n'.join(clean_lines)

clean_s17 = clean_js(s17)

# Class mappings:
# 1 -> Class 1, ..., 12 -> Class 12, 13 -> Class XI & XII Combined
class_name_map = {
    "1": "Class I",
    "2": "Class II",
    "3": "Class III",
    "4": "Class IV",
    "5": "Class V",
    "6": "Class VI",
    "7": "Class VII",
    "8": "Class VIII",
    "9": "Class IX",
    "10": "Class X",
    "11": "Class XI",
    "12": "Class XII",
    "13": "Class XI & XII Combined"
}

# Regex to find each if / else if block in change1
# Pattern matches: if / else if (...) { ... }
# Example: if((document.test.tclass.value==1) && (document.test.tsubject.options[sind].text=="English"))
pattern = r'if\s*\(\s*\(document\.test\.tclass\.value\s*==\s*([^\)]+?)\)\s*&&\s*\(document\.test\.tsubject\.options\[sind\]\.text\s*==\s*["\']([^"\']+)["\']\)\s*\)\s*\{([^}]+)\}'

matches = list(re.finditer(pattern, clean_s17, re.DOTALL))
print(f"Total matching class/subject blocks found: {len(matches)}")

all_books = []
unique_book_codes = set()

for m in matches:
    cls_val = m.group(1).strip()
    subj_name = m.group(2).strip()
    body = m.group(3)
    
    # Parse options inside body
    # document.test.tbook.options[1].text="Mridang";
    # document.test.tbook.options[1].value="textbook.php?aemr1=0-9"
    # Note: sometimes multiple text assignments or value assignments
    # Let's extract per option index
    
    opt_texts = dict(re.findall(r'document\.test\.tbook\.options\[(\d+)\]\.text\s*=\s*["\']([^"\']*)["\']', body))
    opt_vals = dict(re.findall(r'document\.test\.tbook\.options\[(\d+)\]\.value\s*=\s*["\']([^"\']*)["\']', body))
    
    for idx, val in opt_vals.items():
        if not val or val == "-1":
            continue
        title = opt_texts.get(idx, "").strip()
        if not title or title.startswith("..Select"):
            continue
        
        # Parse query string from val: e.g. "textbook.php?aemr1=0-9"
        # or "?aemr1=0-9"
        m_val = re.search(r'([a-zA-Z0-9]+)\s*=\s*(\d+)-(\d+)', val)
        if m_val:
            book_code = m_val.group(1).strip()
            start_ch = int(m_val.group(2))
            end_ch = int(m_val.group(3))
        else:
            m_val2 = re.search(r'\?([a-zA-Z0-9]+)', val)
            if m_val2:
                book_code = m_val2.group(1).strip()
                start_ch = 0
                end_ch = 0
            else:
                book_code = val
                start_ch = 0
                end_ch = 0
        
        # Construct URLs
        zip_url = f"https://ncert.nic.in/textbook/pdf/{book_code}dd.zip"
        prelims_url = f"https://ncert.nic.in/textbook/pdf/{book_code}ps.pdf"
        cover_url = f"https://ncert.nic.in/textbook/pdf/{book_code}cc.jpg"
        web_url = f"https://ncert.nic.in/textbook.php?{book_code}={start_ch}-{end_ch}"
        
        chapters = []
        if end_ch > 0:
            for ch_num in range(1, end_ch + 1):
                ch_code = f"{ch_num:02d}"
                ch_url = f"https://ncert.nic.in/textbook/pdf/{book_code}{ch_code}.pdf"
                chapters.append({
                    "chapter_number": ch_num,
                    "chapter_code": ch_code,
                    "url": ch_url
                })
        
        book_info = {
            "class_id": cls_val,
            "class_name": class_name_map.get(cls_val, f"Class {cls_val}"),
            "subject": subj_name,
            "book_title": title,
            "book_code": book_code,
            "chapters_count": end_ch,
            "web_url": web_url,
            "complete_book_zip": zip_url,
            "prelims_pdf": prelims_url,
            "cover_image": cover_url,
            "chapters": chapters
        }
        all_books.append(book_info)
        unique_book_codes.add(book_code)

print(f"Total books extracted: {len(all_books)}")
print(f"Unique book codes count: {len(unique_book_codes)}")

with open('all_ncert_books.json', 'w', encoding='utf-8') as f:
    json.dump(all_books, f, indent=2, ensure_ascii=False)

print("Saved all books to all_ncert_books.json")
