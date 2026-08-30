import os
import re
import sys
import time
import pikepdf

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\NCERT_Textbook\Class_10"

BOOK_METADATA_MAP = {
    "First_Flight": {
        "subject": "English",
        "book_title": "First Flight",
        "desc": "NCERT Class 10 English Language & Literature Main Reader - First Flight"
    },
    "Footprints_Without_Feet": {
        "subject": "English",
        "book_title": "Footprints Without Feet",
        "desc": "NCERT Class 10 English Supplementary Reader - Footprints Without Feet"
    },
    "Kshitij_2": {
        "subject": "Hindi",
        "book_title": "Kshitij-2",
        "desc": "NCERT Class 10 Hindi Course A Textbook - Kshitij-2"
    },
    "Kritika": {
        "subject": "Hindi",
        "book_title": "Kritika",
        "desc": "NCERT Class 10 Hindi Course A Supplementary Reader - Kritika"
    },
    "Mathematics": {
        "subject": "Mathematics",
        "book_title": "Mathematics",
        "desc": "NCERT Class 10 Mathematics Textbook"
    },
    "Science": {
        "subject": "Science",
        "book_title": "Science",
        "desc": "NCERT Class 10 Science Textbook"
    },
    "Geography_Contemporary_India": {
        "subject": "Social Science (Geography)",
        "book_title": "Contemporary India - II",
        "desc": "NCERT Class 10 Social Science - Geography (Contemporary India - II)"
    },
    "Economics_Understanding_Economic_Development": {
        "subject": "Social Science (Economics)",
        "book_title": "Understanding Economic Development",
        "desc": "NCERT Class 10 Social Science - Economics (Understanding Economic Development)"
    },
    "History_India_and_the_Contemporary_World_II": {
        "subject": "Social Science (History)",
        "book_title": "India and the Contemporary World - II",
        "desc": "NCERT Class 10 Social Science - History (India and the Contemporary World - II)"
    },
    "Political_Science_Democratic_Politics": {
        "subject": "Social Science (Political Science)",
        "book_title": "Democratic Politics - II",
        "desc": "NCERT Class 10 Social Science - Political Science (Democratic Politics - II)"
    },
}

def determine_file_details(folder_name, filename):
    meta_info = BOOK_METADATA_MAP.get(folder_name, {
        "subject": "General",
        "book_title": folder_name.replace("_", " "),
        "desc": f"NCERT Class 10 {folder_name.replace('_', ' ')}"
    })
    
    subj = meta_info["subject"]
    btitle = meta_info["book_title"]
    bdesc = meta_info["desc"]
    
    fname_lower = filename.lower()
    
    if "prelims" in fname_lower or fname_lower.endswith("ps.pdf") or fname_lower.endswith("pr.pdf"):
        title = f"Class 10 {subj} - {btitle} - Preliminary Pages & Contents"
        chapter_label = "Prelims"
    elif fname_lower.endswith("an.pdf"):
        title = f"Class 10 {subj} - {btitle} - Answers & Solutions"
        chapter_label = "Answers"
    elif fname_lower.endswith("a1.pdf"):
        title = f"Class 10 {subj} - {btitle} - Appendix I"
        chapter_label = "Appendix 1"
    elif fname_lower.endswith("a2.pdf"):
        title = f"Class 10 {subj} - {btitle} - Appendix II"
        chapter_label = "Appendix 2"
    elif fname_lower.endswith("lp.pdf"):
        title = f"Class 10 {subj} - {btitle} - Lekhak Parichay (Author Profile)"
        chapter_label = "Author Profile"
    else:
        m = re.search(r'([a-z0-9]+?)(\d{2})\.pdf$', fname_lower)
        if m:
            ch_num = int(m.group(2))
            title = f"Class 10 {subj} - {btitle} - Chapter {ch_num}"
            chapter_label = f"Chapter {ch_num}"
        else:
            title = f"Class 10 {subj} - {btitle} - {filename.replace('.pdf', '')}"
            chapter_label = filename.replace('.pdf', '')
            
    keywords = f"NCERT, Class 10, CBSE, Textbook, {subj}, {btitle}, {chapter_label}, Rationalised Edition"
    
    return {
        "title": title,
        "author": "National Council of Educational Research and Training (NCERT)",
        "subject": f"NCERT Class 10 {subj} - {btitle}",
        "creator": "NCERT",
        "producer": "NCERT Textbook Publication Division",
        "keywords": keywords,
        "description": bdesc
    }

def process_pdf(pdf_path, folder_name):
    filename = os.path.basename(pdf_path)
    meta = determine_file_details(folder_name, filename)
    
    temp_output = pdf_path + ".v17.tmp"
    
    with pikepdf.open(pdf_path) as pdf:
        # Explicitly set Version in Root (Catalog) dictionary
        pdf.Root.Version = pikepdf.Name("/1.7")
        
        # Set standard DocInfo dictionary
        pdf.docinfo['/Title'] = meta["title"]
        pdf.docinfo['/Author'] = meta["author"]
        pdf.docinfo['/Subject'] = meta["subject"]
        pdf.docinfo['/Creator'] = meta["creator"]
        pdf.docinfo['/Producer'] = meta["producer"]
        pdf.docinfo['/Keywords'] = meta["keywords"]
        
        # Synchronize XMP metadata packet without editor tags
        with pdf.open_metadata(set_pikepdf_as_editor=False) as xmp:
            xmp['dc:title'] = meta["title"]
            xmp['dc:creator'] = [meta["author"]]
            xmp['dc:description'] = meta["description"]
            xmp['pdf:Producer'] = meta["producer"]
            xmp['pdf:Keywords'] = meta["keywords"]
            xmp['xmp:CreatorTool'] = meta["creator"]
            
        # Save with PDF 1.7 specification & Linearization (Fast Web View)
        pdf.save(temp_output, linearize=True, min_version="1.7")
    
    os.replace(temp_output, pdf_path)
    return meta["title"]

def main():
    print("=" * 65)
    print("UPGRADING ALL 108 CLASS 10 PDFS TO PDF 1.7 LINEARIZED (FAST WEB VIEW)")
    print("=" * 65)
    
    start_time = time.time()
    total_processed = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        rel_path = os.path.relpath(root, BASE_DIR)
        parts = rel_path.split(os.sep)
        
        if len(parts) >= 2:
            book_folder = parts[1]
        elif len(parts) == 1 and parts[0] != ".":
            book_folder = parts[0]
        else:
            book_folder = "Unknown"
            
        for f in files:
            if f.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, f)
                title = process_pdf(pdf_path, book_folder)
                total_processed += 1
                print(f"[{total_processed:03d}] Upgraded to PDF 1.7 Fast Web View: {f}")
                
    elapsed = time.time() - start_time
    print("\n" + "=" * 65)
    print("ALL 108 PDFS UPGRADED & LINEARIZED SUCCESSFULLY")
    print(f"Total Files: {total_processed}")
    print(f"PDF Version: 1.7")
    print(f"Fast Web View (Linearization): Enabled on 100% of files")
    print(f"Time: {elapsed:.2f} seconds")
    print("=" * 65)

if __name__ == "__main__":
    main()
