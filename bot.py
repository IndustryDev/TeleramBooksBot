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
    
/help to see commands list.''')


@dp.message(HELP_COMMAND)
async def help(message: Message) -> None:
    await message.answer(f'''👋 Hello, {html.bold(message.from_user.full_name)}! Welcome to help menu of "Internet-shop of books"!
    ⭐️ Awailable commands:
1. /books - show list of books
2. /search_books - search books
3. /filter_books - filter books
4. /help - show help menu
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


@dp.message(FILTER_BOOKS_COMMAND)
async def filter_books(message: Message, state: FSMContext) -> None:
    await state.set_state(BookFilter.filter_criteria)
    await message.answer(
        "❓ What criteria would you like to filter by?\n"
        "📌 Choose one of the following: genre, rating, or year.",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(BookFilter.filter_criteria)
async def filter_criteria(message: Message, state: FSMContext) -> None:
    criteria = message.text.lower()

    if criteria in ['genre', 'rating', 'year']:
        await state.update_data(criteria=criteria)
        if criteria == 'genre':
            await state.set_state(BookFilter.genre)
            await message.answer("✏️ Enter the genre you'd like to filter by.")
        elif criteria == 'rating':
            await state.set_state(BookFilter.rating)
            await message.answer("✏️ Enter the minimum rating (0-5).")
        elif criteria == 'year':
            await state.set_state(BookFilter.year)
            await message.answer("✏️ Enter the year to filter by.")
    else:
        await message.answer("🚫 Invalid criteria. Please choose from: genre, rating, or year.")


@dp.message(BookFilter.genre)
async def filter_by_genre(message: Message, state: FSMContext) -> None:
    genre = message.text.lower()
    await state.update_data(genre=genre)
    await state.set_state(BookFilter.filter_criteria)
    books = get_books()
    filtered_books = [book for book in books if genre in book['genre'].lower()]
    if filtered_books:
        markup = books_keyboard_markup(books_list=filtered_books)
        await message.answer("🔰 Filtered books by genre:", reply_markup=markup)
    else:
        await message.answer("❌ No books found for this genre.")
    await state.clear()


@dp.message(BookFilter.rating)
async def filter_by_rating(message: Message, state: FSMContext) -> None:
    try:
        rating = float(message.text)
        if 0 <= rating <= 5:
            await state.update_data(rating=rating)
            await state.set_state(BookFilter.filter_criteria)
            books = get_books()
            filtered_books = [book for book in books if book['rating'] >= rating]
            if filtered_books:
                markup = books_keyboard_markup(books_list=filtered_books)
                await message.answer("🔰 Filtered books by rating:", reply_markup=markup)
            else:
                await message.answer("❌ No books found with this rating.")
        else:
            await message.answer("🚫 Invalid rating. Please enter a number between 0 and 5.")
    except ValueError:
        await message.answer("🚫 Invalid rating. Please enter a valid number between 0 and 5.")
    await state.clear()


@dp.message(BookFilter.year)
async def filter_by_year(message: Message, state: FSMContext) -> None:
    try:
        year = int(message.text)
        await state.update_data(year=year)
        await state.set_state(BookFilter.filter_criteria)
        books = get_books()
        filtered_books = [book for book in books if book['year'] == year]
        if filtered_books:
            markup = books_keyboard_markup(books_list=filtered_books)
            await message.answer(f"🔰 Filtered books by year {year}:", reply_markup=markup)
        else:
            await message.answer(f"❌ No books found from the year {year}.")
    except ValueError:
        await message.answer("🚫 Invalid year. Please enter a valid number.")
    await state.clear()


@dp.message(SEARCH_BOOKS_COMMAND)
async def search_book(message: Message, state: FSMContext) -> None:
    await state.set_state(BookSort.search_query)
    await message.answer(
        '🔍 Enter book name to search.',
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(BookSort.search_query)
async def search_query(message: Message, state: FSMContext) -> None:
    query = message.text.lower()
    books = get_books()
    results = [book for book in books if query in book['name'].lower()]
    if results:
        await message.reply('👍 Search complete!', reply_markup=books_keyboard_markup(results))
    else:
        await message.reply('☹️ Search lose')
    await state.clear()


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
        f"💲 Price: {book.price}$\n"
        f"🔗 Buy here: {book.website}\n"
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
