# Project Structure

```
notes-manager/
├── src/notes_manager/
│   ├── main.py                    # FastAPI app, router registration
│   ├── config.py                  # Settings from .env (pydantic-settings)
│   ├── database.py                # SQLAlchemy engine, session factory
│   ├── dependencies/
│   │   ├── auth.py                # get_current_user, require_role
│   │   └── database.py            # get_db dependency
│   ├── models/
│   │   ├── user.py                # User model
│   │   └── article.py             # Article model
│   ├── schemas/
│   │   ├── auth.py                # LoginRequest, TokenResponse
│   │   ├── user.py                # UserResponse, UserUpdate, UserListResponse
│   │   └── article.py             # ArticleCreate/Update/Response/ListResponse
│   ├── services/
│   │   ├── auth_service.py        # JWT, password hashing, authentication
│   │   ├── user_service.py        # User business logic, permission checks
│   │   └── article_service.py     # Article business logic, permission checks
│   ├── repositories/
│   │   ├── user_repository.py     # User DB queries
│   │   └── article_repository.py  # Article DB queries
│   └── routers/
│       ├── auth_router.py         # POST /auth/login
│       ├── user_router.py         # /users endpoints
│       └── article_router.py      # /articles endpoints
├── tests/
│   ├── conftest.py                # Test fixtures (DB, client, users, tokens)
│   └── unit/
│       ├── test_liveness.py
│       ├── test_auth.py
│       ├── test_articles.py
│       └── test_users.py
├── docs/                          # Documentation
├── init.sql                       # Database schema + seed data
├── Dockerfile
├── docker-compose.yaml            # Local development
├── .github/workflows/deploy.yml   # CI/CD pipeline
├── postman/
│   ├── collection.json            # Postman API requests
│   ├── environment_localhost.json # Postman localhost variables
│   └── environment_ec2.json       # Postman EC2 variables
├── makefiles/
│   ├── app.mk                     # run, stop, restart, docs (Docker)
│   ├── test.mk                    # install, test, coverage (Poetry)
│   └── utils.mk                   # clean
├── .env.example                   # Environment variables template
├── pyproject.toml                 # Dependencies (Poetry)
└── README.md
```

## Architecture

The application follows a 3-layer architecture:

```
Router → Service → Repository → Database
```

- **Routers** — HTTP layer. Receives requests, validates input via Pydantic schemas, calls services
- **Services** — business logic. Permission checks, error handling, orchestration
- **Repositories** — data access. Raw database queries via SQLAlchemy ORM

## Environment Variables

See `.env.example`:

| Variable | Description |
|---|---|
| `POSTGRES_USER` | PostgreSQL username |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `POSTGRES_DB` | PostgreSQL database name |
| `DATABASE_URL` | Full connection string for SQLAlchemy |
| `JWT_SECRET_KEY` | Secret key for signing JWT tokens |

`make install` automatically copies `.env.example` to `.env` and generates a random `JWT_SECRET_KEY`. Other values have sensible defaults for local development.

## Database

Tables and seed data are created by `init.sql`, which PostgreSQL executes on first startup via Docker's `docker-entrypoint-initdb.d` mechanism.

The ORM models in `src/notes_manager/models/` map to these tables but do not create them — `init.sql` is the source of truth for the database schema.