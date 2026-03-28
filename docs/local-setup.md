# Local Setup

## Requirements

- Docker & Docker Compose
- Make

That's it. No Python or Poetry needed to run the application.

## Run the Application

```bash
git clone https://github.com/capitanx9/notes-manager.git
cd notes-manager
make run
```

On first run, `make run` automatically:
1. Creates `.env` from `.env.example`
2. Generates a random `JWT_SECRET_KEY`
3. Builds and starts Docker containers (FastAPI + PostgreSQL)

The application will be available at `http://localhost:8000`.

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

## Running Tests Locally (Optional)

Tests can be run locally without Docker. This requires Python 3.10+ and Poetry.

```bash
make install    # installs Poetry (if missing) and project dependencies
make test       # run all tests
make coverage   # run tests with coverage report
```

`make install` is only needed for local testing — it has nothing to do with running the application.

## Stopping and Resetting

```bash
make stop       # stop containers (data preserved)
make restart    # stop, delete database, rebuild and start fresh (re-runs init.sql)
```

## All Make Commands

### Application (Docker)

| Command | Description |
|---|---|
| `make run` | Create .env (if needed) and start Docker containers |
| `make stop` | Stop Docker containers |
| `make restart` | Recreate containers from scratch (resets database) |
| `make docs` | Open Swagger UI in browser |

### Testing (requires Poetry)

| Command | Description |
|---|---|
| `make install` | Install Poetry (if missing) and project dependencies |
| `make test` | Run tests |
| `make coverage` | Run tests with coverage report |

### Utilities

| Command | Description |
|---|---|
| `make clean` | Remove cache and build artifacts |