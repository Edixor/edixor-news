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

base_url = "https://raw.githubusercontent.com/Terafy/edixor-news/main"

for folder in sorted(os.listdir(news_dir)):
    subdir = os.path.join(news_dir, folder)
    md_path = os.path.join(subdir, "news.md")
    cover_path = os.path.join(subdir, "cover.png")
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

    # Убираем ведущий # и пробел в заголовке, если есть
    raw_title = lines[0].strip() if lines else folder
    title = raw_title[1:].strip() if raw_title.startswith("#") else raw_title

    date = datetime.fromtimestamp(os.path.getmtime(md_path)).strftime("%Y-%m-%d")

    if os.path.isfile(cover_path):
        preview = f"{base_url}/{news_dir}/{folder}/cover.png"
    elif os.path.isfile(preview_path):
        preview = f"{base_url}/{news_dir}/{folder}/preview.png"
        warnings.append(f"{folder}: using fallback preview.png")
    else:
        preview = f"{base_url}/{default_preview}"
        warnings.append(f"{folder}: no cover/preview found, using standard.png")

    md_url = f"{base_url}/{news_dir}/{folder}/news.md"

    news_dict[folder] = {
        "title": title,
        "date": date,
        "path": md_url,
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
