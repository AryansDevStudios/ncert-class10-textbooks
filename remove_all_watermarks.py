import fitz
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\NCERT_Textbook\Class_10"

# Target watermark image dimensions discovered across NCERT textbooks:
# 1. (1894, 1894): The centered square watermark image present on almost every page.
# 2. (2480, 3508): The full-page background watermark/mask overlay.
WATERMARK_DIMS = {
    (1894, 1894),
    (2480, 3508)
}

def remove_watermarks_from_pdf(pdf_path, in_place=True):
    try:
        doc = fitz.open(pdf_path)
        modified = False
        removed_count = 0
        
        for pno, page in enumerate(doc):
            imgs = page.get_images()
            for img in imgs:
                xref = img[0]
                width = img[2]
                height = img[3]
                
                # If image matches the watermark signature
                if (width, height) in WATERMARK_DIMS:
                    try:
                        page.delete_image(xref)
                        removed_count += 1
                        modified = True
                    except Exception as e:
                        pass
        
        if modified and removed_count > 0:
            temp_path = pdf_path + ".tmp"
            doc.save(temp_path, garbage=4, deflate=True)
            doc.close()
            if in_place:
                os.replace(temp_path, pdf_path)
            return removed_count, True
        else:
            doc.close()
            return 0, False
    except Exception as e:
        return 0, False

def batch_process_all_pdfs(directory):
    print(f"Starting batch watermark removal across: {directory}")
    start_time = time.time()
    
    total_processed = 0
    total_watermarks_removed = 0
    modified_files = 0
    
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, f)
                total_processed += 1
                count, was_mod = remove_watermarks_from_pdf(pdf_path, in_place=True)
                if was_mod:
                    modified_files += 1
                    total_watermarks_removed += count
                    print(f"  [CLEANED] {f}: removed {count} watermark image(s)")
                else:
                    print(f"  [CLEAN]   {f}: no watermark found / already clean")

    elapsed = time.time() - start_time
    print("\n=======================================================")
    print("BATCH WATERMARK REMOVAL COMPLETE")
    print(f"Total PDFs Checked: {total_processed}")
    print(f"PDFs Cleaned: {modified_files}")
    print(f"Total Watermark Instances Deleted: {total_watermarks_removed}")
    print(f"Time Elapsed: {elapsed:.2f} seconds")
    print("=======================================================")

if __name__ == "__main__":
    batch_process_all_pdfs(BASE_DIR)
