import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

# Try checking if jess4 has a cover image under other formats
for ext in ['png', 'PNG', 'jpg', 'jpeg']:
    for suffix in ['cc', 'c1', 'c2', '01']:
        url = f"https://ncert.nic.in/textbook/pdf/jess4{suffix}.{ext}"
        res = subprocess.run(['curl', '-s', '-I', '-A', 'Mozilla/5.0', url], capture_output=True, text=True)
        if '200 OK' in res.stdout:
            print(f"Found alternate cover for jess4: {url}")
            target = r"d:\NCERT_Textbook\Class_10\Social_Science\Political_Science_Democratic_Politics\cover.jpg"
            subprocess.run(['curl', '-s', '-A', 'Mozilla/5.0', url, '-o', target])

BASE_DIR = r"d:\NCERT_Textbook\Class_10"

print("\n=== Class 10 Textbook Download Verification Summary ===")
total_size = 0
total_files = 0
total_pdfs = 0

for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        fpath = os.path.join(root, f)
        sz = os.path.getsize(fpath)
        total_size += sz
        total_files += 1
        if f.lower().endswith('.pdf'):
            total_pdfs += 1

print(f"Total Disk Usage: {total_size / (1024*1024):.2f} MB")
print(f"Total Files: {total_files}")
print(f"Total PDFs (Chapters, Prelims, Solutions): {total_pdfs}")

# Tree view
print("\n--- Folder Structure ---")
for root, dirs, files in sorted(os.walk(BASE_DIR)):
    level = root.replace(BASE_DIR, '').count(os.sep)
    indent = ' ' * 4 * level
    folder_name = os.path.basename(root)
    if folder_name == "Class_10":
        print(f"Class_10/")
    else:
        pdf_count = len([f for f in files if f.endswith('.pdf')])
        has_cover = any(f.startswith('cover') for f in files)
        has_zip = any(f.endswith('.zip') for f in files)
        print(f"{indent}📁 {folder_name}/ ({pdf_count} PDFs, Cover: {'✓' if has_cover else 'N/A'}, ZIP: {'✓' if has_zip else 'N/A'})")
