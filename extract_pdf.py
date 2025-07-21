import fitz  # PyMuPDF
import os
import json

# ========== CONFIGURATION ==========
PDF_FILE = "input/olympiad_sample.pdf"
OUTPUT_FOLDER = "output"
JSON_OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "structured_output.json")

# ========== SETUP OUTPUT DIRECTORY ==========
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ========== LOAD PDF ==========
doc = fitz.open(PDF_FILE)
structured_data = []

# ========== PROCESS EACH PAGE ==========
for page_number, page in enumerate(doc, start=1):
    print(f"Processing Page {page_number}...")
    page_text = page.get_text()
    images_on_page = []

    # ========== EXTRACT IMAGES ==========
    image_list = page.get_images(full=True)
    for img_index, img_info in enumerate(image_list):
        xref = img_info[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        image_filename = f"page{page_number}_image{img_index + 1}.{image_ext}"
        image_path = os.path.join(OUTPUT_FOLDER, image_filename)

        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)

        images_on_page.append(image_path)

    # ========== ADD TO STRUCTURE ==========
    structured_data.append({
        "page_number": page_number,
        "text": page_text.strip(),
        "images": images_on_page
    })

# ========== SAVE TO JSON ==========
with open(JSON_OUTPUT_FILE, "w", encoding="utf-8") as json_file:
    json.dump(structured_data, json_file, indent=4, ensure_ascii=False)

print(f"\n✅ Extraction Complete!\n- Text and images saved in '{OUTPUT_FOLDER}'\n- Structured data in '{JSON_OUTPUT_FILE}'")
