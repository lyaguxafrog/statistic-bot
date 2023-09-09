# -*- coding: utf-8 -*-
# app/services/mysql_tools.py

# модуль сервиса
import pymysql as sql

# модуль для переменных окружения
import os
from dotenv import load_dotenv, find_dotenv

# модуль логирования
from app.services.logs import logs_gen

load_dotenv(find_dotenv())

def mysql_connection() -> sql.Connection:
    """
    Функция для коннекта к БД

    :returns: Connect
    """

    logs_gen(logs_type='INFO',
              logs_message='Попытка подключения к Mysql')
    try:
        connection = sql.connect(
            host = os.getenv("MYSQL_HOST"),
            port = int(os.getenv("MYSQL_PORT")),
            user = os.getenv("MYSQL_USER"),
            password = os.getenv("MYSQL_PASSWORD"),
            database = os.getenv("MYSQL_DB"),
            cursorclass = sql.cursors.DictCursor
        )

        logs_gen(logs_type='INFO',
    logs_message=f'Подключено к {os.getenv("MYSQL_USER")}@{os.getenv("MYSQL_HOST")}')
        return connection
    except Exception as err:
        logs_gen(logs_type='ERROR', logs_message=err)


def get_mysql_data(connection: sql.Connection) -> list:
    """
    Функция получения данных из бд

    :params connection: MySQL коннект

    :returns: Список данных из MySQL
    """

    table = os.getenv("TABLE_GET")
    query = f"SELECT * FROM {table}"

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    return result


def save_data_to_mysql(connection: sql.Connection,
                    post_id: str, views: str, 
                    timestamp: any, text: str) -> None:
    """
    Функция сохранения данных из Телеграмма

    :params connection: MySQL коннект
    :params post_id: ID поста
    :params views: Кол-во просмотров
    :params timestamp: Время 
    :params text: Текст сообщения
    """

    table = os.getenv("TABLE_SAVE")
    query = f'''
    INSERT INTO {table} (post_id, stat, timestamp, message_text) VALUES ('{post_id}', '{views}', '{timestamp}', '{text}')'''

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
        connection.commit()
        logs_gen(logs_type='INFO', 
    logs_message='Запись в БД')

    except Exception as err:
        logs_gen(logs_type='CRITICAL', logs_message=err)
        connection.rollback()
