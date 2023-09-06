# -*- coding: utf-8 -*-
# app/services/get_data.py

import os
import datetime
from glob import glob
from dateutil.relativedelta import relativedelta
import pymysql as sql
from dotenv import load_dotenv, find_dotenv
from telethon.sync import TelegramClient

from app.services.logs import logs_gen

load_dotenv(find_dotenv())

async def get_channel_id(client, link) -> int:
    """
    Функция получения ID канала

    :params client: Телеграм клиент
    :params link: Ссылка на телеграм канал

    :returns: ID Канала (int)
    """
    entity = await client.get_entity(link)
    if entity:
        return entity.id

def find_last_parsed_date(path):
    paths = glob(f"data/{path}/*/*meta.txt", recursive=True)
    oldest = datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
    temp = oldest
    for p in paths:
        with open(p, 'r') as file:
            date = datetime.datetime.strptime(file.readlines()[-1], "%Y-%m-%d %H:%M:%S%z")
            if date > oldest:
                oldest = date
    if temp == oldest:
        oldest = datetime.datetime.now() - relativedelta(months=3)
    return oldest

def mysql_tool() -> sql.Connection:
    """
    Функция создания и возврата соединения с базой данных MySQL

    :returns: Подключение к MySQL
    """
    try:
        connection = sql.connect(
            host="158.160.37.87",
            port=3306,
            user="epec_remote",
            password="gWGi1pJXn2KaJpts!",
            database="test_db",
            cursorclass=sql.cursors.DictCursor
        )
        logs_gen(logs_type='INFO',
                  logs_message='Подключено к ' + os.getenv('MYSQL_HOST'))
        return connection
    except Exception as err:
        logs_gen(logs_type='CRITICAL',
                  logs_message="Ошибка подключения к " + os.getenv('MYSQL_HOST') + ":" + str(err))
        exit()

def get_mysql_data() -> list:
    """
    Функция получения данных из базы данных MySQL

    :returns: Список ID каналов
    """
    connection = mysql_tool()
    channel_slugs = []
    qeury = '''
    SELECT * FROM posts
    '''
    with connection.cursor() as cursor:
        cursor.execute(qeury)
        result = cursor.fetchall()
    for row in result:
        channel_slugs.append(row['channel_slug'])
    logs_gen(logs_type='INFO', logs_message=f"{channel_slugs}")
    return channel_slugs

def get_message_content(client, msg, channel_name, directory_name):
    """ 
    Функция получения информации о сообщении и запись в базу данных

    :params client: Телеграм клиент
    :params msg: Сообщение
    :params channel_name: Имя канала
    :params directory_name: Имя директории

    :returns: None
    """
    message_id = str(msg.id)
    message_date = str(msg.date)
    message_text = str(msg.text)
    message_views = str(msg.views)

    file = open(f"data/{channel_name}/{directory_name}/{directory_name}_meta.txt", 'a+')
    file.write(message_id)
    file.write(f"\n{message_date}")
    file.close()

    if msg.text:
        text = message_text
        file = open(f"data/{channel_name}/{directory_name}/{directory_name}.txt", "w")
        file.write(text)
        file.close()

    if msg.media:
        pass
    if msg.entities:
        pass

    connection = mysql_tool()

    try:
        logs_gen(logs_type='INFO', logs_message=f''' Запись данных в MySQL:
                post_id: {message_id}
                stat: {message_views}
                timestamp: {message_date}
                message_text: {message_text} ''')

        insert_query = f'''
INSERT INTO `stats` (post_id, stat, timestamp, message_text) VALUES ('{message_id}', '{message_views}', '{message_date}', '{message_text}');'''
       
        with connection.cursor() as cursor:
            cursor.execute(insert_query)
        connection.commit()
    except Exception as err:
        logs_gen(logs_type='CRITICAL', 
                  logs_message=f'Критическая ошибка: {err}')
        connection.rollback()

async def parse(client, url):
    err = []
    channel_id = str(await get_channel_id(client, url))
    os.makedirs(f"data/{channel_id}", exist_ok=True)
    oldest = find_last_parsed_date(channel_id)
    async for message in client.iter_messages(url, reverse=True, offset_date=oldest):
        try:
            directory_name = str(message.id)
            os.makedirs(f"data/{channel_id}/{directory_name}", exist_ok=True)
            get_message_content(client, message, channel_id, directory_name)

        except Exception as passing:
            err.append(passing)
            continue
    return err

