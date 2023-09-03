# -*- coding: utf-8 -*-
# /statisic_bot/services/logs.py

import logging

import datetime

now = str(datetime.datetime.now())
logging.basicConfig(level=logging.INFO, filename=f"{now}_log.log",filemode="w",
                     format="%(asctime)s %(levelname)s %(message)s")

def logs_gen(logs_type: str, logs_message: str) -> None:
    """
    Функция логирования 
    
    :params logs_type: Типо логирования: INFO, WARNING, ERROR, CRITICAL
    :params logs_message: Сообщение в логи

    :returns: None
    """


    if logs_type == 'INFO':
        logging.info(msg=logs_message)
    elif logs_type == 'WARNING':
        logging.ingo(msg=logs_message)
    elif logs_type == 'ERROR':
        logging.error(msg=logs_message)
    elif logs_type == 'CRITICAL':
        logging.critical(msg=logs_message)
    else:
        logging.warning(msg='Не верный тип логгирования')