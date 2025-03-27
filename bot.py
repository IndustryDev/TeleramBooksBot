# База
import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, URLInputFile, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

# Наші
from commands import *
from config import BOT_TOKEN as TOKEN
from data import get_books
from keyboards import books_keyboard_markup, BookCallback
from models import Book
from states import *

dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f'''👋 Hello, {html.bold(message.from_user.full_name)}! Welcome to internet-shop of books!
🛠 Developers: 
{html.link("Chornomorchenko Nazar", "t.me/iinrange")}
{html.link("Shynkar Snizhana", "t.me/Nekiyamura")}''')


@dp.message(BOOKS_COMMAND)
async def books(message: Message) -> None:
    data = get_books()
    markup = books_keyboard_markup(books_list=data)
    await message.answer(
        "📄 List of books. Click on the books title for details.",
        reply_markup=markup
    )

    

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        await message.answer(f"🙄 {html.bold(message.from_user.full_name)}, I dont understand you!")
    except TypeError:
        await message.answer(f"🙄 {html.bold(message.from_user.full_name)}, I dont understand you!")




@dp.callback_query(BookCallback.filter())
async def callback_book(callback: CallbackQuery, callback_data: BookCallback) -> None:
    book_id = callback_data.id
    book_data = get_books(book_id=book_id)
    book = Book(**book_data)
    text = (
        f"📖 Book: {book.name}\n"
        f"📝 Description: {book.description}\n"
        f"📊 Rating: {book.rating}\n"
        f"📆 Year: {book.year}\n"
        f"🔑 Genre: {book.genre}\n"
        f"👤 Author: {book.author}\n"
        f"🕒 Year: {book.year}\n"
        f"💲 Price: {book.price}\n"
    )
    await callback.message.answer_photo(
        caption=text,
        photo=URLInputFile(
            book.cover,
            filename=f"{book.name}_poster.{book.cover.split('.')[-1]}"
        )
    )

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
