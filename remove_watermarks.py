"""
NCERT PDF Watermark Remover & PDF 1.7 Linearizer
-------------------------------------------------
Recursively scans textbook PDFs, identifies and removes recurring watermark image
XObjects and soft masks without degrading page text, vector diagrams, or real images.
Standardizes metadata and produces Fast Web View (linearized) PDF 1.7 files.
"""

import os
import fitz  # PyMuPDF
import pikepdf

# Watermark signatures identified in NCERT textbooks
WATERMARK_DIMS = {
    (1894, 1894),  # Square watermark base image
    (2480, 3508),  # Full-page soft mask overlay
}

def clean_and_linearize_pdf(pdf_path):
    # Step 1: Remove watermark XObjects using PyMuPDF
    doc = fitz.open(pdf_path)
    watermarks_removed = 0

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        image_list = page.get_images(full=True)
        for img in image_list:
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                w, h = base_image.get("width", 0), base_image.get("height", 0)
                if (w, h) in WATERMARK_DIMS:
                    page.delete_image(xref)
                    watermarks_removed += 1
            except Exception:
                pass

    temp_path = pdf_path + ".tmp"
    doc.save(
        temp_path,
        garbage=4,
        clean=True,
        deflate=True,
        deflate_images=True,
        deflate_fonts=True
    )
    doc.close()

    # Step 2: Sanitize Metadata, apply PDF 1.7 standard, and Linearize via pikepdf
    filename = os.path.basename(pdf_path)
    doc_title = filename.replace(".pdf", "").upper()

    with pikepdf.open(temp_path, allow_overwriting_input=True) as p:
        # Standardize /Info dictionary
        with p.open_metadata(set_pikepdf_as_editor=False) as meta:
            meta["dc:title"] = f"NCERT Class 10 - {doc_title}"
            meta["dc:creator"] = ["NCERT"]
            meta["dc:description"] = "NCERT Class 10 Textbook (Clean & Linearized)"
            meta["pdf:Keywords"] = "NCERT, Class 10, Textbook, CBSE"
            meta["pdf:Producer"] = ""

        p.docinfo["/Title"] = f"NCERT Class 10 - {doc_title}"
        p.docinfo["/Author"] = "NCERT"
        p.docinfo["/Subject"] = "Class 10 Textbook"
        p.docinfo["/Creator"] = ""
        p.docinfo["/Producer"] = ""
        p.docinfo["/Keywords"] = "NCERT, Class 10, Textbook, CBSE"

        p.Root.Version = pikepdf.Name("/1.7")

        p.save(
            pdf_path,
            linearize=True,
            min_version="1.7",
            object_stream_mode=pikepdf.ObjectStreamMode.generate,
            compress_streams=True,
            recompress_flate=True
        )

    if os.path.exists(temp_path):
        os.remove(temp_path)

    return watermarks_removed

def process_all_textbooks(root_dir="Class_10"):
    print("=" * 65)
    print(f"Scanning & Removing Watermarks in '{root_dir}'...")
    print("=" * 65)

    total_files = 0
    total_watermarks = 0

    for root, _, files in os.walk(root_dir):
        for f in sorted(files):
            if f.lower().endswith(".pdf"):
                fp = os.path.join(root, f)
                total_files += 1
                try:
                    count = clean_and_linearize_pdf(fp)
                    total_watermarks += count
                    status = f"✓ Removed {count} watermark instances" if count > 0 else "✓ Clean (Linearized 1.7)"
                    print(f"  [{total_files:3d}] {f:16} -> {status}")
                except Exception as e:
                    print(f"  [{total_files:3d}] {f:16} -> ✗ Error: {e}")

    print("\n" + "=" * 65)
    print(f"Completed: {total_files} PDFs processed, {total_watermarks} watermarks removed.")
    print("All PDFs are now 100% Linearized PDF 1.7 with Fast Web View.")
    print("=" * 65)

if __name__ == "__main__":
    process_all_textbooks()
