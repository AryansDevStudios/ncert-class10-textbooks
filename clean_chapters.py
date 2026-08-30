import os
import shutil

BASE_DIR = r"d:\NCERT_Textbook\Class_10"

for root, dirs, files in os.walk(BASE_DIR):
    if os.path.basename(root) == "chapters":
        # Check if there are subdirectories inside chapters
        for d in list(dirs):
            sub_dir = os.path.join(root, d)
            for sub_f in os.listdir(sub_dir):
                src = os.path.join(sub_dir, sub_f)
                dst = os.path.join(root, sub_f)
                if not os.path.exists(dst):
                    shutil.move(src, dst)
                elif os.path.getsize(src) > os.path.getsize(dst):
                    os.remove(dst)
                    shutil.move(src, dst)
            shutil.rmtree(sub_dir, ignore_errors=True)

print("Chapters directories cleaned and flattened successfully!")
