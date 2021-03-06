import requests
import json
import sys

CHANNEL_ID = "polls_channel"

with open("data.json", "r") as f:
    base: list = json.load(f)

url = f"https://tg.i-c-a.su/json/{CHANNEL_ID}?limit=20"

print(url)

new = requests.get(url).json()

if "errors" in new:
    for i in new["errors"]:
        print(f"::error::{i}")
    exit(1)

last_known_id = max(i["id"] for i in base)

new_messages = sorted(new["messages"], key=lambda a: a["id"])

earliest_new_message_id = min(i["id"] for i in new_messages)

if earliest_new_message_id > last_known_id:
    print("Last known message", last_known_id, "has no overlap with first retrieved message", earliest_new_message_id, file=sys.stderr)
    print("Aborting to avoid loosing messages in between.", file=sys.stderr)
    exit(1)

messages_added = 0

for i in new_messages:
    if i["id"] <= last_known_id:
        continue
    data = {
        "id": i["id"],
        "text_html": i["message"],
    }
    if "media" in i and "poll" in i["media"]:
        poll = i["media"]["poll"]
        data["question"] = poll["question"]
        data["answers"] = [j["text"] for j in poll["answers"]]
    
    base.append(data)

    messages_added += 1

if messages_added > 0:
    with open("data.json", "w") as f:
        json.dump(base, f)

print(f"::set-output name=messagesAdded::{messages_added}")
