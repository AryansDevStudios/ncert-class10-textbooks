"""
NCERT Web Catalog & Manifest Generator
---------------------------------------
Scans Class_10 directory, extracts page counts, chapter metadata, and file sizes,
and produces web_data.json used by index.html for interactive navigation.
"""

import os
import json
import fitz  # PyMuPDF

# Authentic chapter title mapping
CHAPTER_TITLES = {
    # Mathematics (jemh1)
    "jemh1ps.pdf": "Preliminary Pages & Table of Contents",
    "jemh101.pdf": "Real Numbers",
    "jemh102.pdf": "Polynomials",
    "jemh103.pdf": "Pair of Linear Equations in Two Variables",
    "jemh104.pdf": "Quadratic Equations",
    "jemh105.pdf": "Arithmetic Progressions",
    "jemh106.pdf": "Triangles",
    "jemh107.pdf": "Coordinate Geometry",
    "jemh108.pdf": "Introduction to Trigonometry",
    "jemh109.pdf": "Some Applications of Trigonometry",
    "jemh110.pdf": "Circles",
    "jemh111.pdf": "Areas Related to Circles",
    "jemh112.pdf": "Surface Areas and Volumes",
    "jemh113.pdf": "Statistics",
    "jemh114.pdf": "Probability",
    "jemh1a1.pdf": "Appendix I: Proofs in Mathematics",
    "jemh1a2.pdf": "Appendix II: Mathematical Modelling",
    "jemh1an.pdf": "Answers & Solutions",

    # Science (jesc1)
    "jesc1ps.pdf": "Preliminary Pages & Table of Contents",
    "jesc101.pdf": "Chemical Reactions and Equations",
    "jesc102.pdf": "Acids, Bases and Salts",
    "jesc103.pdf": "Metals and Non-metals",
    "jesc104.pdf": "Carbon and its Compounds",
    "jesc105.pdf": "Life Processes",
    "jesc106.pdf": "Control and Coordination",
    "jesc107.pdf": "How do Organisms Reproduce?",
    "jesc108.pdf": "Heredity and Evolution",
    "jesc109.pdf": "Light – Reflection and Refraction",
    "jesc110.pdf": "The Human Eye and the Colourful World",
    "jesc111.pdf": "Electricity",
    "jesc112.pdf": "Magnetic Effects of Electric Current",
    "jesc113.pdf": "Our Environment",
    "jesc1an.pdf": "Answers & Solutions",

    # English: First Flight (jeff1)
    "jeff1ps.pdf": "Preliminary Pages & Table of Contents",
    "jeff101.pdf": "A Letter to God & Poems",
    "jeff102.pdf": "Nelson Mandela: Long Walk to Freedom",
    "jeff103.pdf": "Two Stories about Flying",
    "jeff104.pdf": "From the Diary of Anne Frank",
    "jeff105.pdf": "Glimpses of India",
    "jeff106.pdf": "Mijbil the Otter",
    "jeff107.pdf": "Madam Rides the Bus",
    "jeff108.pdf": "The Sermon at Benares",
    "jeff109.pdf": "The Proposal",

    # English: Footprints Without Feet (jefp1)
    "jefp1ps.pdf": "Preliminary Pages & Table of Contents",
    "jefp101.pdf": "A Triumph of Surgery",
    "jefp102.pdf": "The Thief's Story",
    "jefp103.pdf": "The Midnight Visitor",
    "jefp104.pdf": "A Question of Trust",
    "jefp105.pdf": "Footprints without Feet",
    "jefp106.pdf": "The Making of a Scientist",
    "jefp107.pdf": "The Necklace",
    "jefp108.pdf": "Bholi",
    "jefp109.pdf": "The Book That Saved the Earth",

    # Hindi: Kshitij 2 (jhks1)
    "jhks1ps.pdf": "Preliminary Pages & Table of Contents",
    "jhks101.pdf": "Pad (Surdas)",
    "jhks102.pdf": "Ram-Lakshman-Parashuram Samvad",
    "jhks103.pdf": "Aatmakathya (Jaishankar Prasad)",
    "jhks104.pdf": "Utsah & At Nahi Rahi Hai",
    "jhks105.pdf": "Yeh Danturit Muskan & Fasal",
    "jhks106.pdf": "Sangatkar (Manglesh Dabral)",
    "jhks107.pdf": "Netaji Ka Chashma (Swayam Prakash)",
    "jhks108.pdf": "Balgobin Bhagat (Ramvriksh Benipuri)",
    "jhks109.pdf": "Lakhnavi Andaz (Yashpal)",
    "jhks110.pdf": "Ek Kahani Yeh Bhi (Mannu Bhandari)",
    "jhks111.pdf": "Naubatkhane Mein Ibadat",
    "jhks112.pdf": "Sanskriti (Bhadant Anand Kausalyayan)",

    # Hindi: Kritika (jhkr1)
    "jhkr1ps.pdf": "Preliminary Pages & Table of Contents",
    "jhkr101.pdf": "Mata Ka Aanchal (Shivpujan Sahay)",
    "jhkr102.pdf": "Sana-Sana Hath Jodi... (Madhu Kankariya)",
    "jhkr103.pdf": "Main Kyon Likhta Hoon? (Agyeya)",
    "jhkr1lp.pdf": "Lekhak Parichay (About the Authors)",

    # Social Science: Geography (jess1)
    "jess1ps.pdf": "Preliminary Pages & Table of Contents",
    "jess101.pdf": "Resources and Development",
    "jess102.pdf": "Forest and Wildlife Resources",
    "jess103.pdf": "Water Resources",
    "jess104.pdf": "Agriculture",
    "jess105.pdf": "Minerals and Energy Resources",
    "jess106.pdf": "Manufacturing Industries",
    "jess107.pdf": "Lifelines of National Economy",
    "jess1a1.pdf": "Appendix & Guidelines",

    # Social Science: Economics (jess2)
    "jess2ps.pdf": "Preliminary Pages & Table of Contents",
    "jess201.pdf": "Development",
    "jess202.pdf": "Sectors of the Indian Economy",
    "jess203.pdf": "Money and Credit",
    "jess204.pdf": "Globalization and the Indian Economy",
    "jess205.pdf": "Consumer Rights",

    # Social Science: History (jess3)
    "jess3ps.pdf": "Preliminary Pages & Table of Contents",
    "jess301.pdf": "The Rise of Nationalism in Europe",
    "jess302.pdf": "Nationalism in India",
    "jess303.pdf": "The Making of a Global World",
    "jess304.pdf": "The Age of Industrialisation",
    "jess305.pdf": "Print Culture and the Modern World",

    # Social Science: Political Science (jess4)
    "jess4ps.pdf": "Preliminary Pages & Table of Contents",
    "jess401.pdf": "Power-sharing",
    "jess402.pdf": "Federalism",
    "jess403.pdf": "Gender, Religion and Caste",
    "jess404.pdf": "Political Parties",
    "jess405.pdf": "Outcomes of Democracy",
}

BOOKS_CONFIG = [
    {"id": "Kshitij_2", "category": "Hindi", "title": "Kshitij 2", "code": "jhks1", "dir": "Class_10/Hindi/Kshitij_2"},
    {"id": "Kritika", "category": "Hindi", "title": "Kritika", "code": "jhkr1", "dir": "Class_10/Hindi/Kritika"},
    {"id": "First_Flight", "category": "English", "title": "First Flight", "code": "jeff1", "dir": "Class_10/English/First_Flight"},
    {"id": "Footprints_Without_Feet", "category": "English", "title": "Footprints Without Feet", "code": "jefp1", "dir": "Class_10/English/Footprints_Without_Feet"},
    {"id": "Mathematics", "category": "Mathematics", "title": "Mathematics", "code": "jemh1", "dir": "Class_10/Mathematics/Mathematics"},
    {"id": "Science", "category": "Science", "title": "Science", "code": "jesc1", "dir": "Class_10/Science/Science"},
    {"id": "Geography_Contemporary_India", "category": "Social_Science", "title": "Contemporary India – II (Geography)", "code": "jess1", "dir": "Class_10/Social_Science/Geography_Contemporary_India"},
    {"id": "Economics_Understanding_Economic_Development", "category": "Social_Science", "title": "Understanding Economic Development (Economics)", "code": "jess2", "dir": "Class_10/Social_Science/Economics_Understanding_Economic_Development"},
    {"id": "History_India_and_the_Contemporary_World_II", "category": "Social_Science", "title": "India and the Contemporary World – II (History)", "code": "jess3", "dir": "Class_10/Social_Science/History_India_and_the_Contemporary_World_II"},
    {"id": "Political_Science_Democratic_Politics", "category": "Social_Science", "title": "Democratic Politics – II (Political Science)", "code": "jess4", "dir": "Class_10/Social_Science/Political_Science_Democratic_Politics"},
]

def format_size(bytes_sz):
    if bytes_sz < 1024 * 1024:
        return f"{bytes_sz / 1024:.1f} KB"
    return f"{bytes_sz / (1024 * 1024):.2f} MB"

def build_manifest():
    manifest = []
    total_chapters_all = 0

    for cfg in BOOKS_CONFIG:
        book_dir = cfg["dir"]
        chapters_dir = os.path.join(book_dir, "chapters")
        
        cover_path = os.path.join(book_dir, "cover.jpg")
        cover_url = f"{book_dir}/cover.jpg" if os.path.exists(cover_path) else None

        zip_path = os.path.join(book_dir, f"{cfg['code']}_complete.zip")
        zip_url = f"{book_dir}/{cfg['code']}_complete.zip" if os.path.exists(zip_path) else None

        chapters_list = []
        if os.path.exists(chapters_dir):
            for f in sorted(os.listdir(chapters_dir)):
                if f.lower().endswith(".pdf"):
                    fp = os.path.join(chapters_dir, f)
                    sz = os.path.getsize(fp)
                    
                    # Page count
                    pages = 0
                    try:
                        doc = fitz.open(fp)
                        pages = len(doc)
                        doc.close()
                    except Exception:
                        pass

                    # Chapter type
                    lower_f = f.lower()
                    ch_type = "chapter"
                    if "ps" in lower_f:
                        ch_type = "prelims"
                    elif "an" in lower_f:
                        ch_type = "answers"
                    elif "a1" in lower_f or "a2" in lower_f:
                        ch_type = "appendix"
                    elif "lp" in lower_f:
                        ch_type = "intro"

                    title = CHAPTER_TITLES.get(f, f.replace(".pdf", "").replace("_", " ").title())

                    chapters_list.append({
                        "filename": f,
                        "title": title,
                        "type": ch_type,
                        "pages": pages,
                        "size_bytes": sz,
                        "size_formatted": format_size(sz),
                        "url": f"{chapters_dir}/{f}".replace("\\", "/")
                    })

        total_chapters_all += len(chapters_list)
        manifest.append({
            "id": cfg["id"],
            "category": cfg["category"],
            "title": cfg["title"],
            "code": cfg["code"],
            "cover_url": cover_url,
            "zip_url": zip_url,
            "chapters_count": len(chapters_list),
            "chapters": chapters_list
        })
        print(f"✓ Processed {cfg['title']}: {len(chapters_list)} chapters")

    with open("web_data.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\nSuccessfully wrote web_data.json ({len(manifest)} books, {total_chapters_all} total files).")

if __name__ == "__main__":
    build_manifest()
