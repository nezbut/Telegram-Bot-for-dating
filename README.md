# Telegram-Bot for dating

This project is a Telegram bot created using the Aiogram3 library. The bot is designed to search for new acquaintances on Telegram.

[***Here you can see the bot itself***](https://t.me/nezbut_for_daiting_bot)

### Screenshots

![1s](https://github.com/nezbut/Telegram-Bot-for-dating/assets/121932692/5d169eef-83aa-47b6-a984-f9fc15adcc50) ![2s](https://github.com/nezbut/Telegram-Bot-for-dating/assets/121932692/5562f7cc-1173-4a3e-9624-bdc8ce5395e1)![3s](https://github.com/nezbut/Telegram-Bot-for-dating/assets/121932692/31597a10-f6fa-4081-b85f-8eb803f06cd0)![4s](https://github.com/nezbut/Telegram-Bot-for-dating/assets/121932692/5f1f4a99-c1f5-4dca-b1fa-360e61442256)

## Main Technologies

The bot uses the following main technologies:

- [Aiogram3](https://docs.aiogram.dev/en/latest/) - A powerful library for creating Telegram bots in Python.
- [MongoDB](https://www.mongodb.com/) - NoSQL database used to store user data and forms.
- [Redis](https://redis.io/) - A high-performance database management system used to store bot states and temporary data.

## Installation

To install, follow these steps:

1. Clone the repository to your local computer.
2. Create a virtual environment `python -m venv venv`
3. Install the required dependencies by running the command `pip install -r requirements.txt`.
4. Create a `.env` configuration file and specify the necessary settings in it, such as the bot token, whether to show bot logs, the string to connect to MongoDB and the name of the database (MongoDB).
5. [Install Redis](https://redis.io/docs/install/install-redis/)

## Launch

To start the bot, run the command `python main.py`. The bot will be ready to use after successful launch.