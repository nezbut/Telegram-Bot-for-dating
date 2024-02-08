# Telegram-Bot для знакомств

Этот проект представляет собой Telegram-бота, созданного с использованием библиотеки Aiogram3. Бот предназначен для поиска новых знакомств в Telegram.

<!-- [***Вот тут можно посмотреть на самого бота***](https://t.me/nezbut_for_daiting_bot) -->

### Скриншоты

![1s](https://github.com/nezbut/Telegram-Bot-for-dating/assets/121932692/5d169eef-83aa-47b6-a984-f9fc15adcc50) ![2s](https://github.com/nezbut/Telegram-Bot-for-dating/assets/121932692/5562f7cc-1173-4a3e-9624-bdc8ce5395e1)![3s](https://github.com/nezbut/Telegram-Bot-for-dating/assets/121932692/31597a10-f6fa-4081-b85f-8eb803f06cd0)![4s](https://github.com/nezbut/Telegram-Bot-for-dating/assets/121932692/5f1f4a99-c1f5-4dca-b1fa-360e61442256)

## Основные технологии

Бот использует следующие основные технологии:

- [Aiogram3](https://docs.aiogram.dev/en/latest/) - мощная библиотека для создания ботов в Telegram на языке Python.
- [MongoDB](https://www.mongodb.com/) - NoSQL база данных, используемая для хранения данных о пользователях и их анкеты.
- [Redis](https://redis.io/) - высокопроизводительная система управления базами данных, используемая для хранения состояний бота и временных данных.

## Установка

Для установки выполните следующие шаги:

1. Клонируйте репозиторий на свой локальный компьютер.
2. Создайте виртуально окружение `python -m venv venv`
3. Установите необходимые зависимости, выполнив команду `pip install -r requirements.txt`.
4. Создайте файл конфигурации `.env` и укажите в нем необходимые настройки, такие как токен бота, показывать ли логи бота, строку для подключения к MongoDB и название базы данных (MongoDB).
5. [Установить Redis](https://redis.io/docs/install/install-redis/)

## Запуск

Для запуска бота выполните команду `python main.py`. Бот будет готов к использованию после успешного запуска.