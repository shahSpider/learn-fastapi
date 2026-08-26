# Bookly - FastAPI Book Review REST API

A REST API for a book review web service built with FastAPI and SQLModel.

## Tech Stack

- **Framework:** FastAPI
- **ORM:** SQLModel (SQLAlchemy async + Pydantic)
- **Database:** PostgreSQL (via asyncpg async driver)
- **Validation:** Pydantic
- **Config:** pydantic-settings (`.env` file)

## Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI app entrypoint, lifespan, router registration
│   ├── config.py            # Settings via pydantic-settings (reads .env)
│   ├── requirements.txt     # Dependencies
│   ├── books/
│   │   ├── routes.py        # API routes (CRUD) - currently uses in-memory + JSON
│   │   ├── schemas.py       # Pydantic request/response models
│   │   ├── models.py        # SQLModel database model (Book table)
│   │   └── service.py       # Service layer (stub, not yet implemented)
│   ├── db/
│   │   └── database.py      # Async engine setup, init_db() creates tables
│   └── data/
│       └── data.json        # Seed data (10 books) loaded at import time
├── .env                     # DATABASE_URL env var (gitignored)
├── .gitignore
└── OPENCODE.md
```

## Running the Server

```bash
uvicorn app.main:app --reload
```

The app starts on `http://localhost:8000`. Swagger docs at `/docs`.

## API Endpoints

All book routes are prefixed with `/api/v1/books`.

| Method   | Path                    | Description          |
|----------|-------------------------|----------------------|
| `GET`    | `/`                     | Hello World root     |
| `GET`    | `/api/v1/books/`        | List all books       |
| `POST`   | `/api/v1/books/`        | Create a new book    |
| `GET`    | `/api/v1/books/{book_id}` | Get book by ID     |
| `PATCH`  | `/api/v1/books/{book_id}` | Update book by ID  |
| `DELETE` | `/api/v1/books/{book_id}` | Delete book by ID  |

## Current State / Notes

- **Routes (`routes.py`):** Currently work with an **in-memory list** loaded from `data.json` on startup. Not connected to the database yet.
- **Models (`models.py`):** Defines the `Book` SQLModel table with UUID primary key, mapped to PostgreSQL via `sqlalchemy.dialects.postgresql`.
- **Schemas (`schemas.py`):** Has `BookModel` (full response), `BookCreateModel`, and `BookUpdateModel` (input schemas).
- **Service layer (`service.py`):** Stubbed out with `BookService` class methods (not implemented). Intended to sit between routes and database.
- **Database (`database.py`):** Sets up async SQLAlchemy engine from `.env` `DATABASE_URL` and creates tables on startup via `init_db()`.
- **The app is in transition** from in-memory/JSON storage toward PostgreSQL via SQLModel async sessions.

## Database

- **URL format:** `postgresql+asyncpg://user:pass@host:port/dbname`
- **Current URL in `.env`:** `postgresql+asyncpg://fastapi:fastapi@localhost:5432/fastapidb`
- Tables are auto-created on server startup via `SQLModel.metadata.create_all`.

## Conventions

- All `__init__.py` files are empty (packages only).
- No test framework is set up yet.
- No `requirements.txt` at project root; dependencies live in `app/requirements.txt`.
