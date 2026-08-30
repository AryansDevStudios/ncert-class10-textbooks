import os
import sys
import pikepdf

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\NCERT_Textbook\Class_10"

total_file_size = 0
total_images_size = 0
total_fonts_size = 0
total_streams_size = 0

file_count = 0

for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.lower().endswith('.pdf'):
            file_count += 1
            fpath = os.path.join(root, f)
            sz = os.path.getsize(fpath)
            total_file_size += sz
            
            with pikepdf.open(fpath) as pdf:
                for obj in pdf.objects:
                    if isinstance(obj, pikepdf.Stream):
                        try:
                            stream_len = len(obj.read_raw_bytes())
                            subtype = str(obj.get("/Subtype", ""))
                            obj_type = str(obj.get("/Type", ""))
                            
                            if subtype == "/Image":
                                total_images_size += stream_len
                            elif "/Font" in obj_type or "/Font" in subtype or "Type1" in subtype or "CID" in subtype:
                                total_fonts_size += stream_len
                            else:
                                total_streams_size += stream_len
                        except Exception:
                            pass

print(f"Total PDFs Analyzed: {file_count}")
print(f"Total File Size on Disk: {total_file_size / (1024*1024):.2f} MB")
print(f"Images Streams: {total_images_size / (1024*1024):.2f} MB ({total_images_size / total_file_size * 100:.1f}%)")
print(f"Fonts Streams: {total_fonts_size / (1024*1024):.2f} MB ({total_fonts_size / total_file_size * 100:.1f}%)")
print(f"Content / Vector Streams: {total_streams_size / (1024*1024):.2f} MB ({total_streams_size / total_file_size * 100:.1f}%)")
other_size = total_file_size - (total_images_size + total_fonts_size + total_streams_size)
print(f"Structural Overhead / XRef: {other_size / (1024*1024):.2f} MB ({other_size / total_file_size * 100:.1f}%)")
