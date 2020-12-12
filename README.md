# Polls Channel Messages Log

A simple and brutal public message log for Telegram channels, focused on text and poll messages.

- For text messages or media message with a caption, the text/caption is used.
- For poll/quiz messages, the question and all options are used.
- Message ID is always used to produce a link to the message.
- There is no indication about message type.

## Details

- Web: https://blueset.github.io/polls_channel_history
- Updated daily via GitHub Actions
- Code license: MIT

## How to use this for your own channel?

1. Clone or download this repository locally.
1. Install Python 3.
2. Install all Python dependency packages via `python3 -m pip install -r requirements.txt`.
1. Export your channel using Telegram Desktop, choose the time range of messages, and export to JSON format with no media file.
    - Open a channel in Telegram Desktop
    - Click the 3 dots at the corner
    - Click “Export channel history”
    - Uncheck all boxes
    - Click the text after “Format” and choose “Machine-readable JSON”
1. Generate the initial message list JSON use `python3 from_telegram_desktop_export_json.py < YOUR_EXPORTED_JSON.json > data.json`
1. Edit `template.html` with information about your own channel.
1. Run `python3 render_data.py` to build the web page. The final web page is `index.html`.
1. For further updates, edit `load_latest_from_tme.py`, replace the channel username after `CHANNEL_ID="` with your own one. **Note:** this only work for public channels. Run this script with `python3 load_latest_from_tme.py` to update the content. The script will warn you if auto update is failed due to more than 20 messages added since last update.
