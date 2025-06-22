# ✅ app/tag_text.py
input_path = "resources/FA-cleaned.txt"
output_path = "resources/FA-tagged.txt"

tag_map = {
    "fracture": "# FRACTURE",
    "bleeding": "# BLEEDING",
    "burns": "# BURNS",
    "cpr": "# CPR",
    "shock": "# SHOCK",
    "unconscious": "# UNCONSCIOUS",
    "choking": "# CHOKING",
    "snake bite": "# SNAKE_BITE"
}

with open(input_path, "r", encoding="utf-8") as f:
    content = f.read()

for keyword, tag in tag_map.items():
    content = content.replace(keyword, f"{tag} {keyword}")

with open(output_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Tagged text written to FA-tagged.txt")
