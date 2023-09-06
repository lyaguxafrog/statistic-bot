# -*- coding: utf-8 -*-
# /statistic_bot/services/parser.py

import os
import json
from datetime import datetime
from telethon.tl.functions.messages import GetHistoryRequest
from telegram_client import start_client, stop_client

async def dump_all_messages(channel, total_count_limit=0):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0    # номер записи, с которой начинается считывание
    limit_msg = 99999   # максимальное число записей, передаваемых за один раз

    all_messages = []   # список всех сообщений
    total_messages = 0

    class DateTimeEncoder(json.JSONEncoder):
        '''Класс для сериализации записи дат в JSON'''
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    with open('channel_messages.json', 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main(url: str, total_count_limit=0):
    await start_client()
    channel = await client.get_entity(url)
    await dump_all_messages(channel, total_count_limit)
    await stop_client()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Dump messages from a Telegram channel.")
    parser.add_argument("channel_url", type=str, help="URL of the channel")
    parser.add_argument("--message_limit", type=int, default=0, help="Total message limit (0 for all)")

    args = parser.parse_args()
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.channel_url, args.message_limit))