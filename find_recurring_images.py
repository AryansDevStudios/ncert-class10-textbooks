import fitz
import os
import sys
import hashlib
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\NCERT_Textbook\Class_10"

image_hashes = defaultdict(lambda: {"count": 0, "dims": None, "locations": [], "files": set()})
dim_counts = defaultdict(lambda: {"count": 0, "files": set(), "samples": []})

print("Scanning all PDF pages for images and calculating image frequencies and dimensions...")

total_pdfs = 0
total_pages = 0
total_images_found = 0

for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.lower().endswith('.pdf'):
            pdf_path = os.path.join(root, f)
            total_pdfs += 1
            try:
                doc = fitz.open(pdf_path)
                total_pages += len(doc)
                for pno in range(len(doc)):
                    page = doc[pno]
                    p_rect = page.rect
                    img_list = page.get_images(full=True)
                    for img in img_list:
                        xref = img[0]
                        total_images_found += 1
                        try:
                            base_img = doc.extract_image(xref)
                            img_bytes = base_img["image"]
                            width = base_img["width"]
                            height = base_img["height"]
                            img_ext = base_img["ext"]
                            cs = base_img.get("colorspace", "unknown")
                            
                            # Calculate MD5 hash of image content
                            md5 = hashlib.md5(img_bytes).hexdigest()
                            
                            # Get image rect on page if possible
                            img_rects = page.get_image_rects(xref)
                            
                            dim_key = f"{width}x{height}"
                            dim_counts[dim_key]["count"] += 1
                            dim_counts[dim_key]["files"].add(f)
                            if len(dim_counts[dim_key]["samples"]) < 3:
                                dim_counts[dim_key]["samples"].append({
                                    "file": f,
                                    "page": pno + 1,
                                    "xref": xref,
                                    "rects": [list(r) for r in img_rects] if img_rects else [],
                                    "page_rect": list(p_rect)
                                })
                            
                            image_hashes[md5]["count"] += 1
                            image_hashes[md5]["dims"] = (width, height, img_ext, cs)
                            image_hashes[md5]["files"].add(f)
                            if len(image_hashes[md5]["locations"]) < 3:
                                image_hashes[md5]["locations"].append({
                                    "file": f,
                                    "page": pno + 1,
                                    "xref": xref,
                                    "rects": [list(r) for r in img_rects] if img_rects else [],
                                    "page_rect": list(p_rect)
                                })
                        except Exception as e:
                            pass
            except Exception as e:
                print(f"Error reading {f}: {e}")

print(f"\nScan Complete:")
print(f"Total PDFs Scanned: {total_pdfs}")
print(f"Total Pages Scanned: {total_pages}")
print(f"Total Image Instances: {total_images_found}")
print(f"Unique Image Dimensions: {len(dim_counts)}")
print(f"Unique Image Hashes: {len(image_hashes)}")

print("\n=======================================================")
print("TOP RECURRING IMAGE DIMENSIONS (Sorted by Frequency):")
print("=======================================================")
sorted_dims = sorted(dim_counts.items(), key=lambda x: x[1]["count"], reverse=True)
for dim_key, data in sorted_dims[:25]:
    print(f"Dimension: {dim_key} | Total Occurrences: {data['count']} across {len(data['files'])} PDF files")
    for s in data["samples"][:2]:
        print(f"   -> File: {s['file']}, Page: {s['page']}, Placement rects: {s['rects']}, Page size: {s['page_rect']}")

print("\n=======================================================")
print("TOP RECURRING IMAGE CONTENT HASHES:")
print("=======================================================")
sorted_hashes = sorted(image_hashes.items(), key=lambda x: x[1]["count"], reverse=True)
for md5, data in sorted_hashes[:25]:
    w, h, ext, cs = data["dims"]
    print(f"MD5: {md5} | Dims: {w}x{h} ({ext}, {cs}) | Total Occurrences: {data['count']} across {len(data['files'])} PDF files")
    for s in data["locations"][:2]:
        print(f"   -> File: {s['file']}, Page: {s['page']}, Placement: {s['rects']}")
