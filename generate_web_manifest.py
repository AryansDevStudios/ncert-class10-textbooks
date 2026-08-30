import fitz
import os
import json
import re

BASE_DIR = r"d:\NCERT_Textbook\Class_10"

# Real chapter titles for Class 10 NCERT books
CHAPTER_TITLES = {
    "Mathematics": {
        "1": "Real Numbers",
        "2": "Polynomials",
        "3": "Pair of Linear Equations in Two Variables",
        "4": "Quadratic Equations",
        "5": "Arithmetic Progressions",
        "6": "Triangles",
        "7": "Coordinate Geometry",
        "8": "Introduction to Trigonometry",
        "9": "Some Applications of Trigonometry",
        "10": "Circles",
        "11": "Areas Related to Circles",
        "12": "Surface Areas and Volumes",
        "13": "Statistics",
        "14": "Probability",
        "a1": "Appendix I: Proofs in Mathematics",
        "a2": "Appendix II: Mathematical Modelling",
        "an": "Answers"
    },
    "Science": {
        "1": "Chemical Reactions and Equations",
        "2": "Acids, Bases and Salts",
        "3": "Metals and Non-metals",
        "4": "Carbon and its Compounds",
        "5": "Life Processes",
        "6": "Control and Coordination",
        "7": "How do Organisms Reproduce?",
        "8": "Heredity",
        "9": "Light – Reflection and Refraction",
        "10": "The Human Eye and the Colourful World",
        "11": "Electricity",
        "12": "Magnetic Effects of Electric Current",
        "13": "Our Environment",
        "an": "Answers"
    },
    "First_Flight": {
        "1": "A Letter to God & Poems",
        "2": "Nelson Mandela: Long Walk to Freedom",
        "3": "Two Stories about Flying",
        "4": "From the Diary of Anne Frank",
        "5": "Glimpses of India",
        "6": "Mijbil the Otter",
        "7": "Madam Rides the Bus",
        "8": "The Sermon at Benares",
        "9": "The Proposal"
    },
    "Footprints_Without_Feet": {
        "1": "A Triumph of Surgery",
        "2": "The Thief’s Story",
        "3": "The Midnight Visitor",
        "4": "A Question of Trust",
        "5": "Footprints without Feet",
        "6": "The Making of a Scientist",
        "7": "The Necklace",
        "8": "Bholi",
        "9": "The Book That Saved the Earth"
    },
    "Kshitij_2": {
        "1": "पद (सूरदास)",
        "2": "राम-लक्ष्मण-परशुराम संवाद",
        "3": "आत्मकथ्य (जयशंकर प्रसाद)",
        "4": "उत्साह और अट नहीं रही (निराला)",
        "5": "यह दंतुरित मुस्कान और फसल (नागार्जुन)",
        "6": "संगतकार (मंगलेश डबराल)",
        "7": "नेताजी का चश्मा",
        "8": "बालगोबिन भगत",
        "9": "लखनवी अंदाज़",
        "10": "एक कहानी यह भी",
        "11": "नौबतखाने में इबादत",
        "12": "संस्कृति"
    },
    "Kritika": {
        "1": "माता का अँचल",
        "2": "साना-साना हाथ जोड़ि...",
        "3": "मैं क्यों लिखता हूँ?",
        "lp": "लेखक परिचय"
    },
    "Geography_Contemporary_India": {
        "1": "Resources and Development",
        "2": "Forest and Wildlife Resources",
        "3": "Water Resources",
        "4": "Agriculture",
        "5": "Minerals and Energy Resources",
        "6": "Manufacturing Industries",
        "7": "Lifelines of National Economy",
        "a1": "Appendix & Glossary"
    },
    "Economics_Understanding_Economic_Development": {
        "1": "Development",
        "2": "Sectors of the Indian Economy",
        "3": "Money and Credit",
        "4": "Globalisation and the Indian Economy",
        "5": "Consumer Rights"
    },
    "History_India_and_the_Contemporary_World_II": {
        "1": "The Rise of Nationalism in Europe",
        "2": "Nationalism in India",
        "3": "The Making of a Global World",
        "4": "The Age of Industrialisation",
        "5": "Print Culture and the Modern World"
    },
    "Political_Science_Democratic_Politics": {
        "1": "Power Sharing",
        "2": "Federalism",
        "3": "Gender, Religion and Caste",
        "4": "Political Parties",
        "5": "Outcomes of Democracy"
    }
}

# Build structured web manifest
books_data = []

SUBJECT_METAS = {
    "English": {"icon": "book-open", "color": "#3B82F6", "badge": "English"},
    "Hindi": {"icon": "feather", "color": "#EC4899", "badge": "Hindi"},
    "Mathematics": {"icon": "divide-square", "color": "#8B5CF6", "badge": "Maths"},
    "Science": {"icon": "atom", "color": "#10B981", "badge": "Science"},
    "Social_Science": {"icon": "globe", "color": "#F59E0B", "badge": "Social Science"},
}

for cat_folder in sorted(os.listdir(BASE_DIR)):
    cat_path = os.path.join(BASE_DIR, cat_folder)
    if not os.path.isdir(cat_path):
        continue
    
    for book_folder in sorted(os.listdir(cat_path)):
        bpath = os.path.join(cat_path, book_folder)
        if not os.path.isdir(bpath):
            continue
        
        # Look for cover
        cover_rel = f"Class_10/{cat_folder}/{book_folder}/cover.jpg"
        has_cover = os.path.exists(os.path.join(bpath, "cover.jpg"))
        
        # Look for zip
        zip_rel = None
        for f in os.listdir(bpath):
            if f.endswith(".zip"):
                zip_rel = f"Class_10/{cat_folder}/{book_folder}/{f}"
                break
                
        # Chapters
        chapters_dir = os.path.join(bpath, "chapters")
        chapters_list = []
        if os.path.exists(chapters_dir):
            for cf in sorted(os.listdir(chapters_dir)):
                if cf.endswith(".pdf"):
                    pdf_rel = f"Class_10/{cat_folder}/{book_folder}/chapters/{cf}"
                    sz = os.path.getsize(os.path.join(chapters_dir, cf))
                    
                    # Extract title
                    ch_key = None
                    cf_lower = cf.lower()
                    if "ps" in cf_lower or "pr" in cf_lower or "prelim" in cf_lower:
                        ch_title = "Preliminary Pages & Table of Contents"
                        ch_type = "prelims"
                    elif "an" in cf_lower:
                        ch_title = "Answers & Solutions"
                        ch_type = "answers"
                    elif "a1" in cf_lower:
                        ch_title = "Appendix I"
                        ch_type = "appendix"
                    elif "a2" in cf_lower:
                        ch_title = "Appendix II"
                        ch_type = "appendix"
                    elif "lp" in cf_lower:
                        ch_title = "लेखक परिचय (Author Profiles)"
                        ch_type = "intro"
                    else:
                        m = re.search(r'(\d{2})\.pdf$', cf_lower)
                        if m:
                            num = str(int(m.group(1)))
                            ch_title = CHAPTER_TITLES.get(book_folder, {}).get(num, f"Chapter {num}")
                            ch_type = "chapter"
                        else:
                            ch_title = cf.replace(".pdf", "")
                            ch_type = "other"
                            
                    chapters_list.append({
                        "filename": cf,
                        "title": ch_title,
                        "type": ch_type,
                        "size_formatted": f"{sz / 1024:.1f} KB",
                        "size_bytes": sz,
                        "url": pdf_rel
                    })
        
        # Sort chapters logically: prelims first, then chapters, then appendix/answers
        def ch_sort_key(c):
            if c["type"] == "prelims": return 0
            if c["type"] == "chapter":
                m = re.search(r'(\d+)', c["filename"])
                return int(m.group(1)) if m else 100
            if c["type"] == "intro": return 200
            if c["type"] == "appendix": return 300
            if c["type"] == "answers": return 400
            return 500
        
        chapters_list.sort(key=ch_sort_key)
        
        display_name = book_folder.replace("_", " ")
        if display_name.startswith("Geography"): display_name = "Geography: Contemporary India - II"
        elif display_name.startswith("Economics"): display_name = "Economics: Understanding Economic Development"
        elif display_name.startswith("History"): display_name = "History: India and the Contemporary World - II"
        elif display_name.startswith("Political"): display_name = "Political Science: Democratic Politics - II"
        
        cat_meta = SUBJECT_METAS.get(cat_folder, {"icon": "book", "color": "#6366F1", "badge": cat_folder})
        
        books_data.append({
            "id": book_folder,
            "category": cat_folder.replace("_", " "),
            "category_key": cat_folder,
            "title": display_name,
            "cover_url": cover_rel if has_cover else None,
            "zip_url": zip_rel,
            "chapters_count": len([c for c in chapters_list if c["type"] == "chapter"]),
            "total_files": len(chapters_list),
            "theme_color": cat_meta["color"],
            "badge": cat_meta["badge"],
            "chapters": chapters_list
        })

with open("d:/NCERT_Textbook/web_data.json", "w", encoding="utf-8") as f:
    json.dump(books_data, f, indent=2, ensure_ascii=False)

print(f"Generated web_data.json for {len(books_data)} books with full chapter mappings!")
