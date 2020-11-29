import requests
import json

CHANNEL_ID = "polls_channel"

with open("data.json", "r") as f:
    base: list = json.load(f)

new = requests.get(f"https://tg.i-c-a.su/json/{CHANNEL_ID}?limit=20").json()

last_known_id = max(i["id"] for i in base)

new_messages = sorted(new["messages"], key=lambda a: a["id"])

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

with open("data.json", "w") as f:
    json.dump(base, f)