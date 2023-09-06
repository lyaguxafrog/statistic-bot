# -*- coding: utf-8 -*-
# /statistic_bot/services/telegram_client.py

import os
from dotenv import load_dotenv, find_dotenv
from telethon.sync import TelegramClient

load_dotenv(find_dotenv())

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
session_name = os.getenv('SESSION')

client = TelegramClient(session_name, api_id, api_hash)


async def start_client():
    await client.start()


async def stop_client():
    await client.disconnect()
