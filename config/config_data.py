from dotenv import load_dotenv
from os import getenv

from dataclasses import dataclass

load_dotenv()

@dataclass
class TelegramBot:
    token: str
    bot_logs: bool

@dataclass
class MongoDB:
    connection_string: str
    database_name: str

@dataclass
class ConfigData:
    tg_bot: TelegramBot
    mongodb: MongoDB

def _get_a_choice_of_parameter(parametr: str) -> bool:
    menu = getenv(parametr.strip().upper()).upper()
    menu_choose = menu if menu in ('YES', 'NO') else 'NO'

    match menu_choose:

        case "YES":
            return True

        case "NO":
            return False

def _load_config_data() -> ConfigData:
    return ConfigData(
        tg_bot=TelegramBot(
            token=getenv("BOT_TOKEN"),
            bot_logs=_get_a_choice_of_parameter(parametr="BOT_LOGS")
        ),
        mongodb=MongoDB(
            connection_string=getenv("MONGO_DB_CONNECTION_STRING"),
            database_name=getenv("DATABASE_NAME")
        )
    )

Config = _load_config_data()

__all__ = (
    'Config',
)
