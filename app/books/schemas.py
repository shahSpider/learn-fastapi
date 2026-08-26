from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

class BookModel(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str
    creation: datetime
    updated_on: datetime

class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str