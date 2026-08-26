# Bookly - System Design Workspace

## High-Level Architecture

```mermaid
graph TB
    Client["Client / Browser"]

    subgraph FastAPI["FastAPI Application (app/main.py)"]
        Root["GET /"]
        Router["Book Router<br/>/api/v1/books"]
    end

    subgraph Routes["Route Handlers (books/routes.py)"]
        GET_ALL["GET /"]
        GET_ONE["GET /{book_id}"]
        POST["POST /"]
        PATCH["PATCH /{book_id}"]
        DELETE["DELETE /{book_id}"]
    end

    subgraph Store["Data Store (in-memory list)"]
        Memory["Module-level list<br/>loaded from data.json"]
    end

    subgraph DB_Layer["Database Layer"]
        Engine["Async Engine<br/>(sqlalchemy)"]
        DB["PostgreSQL<br/>fastapidb"]
    end

    subgraph Config["Configuration"]
        Settings["pydantic-settings"]
        Env[".env"]
    end

    Client -->|"HTTP requests"| FastAPI
    FastAPI --> Router
    Router --> Routes
    GET_ALL & GET_ONE & POST & PATCH & DELETE --> Memory
    Engine -.->|"creates tables on startup<br/>(currently unused by routes)"| DB
    Config --> Settings
    Env --> Settings
    Settings -.-> Engine

    style Memory fill:#f9f,stroke:#333,stroke-width:2px
    style DB fill:#cff,stroke:#333,stroke-width:2px
```

## Module Dependency Graph

```mermaid
graph LR
    main["app/main.py"]
    config["app/config.py"]
    database["app/db/database.py"]
    models["app/books/models.py"]
    schemas["app/books/schemas.py"]
    routes["app/books/routes.py"]
    service["app/books/service.py"]
    data["app/data/data.json"]
    env[".env"]

    main -->|"imports book_router"| routes
    main -->|"imports init_db"| database
    database -->|"imports get_settings"| config
    database -->|"imports Book (model registration)"| models
    config -->|"reads DATABASE_URL"| env
    routes -->|"imports BookModel, BookUpdateModel"| schemas
    routes -->|"loads seed data"| data
    service -->|"imports BookCreateModel, BookUpdateModel"| schemas
    service -->|"imports Book"| models

    style service fill:#ffa,stroke:#333,stroke-dasharray: 5 5
    style routes fill:#afa,stroke:#333
```

## Database Schema

```mermaid
erDiagram
    BOOKS {
        uuid uid PK "uuid4, primary key"
        varchar title "book title"
        varchar author "author name"
        varchar publisher "publisher name"
        varchar publish_date "stored as string e.g. 1998"
        integer page_count "total pages"
        varchar language "e.g. English"
        timestamp creation "row creation time"
        timestamp updated_on "last update time"
    }
```

## API Contract

```mermaid
graph TD
    subgraph Endpoints
        E1["GET /"]
        E2["GET /api/v1/books/"]
        E3["POST /api/v1/books/"]
        E4["GET /api/v1/books/{book_id}"]
        E5["PATCH /api/v1/books/{book_id}"]
        E6["DELETE /api/v1/books/{book_id}"]
    end

    subgraph Schemas
        BM["BookModel<br/>(full response)"]
        BCM["BookCreateModel<br/>(unused)"]
        BUM["BookUpdateModel<br/>(all fields required)"]
    end

    E2 -->|"response_model"| BM
    E3 -->|"request body: BookModel<br/>(should be BookCreateModel)"| BM
    E5 -->|"request body"| BUM

    style BCM fill:#faa,stroke:#333,stroke-dasharray: 5 5
```

## Current Data Flow (In-Memory)

```mermaid
sequenceDiagram
    participant C as Client
    participant R as Routes
    participant M as In-Memory List
    participant F as data.json

    Note over F,M: On server startup
    F->>M: Load 10 seed books at import time

    C->>R: GET /api/v1/books/
    R->>M: Return entire list
    M-->>C: 200 OK [books...]

    C->>R: POST /api/v1/books/
    R->>M: Append new book dict
    M-->>C: 201 Created {book}

    C->>R: GET /api/v1/books/3
    R->>M: Linear scan for id=3
    M-->>C: 200 OK {book}

    C->>R: PATCH /api/v1/books/3
    R->>M: Linear scan + dict.update()
    M-->>C: 200 OK {updated}

    C->>R: DELETE /api/v1/books/3
    R->>M: Linear scan + list.remove()
    M-->>C: 204 No Content
```

## Target Data Flow (PostgreSQL + Service Layer)

```mermaid
sequenceDiagram
    participant C as Client
    participant R as Routes
    participant S as BookService
    participant DB as PostgreSQL

    Note over R: FastAPI Depends()<br/>provides AsyncSession

    C->>R: GET /api/v1/books/
    R->>S: get_all_books(session)
    S->>DB: SELECT * FROM books
    DB-->>S: rows
    S-->>R: List[BookModel]
    R-->>C: 200 OK

    C->>R: POST /api/v1/books/
    R->>S: create_book(session, BookCreateModel)
    S->>DB: INSERT INTO books ...
    DB-->>S: created row
    S-->>R: BookModel
    R-->>C: 201 Created

    C->>R: PATCH /api/v1/books/{uid}
    R->>S: update_book(session, uid, BookUpdateModel)
    S->>DB: UPDATE books SET ... WHERE uid=?
    DB-->>S: updated row
    S-->>R: BookModel
    R-->>C: 200 OK

    C->>R: DELETE /api/v1/books/{uid}
    R->>S: delete_book(session, uid)
    S->>DB: DELETE FROM books WHERE uid=?
    DB-->>S: confirmed
    R-->>C: 204 No Content
```

## Migration Status

```mermaid
graph TD
    subgraph Done["Completed"]
        A1["FastAPI app + lifespan"]
        A2["pydantic-settings config"]
        A3["Async engine setup"]
        A4["SQLModel Book model"]
        A5["Pydantic schemas"]
    end

    subgraph InProgress["In Progress"]
        B1["In-memory CRUD routes"]
    end

    subgraph Todo["Not Implemented"]
        C1["BookService methods"]
        C2["DB session dependency"]
        C3["Routes wired to service"]
        C4["Seed data inserted to DB"]
        C5["UUID-based lookups"]
        C6["Tests"]
    end

    Done --> InProgress --> Todo

    style Done fill:#afa,stroke:#333
    style InProgress fill:#ffa,stroke:#333
    style Todo fill:#faa,stroke:#333,stroke-dasharray: 5 5
```
