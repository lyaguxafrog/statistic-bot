# -*- coding: utf-8 -*-
# /statistic_bot/services/telegram_tools.py

import requests as rq
import telethon
from telethon import TelegramClient

import random
import string
import os 
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from logs import logs_gen

def generate_session(length: int) -> str:
    """  
    Генерация случайных строк для сессии

    :params length: Длина строки
    :returns: Строка(Имя сессии)
    """
    try:
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        
        return rand_string
    except TypeError as error:
        logs_gen(logs_type='CRITICAL',
                  logs_message=f'Неверно указана длинна строки: {error}')

def telegram_auth(login: None) -> None:
    """ Логин в телеграм по API """

    logs_gen(logs_type='INFO',
              logs_message='Запукск telegram_auth, попытка аунтификации...')

    try:
        api_id = os.getenv('API_ID')
        api_hash = os.getenv('API_HASH')
        phone_number = os.getenv('PHONE')

        session = generate_session(8)

        logs_gen(logs_type='INFO', logs_message=f'''
                API ID: {api_id}\n
                API_HASH: {api_hash}
                PHONE = {phone_number}
                SESSION = {session}''')
        
        client = TelegramClient(session=session, api_id=api_id, 
                                api_hash=api_hash, )
        
        try:
            client.connect()
        except OSError as error:
            logs_gen(logs_type='CRITICAL', 
            logs_message=f'Не удалось подключиться к телеграмму: {error}')
    except:
        logs_gen(logs_type='CRITICAL',
                  logs_message='Не удалось подключится, проверьте .env')