# Документация для проекта "statistic-bot"

## Структура проекта

Проект "statistic-bot" представляет собой Telegram-бота, предназначенного для сбора статистических данных из каналов Telegram. В проекте используется следующая структура каталогов:

```
├── app
│   ├── __init__.py
│   ├── parser.py
│   └── services
│       ├── mysql_tools.py
│       ├── __init__.py
│       ├── telegram_tools.py
│       └── logs.py
├── manage.py
├── pyproject.toml
└── README.md
```

1. `app`: Главный каталог приложения.
   - `__init__.py`: Инциализационный файл для приложения.
   - `parser.py`: Главный скрипт приложения для сбора статистики из каналов Telegram.
   - `services`: Каталог с сервисными модулями.
     - `mysql_tools`: Модуль для управления БД.
     - `telegram_tools`: Модуль для сбора данных из каналов Telegram и записи их в базу данных
     - `__init__.py`: Инциализационный файл для сервисных модулей.
     - `logs.py`: Модуль для логирования событий и ошибок в приложении.

2. `manage.py`: Основной скрипт для управления ботом и запуска сбора данных.

3. `pyproject.toml`: Файл конфигурации Poetry с зависимостями проекта.

4. `README.md`: Описание проекта и инструкции по установке и настройке.



## Инструкция по настройке и запуску

Для успешной настройки и запуска проекта "statistic-bot" выполните следующие шаги:

1. Установите Python 3.10 или более позднюю версию, если она ещё не установлена.

2. Установите Poetry, если он не установлен, с помощью следующей команды:
   ```
   pip install poetry
   ```

3. Перейдите в корневой каталог проекта и выполните следующую команду для установки зависимостей:
   ```
   poetry install
   ```

4. Создайте файл `.env` в корневом каталоге проекта и определите в нем следующие переменные окружения:

   - `API_ID`: API ID для доступа к Telegram API.
   - `API_HASH`: API HASH для доступа к Telegram API.
   - `MYSQL_HOST`: Хост базы данных MySQL.
   - `MYSQL_USER`: Пользователь базы данных MySQL.
   - `MYSQL_PASSWORD`: Пароль пользователя базы данных MySQL.
   - `MYSQL_DB`: Название базы данных MySQL.
   - `MYSQL_PORT`: Порт
   - `TABLE_GET`: Таблица откуда берутся данные
   - `TABLE_SAVE`: Таблица куда сохраняются данные
   - `TELEGRAM_SESSION`: Имя для вашей сессии(любое)

5. Запустите приложение с помощью команды:
   ```
   poetry run python manage.py
   ```

6. Приложение будет периодически собирать статистику из каналов Telegram и записывать её в базу данных MySQL.

Теперь проект "statistic-bot" настроен и готов к работе.

