import json
import os
import sys
from datetime import datetime

news_dir = "News"
index_file = "index.json"
default_preview = "resources/standard.png" 

news_dict = {}
warnings = []
errors = []

if not os.path.isdir(news_dir):
    print(f"❌ '{news_dir}' directory not found.")
    sys.exit(1)

for folder in sorted(os.listdir(news_dir)):
    subdir = os.path.join(news_dir, folder)
    md_path = os.path.join(subdir, "news.md")
    preview_path = os.path.join(subdir, "preview.png")

    if not os.path.isdir(subdir):
        continue

    if not os.path.isfile(md_path):
        warnings.append(f"{folder}: missing news.md — skipped")
        continue

    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    content = "".join(lines).strip()
    if not content:
        errors.append(f"{folder}: news.md is empty")
        continue

    title = lines[0].strip() if lines else folder
    date = datetime.fromtimestamp(os.path.getmtime(md_path)).strftime("%Y-%m-%d")
    preview = f"{news_dir}/{folder}/preview.png" if os.path.isfile(preview_path) else default_preview

    if not os.path.isfile(preview_path):
        warnings.append(f"{folder}: preview.png not found, using standard.png")

    news_dict[folder] = {
        "title": title,
        "date": date,
        "path": f"{news_dir}/{folder}",
        "preview": preview
    }

if warnings:
    print("⚠️ Warnings:")
    for w in warnings:
        print("  -", w)

if errors:
    print("❌ Errors:")
    for e in errors:
        print("  -", e)
    sys.exit(1)

with open(index_file, "w", encoding="utf-8") as f:
    json.dump(news_dict, f, indent=2, ensure_ascii=False)

print(f"✅ New news entries: {', '.join(news_dict.keys())}")
print(f"📦 {index_file} updated, {len(news_dict)} entries.")
