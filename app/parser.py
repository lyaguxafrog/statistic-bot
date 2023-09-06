# -*- coding: utf-8 -*-
# app/parser.py

import asyncio
import threading
import os
from dotenv import find_dotenv, load_dotenv
from telethon.sync import TelegramClient

from app.services.logs import logs_gen
from app.services import get_data

load_dotenv(find_dotenv())

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Глобальная переменная-флаг для управления статусом успешности
flag = True


def reset() -> None:
    global flag

    try:
        print('Нажмите Ctrl+C для остановки')
        threading.Timer(3600.0, reset).start()  # Перезапуск через час

        with TelegramClient('pars', api_id, api_hash) as tc:
            try:
                loop = asyncio.get_event_loop()

                urls = get_data.get_mysql_data()  # Получаем список URL из базы данных

                for url in urls:
                    # Вызываем асинхронную функцию parse_channel с использованием asyncio.run
                    err = loop.run_until_complete(get_data.parse(tc, url))

                    if err:
                        flag = False

            except Exception as error:
                logs_gen(logs_type='CRITICAL', logs_message=f'ERROR {error}')
                flag = False

            if flag:
                logs_gen(logs_type='INFO', logs_message='Успешно')
            else:
                logs_gen(logs_type='WARNING', logs_message='Произошла непредвиденная ошибка при попытке запуска.')

    except KeyboardInterrupt:
        logs_gen(logs_type='INFO', logs_message='Остановка сбора данных пользователем...')

if __name__ == "__main__":
    reset()  # Запуск начальной функции reset()
