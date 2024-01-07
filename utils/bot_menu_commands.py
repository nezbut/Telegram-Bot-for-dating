from aiogram import Bot
from aiogram.types import BotCommand
import logging

logger = logging.getLogger(__name__)

async def set_menu_commands(bot: Bot) -> None:
    bot_menu_commands = await bot.get_my_commands()

    if not _check_exists_and_valid_bot_commands(commands=bot_menu_commands):
        commands = [
            BotCommand(
                command="/myprofile",
                description="👤"
            ),

            BotCommand(
                command="/help",
                description="🆘"
            )
        ]

        await bot.set_my_commands(commands=commands)
        logger.info("Installed menu with commands")

def _check_exists_and_valid_bot_commands(commands: list[BotCommand]) -> bool | None:

    if commands:

        for command in commands:
            if command.command not in ("myprofile", "help"):
                return False

        return True

__all__ = (
    'set_menu_commands',
)
