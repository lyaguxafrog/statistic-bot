# -*- coding: utf-8 -*-
# app/services/telegram_tools.py

import telethon
from telethon import TelegramClient

import os
from dotenv import load_dotenv, find_dotenv

from app.services.logs import logs_gen
from app.services.mysql_tools import *



async def telegram_get_messages(client, channel_name: str, post_id: str):
    """
    Получение сообщения из телеграмма по ID

    :params client: Клиент телеграмма
    :params channel_name: Имя канала ( @<это_имя> )
    :params post_id: ID Поста

    :returns: ID поста, просмотры, время, текст
    """

    message = await client.get_messages(channel_name, ids=post_id)

    message_id = message.id
    message_views = message.views
    message_date = message.date
    message_text = str(message.text)

    logs_gen(logs_type='INFO', logs_message=f'''Получены данные\n
                                                {message_id}
                                                {message_views}
                                                {message_date}
                                                {message_text}''')



    return message_id, message_views, message_date, message_text    
