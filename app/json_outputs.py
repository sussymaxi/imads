# import asyncio
# from telethon import TelegramClient
# from openai import OpenAI
# import json

# TELEGRAM_API_ID = "4330424"
# TELEGRAM_API_HASH = "94e95232ea1953cb8a4783dcc979e45a"
# api_id = TELEGRAM_API_ID
# api_hash = TELEGRAM_API_HASH
# session_name = "../fetches/sessions/tg_fetches"  

# client = OpenAI(api_key="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")


# def send_query(messages):
#     completion = client.chat.completions.create(
#         model = "gpt-4o-mini",
#         messages = messages,
#         response_format = {
#             "type": "json_object"
#         }
#     )
#     output = completion.choices[0].message.content
#     cleaned_output= output.replace("```json", "").replace("```", "").strip()
#     json_transform = json.loads(cleaned_output)
#     return json_transform


# async def main(chat_name, limit):
#     # "async with" creates asynchronous context managers
#     # It is an extension of the “with” expression for use only in coroutines within asyncio programs
#     async with TelegramClient(session_name, api_id, api_hash) as client:
#         # Get chat info  
#         chat_info = await client.get_entity(chat_name)
#         # Get all the messages, given the limit
#         # It will return the latest 5 messages if limit is 5
#         messages = await client.get_messages(entity=chat_info, limit=3)
#         # return the results in a dictionary
#         return ({"messages": messages, "channel": chat_info})
    
# async def run():
#     chat_input = "leofferteita"
#     results = await main(chat_name=chat_input, limit=20)
#     for result in results['messages']:
#         # print(result.message)
#         ai_dict = [
#                 {
#                     "role": "system",
#                     "content": 'You have to fetch all the data from the posts from a Telegram channel and then give as output the json, for example:{"name": "hoodie", "description": "This hoodie is nice for black people.", "link": "", "price_old": 0, "price_new: 0, "id_post": "", "id_channel": ""}'
#                 },
#                 {
#                     "role": "user",
#                     "content": str(result)
#                 }
#         ]
#         query_res = send_query(ai_dict)
#         print(query_res)
#         break

# asyncio.run(run())


import asyncio
from telethon import TelegramClient
from openai import OpenAI
import json
import sqlite3

# Telegram API credentials
TELEGRAM_API_ID = "4330424"
TELEGRAM_API_HASH = "94e95232ea1953cb8a4783dcc979e45a"
api_id = TELEGRAM_API_ID
api_hash = TELEGRAM_API_HASH
session_name = "../fetches/sessions/tg_fetches"

# OpenAI API client
client = OpenAI(api_key="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")


def send_query(messages):
    """Send query to OpenAI API and parse the result."""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={
            "type": "json_object"
        }
    )
    output = completion.choices[0].message.content
    cleaned_output = output.replace("```json", "").replace("```", "").strip()
    json_transform = json.loads(cleaned_output)
    return json_transform


async def main(chat_name, limit):
    """Fetch messages from a Telegram channel."""
    async with TelegramClient(session_name, api_id, api_hash) as client:
        chat_info = await client.get_entity(chat_name)
        messages = await client.get_messages(entity=chat_info, limit=limit)  # Use limit argument here
        return {"messages": messages, "channel": chat_info}


DB_PATH = "imads.db"  # Path to your SQLite database

# Function to save data into the database
def save_to_database(data):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Insert data into the table
        cursor.execute("""
            INSERT INTO imads (name, description, link, price_old, price_new, id_post, id_channel)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("name", ""),
            data.get("description", ""),
            data.get("link", ""),
            data.get("price_old", 0),
            data.get("price_new", 0),
            data.get("id_post", ""),
            data.get("id_channel", "")
        ))

        # Commit the transaction
        conn.commit()
    except Exception as e:
        print(f"Error saving to database: {e}")
    finally:
        conn.close()

async def run():
    """Main function to fetch messages and process with AI."""
    chat_input = "leofferteita"
    results = await main(chat_name=chat_input, limit=10)  # Fetch N messages
    for result in results['messages']:
        ai_dict = [
            {
                "role": "system",
                "content": 'You have to fetch all the data from the posts from a Telegram channel and then give as output the json, for example:{"name": "hoodie", "description": "This hoodie is nice for black people.", "link": "", "price_old": 0, "price_new: 0, "id_post": "", "id_channel": ""}'
            },
            {
                "role": "user",
                "content": str(result)
            }
        ]
        query_res = send_query(ai_dict)
        # print(query_res)  # Print the AI-processed JSON
        # Remove "break" to process all fetched messages
        # break


# Run the asyncio event loop
asyncio.run(run())
