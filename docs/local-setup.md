# Local Setup

## Requirements

- Docker & Docker Compose
- Make
- Poetry (optional, for running tests locally)

## Installation and Run

```bash
git clone https://github.com/capitanx9/notes-manager.git
cd notes-manager
make install    # copies .env.example → .env, generates JWT_SECRET_KEY, installs dependencies
make run        # builds and starts Docker containers (FastAPI + PostgreSQL)
```

The application will be available at `http://localhost:8000`.

`make install` does three things:
1. Copies `.env.example` to `.env` if it doesn't exist
2. Generates a random `JWT_SECRET_KEY` in `.env`
3. Installs Python dependencies via Poetry

## Swagger (API Documentation)

```bash
make docs
```

This opens `http://localhost:8000/docs` in the browser.

How to use:
1. Open Swagger UI
2. Expand `POST /auth/login` and click "Try it out"
3. Enter test user credentials (see [API & Permissions](api-permissions.md))
4. Copy the `access_token` from the response
5. Click "Authorize" at the top, paste the token
6. All protected endpoints are now accessible

## Postman

All Postman files are in the `postman/` directory:

```
postman/
├── collection.json              # all API requests
├── environment_localhost.json   # localhost variables
└── environment_ec2.json         # EC2 variables
```

How to import:

1. Open Postman → Workspaces → Create Workspace → Blank workspace
2. Click **Import** in the left sidebar
3. Drag and drop all 3 files from `postman/` (or select them manually)
4. Select the **localhost** environment in the top-right corner
5. Run `Login (admin)` request first — it automatically saves the token
6. All other requests will use the token automatically

## Tests

```bash
make test       # run all tests
make coverage   # run tests with coverage report
```

Tests use SQLite in-memory database — no Docker required.

## Make Commands

| Command | Description |
|---|---|
| `make install` | Copy .env, generate JWT secret, install dependencies |
| `make run` | Start Docker containers |
| `make stop` | Stop Docker containers |
| `make restart` | Recreate containers from scratch (resets database) |
| `make test` | Run tests |
| `make coverage` | Run tests with coverage report |
| `make docs` | Open Swagger UI in browser |
| `make info` | Show Poetry environment info |
| `make clean` | Remove cache and build artifacts |

## Stopping and Resetting

```bash
make stop       # stop containers (data preserved)
make restart    # stop, delete database volume, rebuild and start fresh
```

`make restart` is useful when you want to reset the database to its initial state (re-runs init.sql).