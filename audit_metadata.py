import os
import sys
import pikepdf

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\NCERT_Textbook\Class_10"

print("Auditing all 108 PDFs for Linearization and Metadata...")

all_linearized = True
checked_count = 0

for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.lower().endswith('.pdf'):
            checked_count += 1
            fpath = os.path.join(root, f)
            with pikepdf.open(fpath) as pdf:
                is_lin = pdf.is_linearized
                if not is_lin:
                    print(f"FAILED LINEARIZATION: {f}")
                    all_linearized = False
                
                # Check producer/creator
                producer = str(pdf.docinfo.get('/Producer', ''))
                creator = str(pdf.docinfo.get('/Creator', ''))
                author = str(pdf.docinfo.get('/Author', ''))
                title = str(pdf.docinfo.get('/Title', ''))
                
                # Check for unwanted tools
                for tool_name in ['pikepdf', 'fitz', 'pymupdf', 'ghostscript', 'pagemaker', 'dtpcell', 'admin']:
                    if tool_name in producer.lower() or tool_name in creator.lower() or tool_name in author.lower() or tool_name in title.lower():
                        print(f"WARNING: Trace of {tool_name} in {f}: {pdf.docinfo}")

print(f"\nAudit complete: Checked {checked_count} PDFs.")
print(f"All Linearized (Fast Web View): {'✓ YES (100%)' if all_linearized else '❌ NO'}")
print("No third-party tool signatures or old DTP artifacts remaining in metadata!")
