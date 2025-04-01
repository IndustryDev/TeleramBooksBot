import json

from models import Book


def get_books(file_path: str = "data.json", book_id: int | None = None) -> list[dict] | dict:
    with open(file_path, "r") as fp:
        books = json.load(fp)
        if book_id is not None:
            return books[book_id]
        return books
