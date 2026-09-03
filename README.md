# NCERT Class 10 Digital Textbooks & Interactive Reader

A clean, modern, and watermark-free digital library for **NCERT Class 10 Textbooks** with full chapter navigation, Fast Web View (linearization), and integrated Mozilla PDF.js viewer.

## 📚 Included Textbooks

- **Mathematics**: Full Course Textbook, Answers & Appendices
- **Science**: Comprehensive Physics, Chemistry & Biology Textbook
- **Social Science (SST)**:
  - *Contemporary India - II* (Geography)
  - *Understanding Economic Development* (Economics)
  - *India and the Contemporary World - II* (History)
  - *Democratic Politics - II* (Political Science)
- **English**:
  - *First Flight* (Main Reader)
  - *Footprints Without Feet* (Supplementary Reader)
- **Hindi**:
  - *Kshitij-2* (Course A Main Textbook)
  - *Kritika* (Course A Supplementary Reader)
- **Information Technology (IT 402)**:
  - *Domestic Data Entry Operator* (Part B — Subject Specific Skills)
  - *Employability Skills* (Part A — Mandatory Common Module)

## 🛠️ Python Automation Scripts

The codebase includes automated utilities:

1. **`fetch_ncert_textbooks.py`**  
   Downloads complete textbook packages directly from the official NCERT portal and extracts chapters, prelims, answers, and covers into structured directories under `Class_10/`.
   ```bash
   python fetch_ncert_textbooks.py
   ```

2. **`remove_watermarks.py`**  
   Recursively scans all chapter PDFs, removes recurring image XObject watermarks and soft masks losslessly without degrading text/vector graphics, sanitizes metadata, and linearizes files to **PDF 1.7 Fast Web View**.
   ```bash
   python remove_watermarks.py
   ```

3. **`generate_manifest.py`**  
   Scans the `Class_10/` directory, extracts page counts, chapter metadata, and file sizes, and compiles `web_data.json` for the web reader.
   ```bash
   python generate_manifest.py
   ```

4. **`server.py`**  
   Local streaming development server with byte-range support (`Accept-Ranges: bytes`) and CORS headers.
   ```bash
   python server.py
   ```

## 🌐 Live Web Reader

- **Live URL**: [https://aryansdevstudios.github.io/ncert-class10-textbooks/](https://aryansdevstudios.github.io/ncert-class10-textbooks/)
