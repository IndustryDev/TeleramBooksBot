
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

BOOKS_COMMAND = Command("books")
START_COMMAND = Command("start")
SEARCH_BOOKS_COMMAND = Command("search_books")
FILTER_BOOKS_COMMAND = Command("filter_books")
HELP_COMMAND = Command("help")

BOT_COMMANDS = [
   BotCommand(command="books", description="View a list of available books"),
   BotCommand(command="start", description="Start a conversation"),
   BotCommand(command="search_books", description="Search books"),
   BotCommand(command="filter_books", description="Filter books"),
   BotCommand(command="help", description="Show help")
]
