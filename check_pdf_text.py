import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

def analyze_pdf(pdf_path):
    print(f"\nAnalyzing: {pdf_path}")
    doc = fitz.open(pdf_path)
    for pno in range(len(doc)):
        page = doc[pno]
        # Check text lines
        for line in page.get_text("text").split('\n'):
            line_s = line.strip()
            # Watermark strings often have phrases like:
            if any(k in line_s.lower() for k in ["not to be", "republish", "rationalised 202", "watermark", "ncert"]):
                print(f"  Page {pno+1}: '{line_s}'")

analyze_pdf(r"d:\NCERT_Textbook\Class_10\Mathematics\Mathematics\chapters\jemh101.pdf")
analyze_pdf(r"d:\NCERT_Textbook\Class_10\Science\Science\chapters\jesc101.pdf")
analyze_pdf(r"d:\NCERT_Textbook\Class_10\English\First_Flight\chapters\jeff101.pdf")
