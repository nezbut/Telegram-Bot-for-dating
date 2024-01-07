from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase
from config import Config


def get_database() -> AgnosticDatabase:
    client = AsyncIOMotorClient(Config.mongodb.connection_string)
    return client.get_database(Config.mongodb.database_name)

__all__ = (
    'get_database',
)
