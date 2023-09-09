#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncio
from app import parser

async def main():
    await parser.pars()

if __name__ == "__main__":
    asyncio.run(main())
