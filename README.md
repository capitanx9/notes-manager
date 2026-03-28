# Notes Manager

REST API for managing users and articles with role-based access control, built with FastAPI.

**Technologies:** FastAPI, SQLAlchemy, PostgreSQL, JWT, Docker, GitHub Actions, AWS (ECR + EC2)

## Quick Start

```bash
git clone https://github.com/capitanx9/notes-manager.git
cd notes-manager
make install
make run
```

Open Swagger UI: `make docs` or go to http://localhost:8000/docs

Login with `admin@example.com` / `password123` to get a JWT token.

## Documentation

- [Local Setup](docs/local-setup.md) — installation, running, testing, Postman
- [AWS Deployment](docs/aws-setup.md) — EC2 access, CI/CD pipeline
- [API & Permissions](docs/api-permissions.md) — roles, access rights, test users, endpoints
- [Project Structure](docs/project-structure.md) — file layout, environment variables