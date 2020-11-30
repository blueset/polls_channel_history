"""
Build data json from JSON exported from Telegram Desktop single chat JSON export.

Usage:
    python3 from_telegram_desktop_export_json.py < telegram_export.json > data.json
"""

import json
import sys
import html

def transform_text(t) -> str:
    if isinstance(t, str):
    elif isinstance(t, list):
        return "".join(transform_text(i) for i in t)
    else:
        if t["type"] == "text_link":
            return f'<a href="{html.escape(t["href"])}">{transform_text(t["text"])}</a>'
        elif t["type"] == "link":
            return f'<a href="{html.escape(t["text"])}">{transform_text(t["text"])}</a>'
        elif t["type"] == "mention":
            return f'<a href="https://t.me/{t["text"][1:]}">{t["text"]}</a>'
        elif t["type"] == "bold":
            return f'<b>{transform_text(t["text"])}</b>'
        elif t["type"] == "italics":
            return f'<i>{transform_text(t["text"])}</i>'
        elif t["type"] == "underline":
            return f'<u>{transform_text(t["text"])}</u>'
        elif t["type"] == "code":
            return f'<code>{transform_text(t["text"])}</code>'
        elif t["type"] == "strikethrough":
            return f'<s>{transform_text(t["text"])}</s>'
        else:
            return transform_text(t["text"])

tg_data = json.load(sys.stdin)

result = []

for i in tg_data["messages"]:
    item = {
        "id": i["id"],
    }
    if "text" in i:
        item["text_html"] = transform_text(i["text"])
    if "poll" in i:
        item["question"] = i["poll"]["question"]
        item["answers"] = [a["text"] for a in i["poll"]["answers"]]
    result.append(item)
    
json.dump(result, sys.stdout)
