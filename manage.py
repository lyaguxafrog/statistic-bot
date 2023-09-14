
#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncio
from asyncio import run
from app import parser
import asyncio

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

time = float(os.getenv("TIME"))

print("Нажмите Ctrl+C для остановки.")

async def repeat():
    while True:
        await parser.pars()
        await asyncio.sleep(time)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(repeat())

