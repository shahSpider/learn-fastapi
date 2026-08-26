import json
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from app.books.schemas import BookModel, BookUpdateModel
from typing import Optional, List
from pathlib import Path

book_router = APIRouter()

books = []

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data/data.json"

with open(DATA_FILE, "r") as f:
    data = json.load(f)
    books = data["books"]



@book_router.get('/', response_model=List[BookModel])
async def get_all_books():
    return books


@book_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookModel) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

@book_router.get('/{book_id}')
async def get_book(book_id: int = None) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Book not found'
    )

@book_router.patch('/{book_id}')
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    for book in books:
        if book['id'] == book_id:
            data = book_update_data.model_dump()
            book.update(data)
            return book
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No book found to update'
        )

@book_router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Not Found'
    )