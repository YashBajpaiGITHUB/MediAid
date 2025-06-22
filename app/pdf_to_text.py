# ✅ app/pdf_to_text.py
import fitz  # PyMuPDF

pdf_path = "resources/FA-manual-YashProject.pdf"
output_path = "resources/FA-cleaned.txt"

doc = fitz.open(pdf_path)
with open(output_path, "w", encoding="utf-8") as out:
    for page in doc:
        out.write(page.get_text() + "\n\n")

print("✅ Cleaned PDF text saved to FA-cleaned.txt")
