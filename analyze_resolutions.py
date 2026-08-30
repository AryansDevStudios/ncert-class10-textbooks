import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\NCERT_Textbook\Class_10"

page_sizes = {}
image_resolutions = []

for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.lower().endswith('.pdf'):
            pdf_path = os.path.join(root, f)
            doc = fitz.open(pdf_path)
            # Check first 3 pages
            for pno in range(min(3, len(doc))):
                page = doc[pno]
                rect = page.rect # in points (1/72 inch)
                w_pt, h_pt = rect.width, rect.height
                w_in, h_in = w_pt / 72.0, h_pt / 72.0
                w_mm, h_mm = w_in * 25.4, h_in * 25.4
                
                size_key = f"{w_in:.2f} x {h_in:.2f} in ({w_mm:.1f} x {h_mm:.1f} mm)"
                page_sizes[size_key] = page_sizes.get(size_key, 0) + 1
                
                # Check image resolutions (DPI inside page)
                for img_info in page.get_image_info(xrefs=True):
                    # bbox on page
                    bbox = img_info.get("bbox")
                    w_px = img_info.get("width")
                    h_px = img_info.get("height")
                    if bbox and w_px and h_px:
                        bw = bbox[2] - bbox[0] # width in points
                        bh = bbox[3] - bbox[1] # height in points
                        if bw > 10 and bh > 10:
                            dpi_x = (w_px / bw) * 72.0
                            dpi_y = (h_px / bh) * 72.0
                            image_resolutions.append({
                                "file": f,
                                "dim": f"{w_px}x{h_px}",
                                "dpi": f"{int(dpi_x)}x{int(dpi_y)} DPI"
                            })

print("=== PAGE SIZES ACROSS CLASS 10 TEXTBOOKS ===")
for sz, count in page_sizes.items():
    print(f"Page Size: {sz} (found on {count} pages)")

print("\n=== SAMPLE EMBEDDED IMAGE RESOLUTIONS & DPI ===")
for img in image_resolutions[:15]:
    print(f"Image: {img['dim']} | Rendered DPI: {img['dpi']} in {img['file']}")
