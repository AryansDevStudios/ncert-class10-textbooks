"""
NCERT Class 10 Textbook Fetcher
---------------------------------
Downloads official NCERT Class 10 textbook ZIP archives directly from NCERT portal,
extracts all chapter PDFs, table of contents (prelims), answers, appendices,
and cover artwork into organized directory structures.
"""

import os
import zipfile
import urllib.request
import time
import json

TARGET_BOOKS = [
    # Hindi
    {
        "id": "Kshitij_2",
        "category": "Hindi",
        "title": "Kshitij 2",
        "code": "jhks1",
        "num_chapters": 12,
        "folder": os.path.join("Class_10", "Hindi", "Kshitij_2")
    },
    {
        "id": "Kritika",
        "category": "Hindi",
        "title": "Kritika",
        "code": "jhkr1",
        "num_chapters": 3,
        "folder": os.path.join("Class_10", "Hindi", "Kritika")
    },
    # English
    {
        "id": "First_Flight",
        "category": "English",
        "title": "First Flight",
        "code": "jeff1",
        "num_chapters": 9,
        "folder": os.path.join("Class_10", "English", "First_Flight")
    },
    {
        "id": "Footprints_Without_Feet",
        "category": "English",
        "title": "Footprints Without Feet",
        "code": "jefp1",
        "num_chapters": 9,
        "folder": os.path.join("Class_10", "English", "Footprints_Without_Feet")
    },
    # Mathematics
    {
        "id": "Mathematics",
        "category": "Mathematics",
        "title": "Mathematics",
        "code": "jemh1",
        "num_chapters": 14,
        "folder": os.path.join("Class_10", "Mathematics", "Mathematics")
    },
    # Science
    {
        "id": "Science",
        "category": "Science",
        "title": "Science",
        "code": "jesc1",
        "num_chapters": 13,
        "folder": os.path.join("Class_10", "Science", "Science")
    },
    # Social Science (SST)
    {
        "id": "Geography_Contemporary_India",
        "category": "Social_Science",
        "title": "Geography — Contemporary India II",
        "code": "jess1",
        "num_chapters": 7,
        "folder": os.path.join("Class_10", "Social_Science", "Geography_Contemporary_India")
    },
    {
        "id": "Economics_Understanding_Economic_Development",
        "category": "Social_Science",
        "title": "Economics — Understanding Economic Development",
        "code": "jess2",
        "num_chapters": 5,
        "folder": os.path.join("Class_10", "Social_Science", "Economics_Understanding_Economic_Development")
    },
    {
        "id": "History_India_and_the_Contemporary_World_II",
        "category": "Social_Science",
        "title": "History — India and the Contemporary World II",
        "code": "jess3",
        "num_chapters": 5,
        "folder": os.path.join("Class_10", "Social_Science", "History_India_and_the_Contemporary_World_II")
    },
    {
        "id": "Political_Science_Democratic_Politics",
        "category": "Social_Science",
        "title": "Political Science — Democratic Politics II",
        "code": "jess4",
        "num_chapters": 5,
        "folder": os.path.join("Class_10", "Social_Science", "Political_Science_Democratic_Politics")
    },
    # Information Technology (Subject Code 402)
    {
        "id": "Domestic_Data_Entry_Operator",
        "category": "Information_Technology",
        "title": "Domestic Data Entry Operator (Part B)",
        "code": "jhde1",
        "num_chapters": 4,
        "zip_url": "https://ncert.nic.in/vocational/pdf/jhde1dd.zip",
        "folder": os.path.join("Class_10", "Information_Technology", "Domestic_Data_Entry_Operator")
    },
    {
        "id": "Employability_Skills",
        "category": "Information_Technology",
        "title": "Employability Skills (Part A)",
        "code": "jees1",
        "num_chapters": 5,
        "zip_url": "https://ncert.nic.in/vocational/pdf/jees1dd.zip",
        "folder": os.path.join("Class_10", "Information_Technology", "Employability_Skills")
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://ncert.nic.in/textbook.php"
}

def download_file(url, target_path):
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    try:
        import subprocess
        cmd = ["curl.exe", "-4", "-fSL", "-A", HEADERS["User-Agent"], "-e", "https://ncert.nic.in/vocational.php", "-o", target_path, url]
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode == 0:
            return
    except Exception:
        pass
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp, open(target_path, "wb") as f:
        f.write(resp.read())

def fetch_all_textbooks():
    print("=" * 65)
    print("Fetching NCERT Class 10 Textbooks...")
    print("=" * 65)

    for b in TARGET_BOOKS:
        code = b["code"]
        folder = b["folder"]
        chapters_dir = os.path.join(folder, "chapters")
        os.makedirs(chapters_dir, exist_ok=True)

        zip_filename = f"{code}_complete.zip"
        zip_path = os.path.join(folder, zip_filename)
        zip_url = b.get("zip_url", f"https://ncert.nic.in/textbook/pdf/{code}dd.zip")

        print(f"\n[Book] {b['title']} ({code})")
        if not os.path.exists(zip_path):
            print(f"  Downloading full ZIP archive from {zip_url}...")
            try:
                download_file(zip_url, zip_path)
                print(f"  ✓ Downloaded {zip_filename} ({os.path.getsize(zip_path) / (1024*1024):.2f} MB)")
            except Exception as e:
                print(f"  ✗ Failed to download ZIP: {e}")
                continue
        else:
            print(f"  ✓ ZIP archive already present ({os.path.getsize(zip_path) / (1024*1024):.2f} MB)")

        # Extract ZIP contents
        print("  Extracting chapters and assets...")
        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                for item in z.infolist():
                    fn = os.path.basename(item.filename)
                    if not fn:
                        continue
                    lower_fn = fn.lower()
                    
                    # Extract to chapters directory
                    out_path = os.path.join(chapters_dir, fn)
                    with z.open(item) as src, open(out_path, "wb") as dst:
                        dst.write(src.read())

                    # Copy cover & prelims to book root for quick reference
                    if lower_fn.endswith(".jpg") or lower_fn.endswith("cc.jpg"):
                        root_cover = os.path.join(folder, "cover.jpg")
                        with open(out_path, "rb") as src, open(root_cover, "wb") as dst:
                            dst.write(src.read())
                    elif lower_fn.endswith("ps.pdf"):
                        root_ps = os.path.join(folder, "prelims.pdf")
                        with open(out_path, "rb") as src, open(root_ps, "wb") as dst:
                            dst.write(src.read())

            extracted_files = os.listdir(chapters_dir)
            print(f"  ✓ Extracted {len(extracted_files)} files into {chapters_dir}")
        except Exception as e:
            print(f"  ✗ Extraction error: {e}")

    print("\n" + "=" * 65)
    print("All Class 10 NCERT Textbooks downloaded and organized.")
    print("=" * 65)

if __name__ == "__main__":
    fetch_all_textbooks()
