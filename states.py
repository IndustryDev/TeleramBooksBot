from aiogram.fsm.state import StatesGroup, State


class BookSort(StatesGroup):
    search_query = State()


class BookForm(StatesGroup):
    name = State()
    description = State()
    rating = State()
    year = State()
    genre = State()
    author = State()
    cover = State()
    price = State()


class BookFilter(StatesGroup):
    filter_criteria = State()
    rating = State()
    year = State()
    genre = State()
