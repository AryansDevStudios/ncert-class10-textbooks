import os
import sys
import pikepdf
import fitz

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\NCERT_Textbook\Class_10"

print("Analyzing lossless optimization opportunities across all Class 10 PDFs...")

sample_files = [
    r"d:\NCERT_Textbook\Class_10\Mathematics\Mathematics\chapters\jemh105.pdf",
    r"d:\NCERT_Textbook\Class_10\Science\Science\chapters\jesc101.pdf",
    r"d:\NCERT_Textbook\Class_10\English\First_Flight\chapters\jeff101.pdf",
    r"d:\NCERT_Textbook\Class_10\Hindi\Kshitij_2\chapters\jhks101.pdf",
    r"d:\NCERT_Textbook\Class_10\Social_Science\History_India_and_the_Contemporary_World_II\chapters\jess301.pdf"
]

total_orig_sample_size = 0
total_opt_sample_size = 0

print("\n--- Testing Lossless Optimization on Sample Chapters ---")
for fpath in sample_files:
    fname = os.path.basename(fpath)
    orig_size = os.path.getsize(fpath)
    total_orig_sample_size += orig_size
    
    out_opt = f"opt_{fname}"
    
    # 1. Using pikepdf with Object Streams and Stream Compression
    with pikepdf.open(fpath) as pdf:
        # Check streams
        pdf.save(
            out_opt,
            linearize=True,
            min_version="1.7",
            compress_streams=True,
            object_stream_mode=pikepdf.ObjectStreamMode.generate,
            recompress_flate=True
        )
    
    opt_size = os.path.getsize(out_opt)
    total_opt_sample_size += opt_size
    saved_kb = (orig_size - opt_size) / 1024
    pct = (1 - (opt_size / orig_size)) * 100
    
    print(f"{fname}: {orig_size/1024:.1f} KB -> {opt_size/1024:.1f} KB (Saved: {saved_kb:.1f} KB | {pct:.1f}%)")

print(f"\nSample Total: {total_orig_sample_size/1024:.1f} KB -> {total_opt_sample_size/1024:.1f} KB")
print(f"Sample Savings: {(1 - total_opt_sample_size/total_orig_sample_size)*100:.1f}%")
