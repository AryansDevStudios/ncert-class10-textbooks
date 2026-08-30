import fitz
from PIL import Image
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"d:\NCERT_Textbook\Class_10\English\First_Flight\chapters\jeff101.pdf"
doc = fitz.open(pdf_path)

# Let's extract xref 470 (the 1894x1894 image) and its smask (xref 471)
base_img = doc.extract_image(470)
smask_img = doc.extract_image(471)

print("Base img (470):", base_img["width"], base_img["height"], base_img["ext"], len(base_img["image"]))
print("SMask img (471):", smask_img["width"], smask_img["height"], smask_img["ext"], len(smask_img["image"]))

with open("watermark_base_470.png", "wb") as f:
    f.write(base_img["image"])

with open("watermark_smask_471.png", "wb") as f:
    f.write(smask_img["image"])

print("Saved watermark_base_470.png and watermark_smask_471.png")
