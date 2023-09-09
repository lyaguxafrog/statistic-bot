# -*- coding: utf-8 -*-
# app/parser.py


import telethon
from telethon.sync import TelegramClient

import asyncio
import threading
import os
from dotenv import load_dotenv, find_dotenv

from app.services.logs import logs_gen
from app.services.mysql_tools import mysql_connection, get_mysql_data, save_data_to_mysql
from app.services.telegram_tools import telegram_get_messages

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session = os.getenv("TELEGRAM_SESSION")
flag = True

async def pars() -> None:
    print("Нажмите Ctrl+C для остановки.")
    logs_gen(logs_type='INFO', logs_message='Start...')
    threading.Timer(3600.0, pars).start()

    try:

        async with TelegramClient(session, api_id, api_hash) as client:
            try: 
                loop = asyncio.get_event_loop()
                connection = mysql_connection()

                data = get_mysql_data(connection=connection)

                for part_data in data:
                    channel_name = part_data['channel_slug']
                    ids = int(part_data['post_id'])

                    logs_gen(logs_type='INFO', 
                             logs_message=f'{channel_name} | {ids}')
                    
                    message_id, message_views, message_date, message_text = await telegram_get_messages(client, channel_name, ids)

                    save_data_to_mysql(connection=connection, 
                                    post_id=message_id, 
                                    views=message_views, 
                                    timestamp=message_date, 
                                    text=message_text)

            except Exception as err:
                flag = False
                logs_gen(logs_type='CRITICAL', logs_message=err)
            
            if flag:
                logs_gen(logs_type='INFO', logs_message='Успешно]!')
            else:
                logs_gen(logs_type='WARNING', logs_message='Произошла непредвиденная ошибка')

    except KeyboardInterrupt:
        logs_gen(logs_type='INFO', logs_message='Процесс остановлен пользователем...')


