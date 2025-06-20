import json
import os
import sys
import re
from pathlib import Path

news_dir = "News"
index_file = os.path.join(news_dir, "index.json")
standard_cover = "standard.png"

warnings = []
errors = []

def read_file_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        errors.append(f"Failed to read {path}: {e}")
        return None

def check_md_content(md_path: Path):
    content = read_file_text(md_path)
    if content is None:
        return None, None
    if not content.strip():
        errors.append(f"{md_path} is empty")
        return None, None

    title_match = re.search(r"^# (.+)", content, flags=re.MULTILINE)
    title = title_match.group(1).strip() if title_match else md_path.parent.name

    img_paths = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", content)
    for img_rel in img_paths:
        img_abs = md_path.parent / img_rel
        if not img_abs.exists():
            errors.append(f"Image '{img_rel}' referenced in {md_path} not found")

    description = ""
    lines = content.splitlines()
    if title_match:
        idx = lines.index(title_match.group(0))
        snippet_lines = lines[idx+1:idx+3]
        description = " ".join([l.strip() for l in snippet_lines]).strip()
    if not description:
        description = content[:100].replace("\n", " ").strip()

    return title, description

def generate_index():
    new_index = {}

    if not os.path.isdir(news_dir):
        errors.append(f"News directory '{news_dir}' not found")
        return new_index

    for folder in sorted(os.listdir(news_dir), reverse=True):
        folder_path = Path(news_dir) / folder
        if not folder_path.is_dir():
            continue

        md_path = folder_path / "news.md"
        if not md_path.exists():
            warnings.append(f"'{folder}/news.md' not found, skipping")
            continue

        title, description = check_md_content(md_path)
        if title is None:
            continue

        cover_path = folder_path / "cover.png"
        if not cover_path.exists():
            warnings.append(f"'{folder}/cover.png' not found, using '{standard_cover}'")
            cover_url = f"{standard_cover}"
        else:
            cover_url = f"{folder}/cover.png"

        new_index[folder] = {
            "id": folder,
            "title": title,
            "date": folder[:10],
            "description": description,
            "cover": f"News/{cover_url}",
            "markdown": f"News/{folder}/news.md"
        }

    return new_index

def main():
    old_index = {}
    if os.path.isfile(index_file):
        try:
            with open(index_file, "r", encoding="utf-8") as f:
                old_index = json.load(f)
        except Exception as e:
            warnings.append(f"Cannot load old index.json: {e}")

    new_index = generate_index()

    old_keys = set(old_index.keys())
    new_keys = set(new_index.keys())

    new_news = new_keys - old_keys
    removed_news = old_keys - new_keys
    updated_news = []

    for key in old_keys & new_keys:
        old_ver = old_index.get(key, {}).get("date")
        new_ver = new_index.get(key, {}).get("date")
        if old_ver != new_ver:
            updated_news.append(f"{key}: date {old_ver} → {new_ver}")

    if new_news:
        print("✅ New news entries:", ", ".join(sorted(new_news)))
    if removed_news:
        print("❌ Removed news entries:", ", ".join(sorted(removed_news)))
    if updated_news:
        print("🔄 Updated news entries:")
        for u in updated_news:
            print("  -", u)

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
        json.dump(new_index, f, indent=2, ensure_ascii=False)
    print(f"📦 {index_file} updated, {len(new_index)} entries.")

if __name__ == "__main__":
    main()
