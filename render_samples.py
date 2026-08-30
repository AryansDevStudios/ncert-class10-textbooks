import fitz
import os

sample_pdfs = [
    (r"d:\NCERT_Textbook\Class_10\Mathematics\Mathematics\chapters\jemh101.pdf", "math_p1.png"),
    (r"d:\NCERT_Textbook\Class_10\English\First_Flight\chapters\jeff101.pdf", "eng_p1.png"),
    (r"d:\NCERT_Textbook\Class_10\Science\Science\chapters\jesc101.pdf", "sci_p1.png"),
    (r"d:\NCERT_Textbook\Class_10\Hindi\Kshitij_2\chapters\jhks101.pdf", "hindi_p1.png"),
]

for pdf_path, out_img in sample_pdfs:
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap(dpi=150)
    pix.save(out_img)
    print(f"Rendered {pdf_path} page 1 -> {out_img} ({os.path.getsize(out_img)} bytes)")
