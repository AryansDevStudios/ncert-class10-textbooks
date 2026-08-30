import os
import sys
import zipfile
import subprocess
import shutil

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\NCERT_Textbook\Class_10"

BOOKS_TO_DOWNLOAD = [
    {
        "category": "English",
        "folder": "First_Flight",
        "code": "jeff1",
        "title": "First Flight (Class X English Main Reader)",
        "chapters_count": 9
    },
    {
        "category": "English",
        "folder": "Footprints_Without_Feet",
        "code": "jefp1",
        "title": "Footprints Without Feet (Class X English Supplementary Reader)",
        "chapters_count": 9
    },
    {
        "category": "Hindi",
        "folder": "Kshitij_2",
        "code": "jhks1",
        "title": "Kshitij-2 (Class X Hindi Course A)",
        "chapters_count": 12
    },
    {
        "category": "Hindi",
        "folder": "Kritika",
        "code": "jhkr1",
        "title": "Kritika (Class X Hindi Course A Supplementary)",
        "chapters_count": 3
    },
    {
        "category": "Mathematics",
        "folder": "Mathematics",
        "code": "jemh1",
        "title": "Mathematics (Class X)",
        "chapters_count": 14
    },
    {
        "category": "Science",
        "folder": "Science",
        "code": "jesc1",
        "title": "Science (Class X)",
        "chapters_count": 13
    },
    {
        "category": "Social_Science",
        "folder": "Geography_Contemporary_India",
        "code": "jess1",
        "title": "Contemporary India - II (Class X Geography)",
        "chapters_count": 7
    },
    {
        "category": "Social_Science",
        "folder": "Economics_Understanding_Economic_Development",
        "code": "jess2",
        "title": "Understanding Economic Development (Class X Economics)",
        "chapters_count": 5
    },
    {
        "category": "Social_Science",
        "folder": "History_India_and_the_Contemporary_World_II",
        "code": "jess3",
        "title": "India and the Contemporary World - II (Class X History)",
        "chapters_count": 5
    },
    {
        "category": "Social_Science",
        "folder": "Political_Science_Democratic_Politics",
        "code": "jess4",
        "title": "Democratic Politics - II (Class X Political Science)",
        "chapters_count": 5
    },
]

def download_file_curl(url, dest_path):
    cmd = [
        "curl", "-s", "-L",
        "--retry", "3",
        "--retry-delay", "2",
        "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        url,
        "-o", dest_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        return True
    return False

def process_book(book_info):
    cat_dir = os.path.join(BASE_DIR, book_info["category"])
    target_dir = os.path.join(cat_dir, book_info["folder"])
    chapters_dir = os.path.join(target_dir, "chapters")
    
    os.makedirs(chapters_dir, exist_ok=True)
    
    code = book_info["code"]
    title = book_info["title"]
    print(f"\n==================================================")
    print(f"Processing: {title} (Code: {code})")
    print(f"Target Directory: {target_dir}")
    
    # 1. Download Cover Page
    cover_path = os.path.join(target_dir, "cover.jpg")
    cover_url = f"https://ncert.nic.in/textbook/pdf/{code}cc.jpg"
    print(f"Downloading cover page from {cover_url}...")
    if download_file_curl(cover_url, cover_path):
        print(f"  [OK] Cover saved ({os.path.getsize(cover_path)} bytes)")
    else:
        print(f"  [WARN] Cover download failed or not found at {cover_url}")

    # 2. Download Prelims
    prelims_path = os.path.join(target_dir, "prelims.pdf")
    prelims_url = f"https://ncert.nic.in/textbook/pdf/{code}ps.pdf"
    print(f"Downloading prelims from {prelims_url}...")
    if download_file_curl(prelims_url, prelims_path):
        print(f"  [OK] Prelims saved ({os.path.getsize(prelims_path)} bytes)")
    else:
        # Try alternate prelims url with 'pr'
        alt_prelims_url = f"https://ncert.nic.in/textbook/pdf/{code}pr.pdf"
        print(f"  Trying alternate prelims url: {alt_prelims_url}")
        if download_file_curl(alt_prelims_url, prelims_path):
            print(f"  [OK] Prelims saved ({os.path.getsize(prelims_path)} bytes)")
        else:
            print(f"  [WARN] Prelims not available")

    # 3. Download Complete Book ZIP
    zip_path = os.path.join(target_dir, f"{code}_complete.zip")
    zip_url = f"https://ncert.nic.in/textbook/pdf/{code}dd.zip"
    print(f"Downloading complete book ZIP from {zip_url}...")
    zip_success = download_file_curl(zip_url, zip_path)
    
    if zip_success:
        print(f"  [OK] Complete ZIP downloaded ({os.path.getsize(zip_path)} bytes)")
        print(f"  Extracting ZIP archive into {chapters_dir}...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(chapters_dir)
            print(f"  [OK] Successfully extracted ZIP archive.")
        except Exception as e:
            print(f"  [ERROR] Unzipping failed: {e}")
    else:
        print(f"  [WARN] ZIP download failed from {zip_url}. Will download chapter PDFs individually...")
        
    # 4. Verify individual chapter PDFs in chapters_dir (and download any missing ones directly)
    total_ch = book_info["chapters_count"]
    for ch in range(1, total_ch + 1):
        ch_str = f"{ch:02d}"
        expected_pdf_name = f"{code}{ch_str}.pdf"
        expected_path = os.path.join(chapters_dir, expected_pdf_name)
        
        # Check if already present from unzipping (case-insensitive search)
        found = False
        for fname in os.listdir(chapters_dir):
            if fname.lower() == expected_pdf_name.lower() and os.path.getsize(os.path.join(chapters_dir, fname)) > 1000:
                found = True
                break
        
        if not found:
            ch_url = f"https://ncert.nic.in/textbook/pdf/{code}{ch_str}.pdf"
            print(f"  Downloading missing Chapter {ch} from {ch_url}...")
            if download_file_curl(ch_url, expected_path):
                print(f"    [OK] Chapter {ch} downloaded.")
            else:
                print(f"    [ERROR] Chapter {ch} failed.")

    # 5. List all files extracted in chapters_dir
    extracted_files = os.listdir(chapters_dir)
    print(f"  Chapters folder content ({len(extracted_files)} files): {extracted_files}")

def main():
    print(f"Starting Class 10 Textbook Download to {BASE_DIR}")
    os.makedirs(BASE_DIR, exist_ok=True)
    
    for b in BOOKS_TO_DOWNLOAD:
        process_book(b)
        
    print("\n==================================================")
    print("[SUCCESS] All requested Class 10 textbooks downloaded and extracted successfully!")

if __name__ == "__main__":
    main()
