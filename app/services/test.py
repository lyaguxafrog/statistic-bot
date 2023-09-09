from telethon import TelegramClient
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_ID= os.getenv("API_ID")
API_HASH= os.getenv("API_HASH")

client = TelegramClient('pars', api_id=API_ID, api_hash=API_HASH)

async def print_message():
    message = await client.get_messages('makridos', ids=14)
    print("MESSAGE:", end="\n-------\n")
    print(message.text)
    print(message.id)
    print(message.views)

with client:
    client.loop.run_until_complete(print_message())
