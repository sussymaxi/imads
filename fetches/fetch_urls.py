import re  # Import the regular expression module
import asyncio
from telethon import TelegramClient

# Telegram API credentials
TELEGRAM_API_ID = "4330424"
TELEGRAM_API_HASH = "94e95232ea1953cb8a4783dcc979e45a"
api_id = TELEGRAM_API_ID
api_hash = TELEGRAM_API_HASH
session_name = "sessions/tg_fetch_buttons"

async def main(chat_name, limit):
    """
    Fetches messages from a Telegram channel and extracts URLs from text and buttons.
    :param chat_name: Username of the channel (e.g., '@example_channel').
    :param limit: Number of messages to fetch.
    :return: A dictionary with the channel name and a list of extracted URLs.
    """
    async with TelegramClient(session_name, api_id, api_hash) as client:
        # Fetch the channel entity
        try:
            chat_info = await client.get_entity(chat_name)
        except Exception as e:
            print(f"Error fetching channel info: {e}")
            return {"channel": None, "urls": []}

        # Fetch messages from the channel
        try:
            messages = await client.get_messages(entity=chat_info, limit=limit)
        except Exception as e:
            print(f"Error fetching messages: {e}")
            return {"channel": chat_name, "urls": []}

        # Extract URLs from messages and buttons
        urls = []
        for message in messages:
            # Extract URLs from message text
            if message.text:
                text_urls = extract_urls(message.text)
                urls.extend(text_urls)

            # Extract URLs from buttons (if present)
            if message.buttons:
                for row in message.buttons:
                    for button in row:
                        if button.url:
                            urls.append(button.url)

        return {"channel": chat_name, "urls": urls}

def extract_urls(text):
    """
    Extract all URLs from the given text.
    :param text: The text to search for URLs.
    :return: A list of URLs.
    """
    if not text:
        return []
    url_pattern = r'(https?://amazon[^\s]+)'  # Matches http and https URLs
    return re.findall(url_pattern, text)

async def run():
    """
    Main function to fetch and print URLs from a Telegram channel.
    """
    chat_input = "leofferteita"  # Replace with your channel username
    limit = 20  # Number of recent messages to check
    results = await main(chat_name=chat_input, limit=limit)

    if results['urls']:
        print(f"Fetched URLs from channel '{results['channel']}':")
        for url in results['urls']:
            print(url)
    else:
        print(f"No URLs found in the last {limit} messages from '{results['channel']}'.")

# Run the function
if __name__ == "__main__":
    asyncio.run(run())
