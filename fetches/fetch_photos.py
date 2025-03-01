import asyncio
from telethon import TelegramClient
from telethon.tl.types import PeerChannel

# Telegram API credentials
api_id = 4330424
api_hash = "94e95232ea1953cb8a4783dcc979e45a"
session_name = "sessions/tg_fetches"

async def fetch_photos_by_ids(channel_username, photo_ids):
    """
    Fetch multiple photos from a Telegram channel using their IDs and save with proper filenames.
    :param channel_username: Username of the channel (e.g., '@example_channel').
    :param photo_ids: List of photo IDs to fetch.
    :return: List of paths to the downloaded photos.
    """
    downloaded_photos = []  # To store the paths of successfully downloaded photos

    async with TelegramClient(session_name, api_id, api_hash) as client:
        # Get the channel entity
        channel = await client.get_entity(channel_username)
        
        # Iterate through messages to find the photos with the given IDs
        async for message in client.iter_messages(channel, limit=1000):  # Adjust limit as needed
            if message.photo and str(message.photo.id) in map(str, photo_ids):
                # Define a meaningful filename
                filename = f"photos/{message.photo.id}.jpg"  # Adjust extension as needed
                file_path = await message.download_media(file=filename)
                print(f"Downloaded photo: {file_path}")
                downloaded_photos.append(file_path)
                
                # Remove the found photo ID from the list to avoid redundant checks
                photo_ids.remove(str(message.photo.id))
                
                # Stop if all photos are downloaded
                if not photo_ids:
                    break

        if photo_ids:
            print(f"Some photo IDs were not found: {photo_ids}")

    return downloaded_photos

async def run():
    # Replace with the channel username and photo IDs
    channel_username = "leofferteita"  # Replace with your channel username
    photo_ids = ["5873954362894693880", "5784208100667010154", "6038578758543322915"]  # Replace with the actual photo IDs

    photo_paths = await fetch_photos_by_ids(channel_username, photo_ids)
    if photo_paths:
        print("Photos saved at:")
        for path in photo_paths:
            print(path)
    else:
        print("No photos were downloaded.")

# Run the function
if __name__ == "__main__":
    asyncio.run(run())
