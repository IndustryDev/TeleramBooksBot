from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class BookCallback(CallbackData, prefix="book", sep=";"):
    id: int
    name: str


def books_keyboard_markup(books_list: list[dict], offset: int | None = None, skip: int | None = None):
    builder = InlineKeyboardBuilder()
    for book_data in books_list:
        callback_data = BookCallback(**book_data)
        builder.button(
            text=f"{callback_data.name}",
            callback_data=callback_data.pack()
        )
    builder.adjust(1, repeat=True)
    return builder.as_markup()

