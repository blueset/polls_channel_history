import requests
import json
import sys
from bs4 import BeautifulSoup

CHANNEL_ID = "polls_channel"

def extract_id(data_post: str) -> int:
    return int(data_post[len(CHANNEL_ID) + 1:])

with open("data.json", "r") as f:
    base: list = json.load(f)

url = f"https://t.me/s/{CHANNEL_ID}"

print(url)

content = requests.get(url).text
soup = BeautifulSoup(content, features="html.parser")

for i in soup.select("i.emoji"):
    i.replace_with(i.text)

last_known_id = max(i["id"] for i in base)

messages = soup.select("[data-post]")

earliest_new_message_id = min(extract_id(i["data-post"]) for i in messages)

if earliest_new_message_id > last_known_id:
    print("Last known message", last_known_id, "has no overlap with first retrieved message",
          earliest_new_message_id, file=sys.stderr)
    print("Aborting to avoid loosing messages in between.", file=sys.stderr)
    exit(1)

messages_added = 0

for i in messages:
    msg_id = extract_id(i["data-post"])
    if msg_id <= last_known_id:
        continue
    data = {
        "id": msg_id,
        "text_html": "",
    }

    text_node = i.select_one(".tgme_widget_message_text")
    if text_node is not None:
        data["text_html"] = text_node.decode_contents()

    question_node = i.select_one(".tgme_widget_message_poll_question")
    if question_node:
        data["question"] = question_node.text
        answer_nodes = i.select(".tgme_widget_message_poll_option_text")
        data["answers"] = [j.text for j in answer_nodes]

    base.append(data)

    messages_added += 1

if messages_added > 0:
    with open("data.json", "w") as f:
        json.dump(base, f, ensure_ascii=False, indent=2)

print(f"::set-output name=messagesAdded::{messages_added}")
