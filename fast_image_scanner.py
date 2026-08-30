import fitz
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\NCERT_Textbook\Class_10"

dim_counts = defaultdict(lambda: {"count": 0, "files": set(), "pages": []})

total_pdfs = 0
total_pages = 0
total_images = 0

for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.lower().endswith('.pdf'):
            pdf_path = os.path.join(root, f)
            total_pdfs += 1
            try:
                doc = fitz.open(pdf_path)
                total_pages += len(doc)
                for pno, page in enumerate(doc):
                    imgs = page.get_images()
                    for img in imgs:
                        # img is tuple: (xref, smask, width, height, bpc, colorspace, ...)
                        xref, smask, width, height = img[0], img[1], img[2], img[3]
                        total_images += 1
                        dim_key = f"{width}x{height}"
                        dim_counts[dim_key]["count"] += 1
                        dim_counts[dim_key]["files"].add(f)
                        if len(dim_counts[dim_key]["pages"]) < 5:
                            dim_counts[dim_key]["pages"].append((f, pno + 1, xref))
            except Exception as e:
                print(f"Error on {f}: {e}")

print(f"Scanned {total_pdfs} PDFs, {total_pages} Pages, {total_images} Total Images.")
print(f"Unique dimensions found: {len(dim_counts)}")

print("\n=== TOP 20 MOST RECURRING IMAGE DIMENSIONS ===")
sorted_dims = sorted(dim_counts.items(), key=lambda x: x[1]["count"], reverse=True)
for dim_key, data in sorted_dims[:20]:
    print(f"\nDimensions: {dim_key} | Occurrences: {data['count']} across {len(data['files'])} PDF files")
    for fname, pno, xref in data["pages"][:3]:
        print(f"   Sample: {fname} -> Page {pno} (xref: {xref})")

# Also let's inspect the top 3 recurring images in detail: extract their image bytes and save them to disk
print("\n=== Extracting Top Recurring Images to Disk for Visual Inspection ===")
for i, (dim_key, data) in enumerate(sorted_dims[:5]):
    fname, pno, xref = data["pages"][0]
    # find file path
    for root, dirs, files in os.walk(BASE_DIR):
        if fname in files:
            doc = fitz.open(os.path.join(root, fname))
            base_img = doc.extract_image(xref)
            ext = base_img["ext"]
            out_name = f"recurring_img_{i+1}_{dim_key}.{ext}"
            with open(out_name, "wb") as img_f:
                img_f.write(base_img["image"])
            print(f"Saved Top #{i+1} ({dim_key}, count={data['count']}) to {out_name} (format: {ext}, size: {len(base_img['image'])} bytes)")
            break
