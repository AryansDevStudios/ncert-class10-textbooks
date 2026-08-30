import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\NCERT_Textbook\Class_10"

print("Scanning all 108 Class 10 PDFs for watermarks, annotations, or background layers...")

watermark_findings = []

for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.lower().endswith('.pdf'):
            pdf_path = os.path.join(root, f)
            try:
                doc = fitz.open(pdf_path)
                for pno in range(len(doc)):
                    page = doc[pno]
                    
                    # 1. Check annotations
                    annots = list(page.annots())
                    if annots:
                        print(f"[Annot] {f} p{pno+1}: {len(annots)} annotations found")
                    
                    # 2. Check for text that might be a watermark (e.g. diagonal or low-opacity or common watermark strings)
                    td = page.get_text("dict")
                    for block in td.get("blocks", []):
                        if "lines" in block:
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    txt = span["text"].strip()
                                    txt_lower = txt.lower()
                                    if any(w in txt_lower for w in ["not to be republished", "republish", "watermark", "draft", "sample copy", "rationalised"]):
                                        watermark_findings.append({
                                            "file": f,
                                            "page": pno + 1,
                                            "text": txt,
                                            "bbox": span["bbox"],
                                            "font": span["font"],
                                            "size": span["size"],
                                            "color": span["color"],
                                            "flags": span["flags"]
                                        })
            except Exception as e:
                print(f"Error on {f}: {e}")

print(f"\nTotal potential watermark strings detected: {len(watermark_findings)}")
for wf in watermark_findings[:20]:
    print(wf)
