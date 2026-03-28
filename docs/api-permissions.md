# API & Permissions

## Test Users

All users are created via `init.sql` on first database startup.

| Email | Password | Role |
|---|---|---|
| admin@example.com | password123 | admin |
| editor@example.com | password123 | editor |
| user@example.com | password123 | user |

Users cannot be created through the API. New users can only be added via SQL queries.

## Roles

- **user** — can manage own articles, view others' articles, edit own profile
- **editor** — same as user, plus can edit any article (but cannot delete any)
- **admin** — full access to everything: all articles and all users

## Permissions Table

### Articles

| Action | user | editor | admin |
|---|---|---|---|
| View any article | yes | yes | yes |
| Create articles | yes | yes | yes |
| Edit own articles | yes | yes | yes |
| Edit any article | no | yes | yes |
| Delete own articles | yes | no | yes |
| Delete any article | no | no | yes |

### Users

| Action | user | editor | admin |
|---|---|---|---|
| GET /users/me | yes | yes | yes |
| List all users | no | no | yes |
| View any user | no | no | yes |
| Edit own profile | yes | yes | yes |
| Edit any user | no | no | yes |
| Change user roles | no | no | yes |
| Delete users | no | no | yes |

## Endpoints

### Auth

| Method | Path | Description | Auth |
|---|---|---|---|
| POST | /auth/login | Login, get JWT token | No |

### Articles

| Method | Path | Description | Auth |
|---|---|---|---|
| GET | /articles | List articles (limit, offset, search) | Yes |
| GET | /articles/{id} | Get article by ID | Yes |
| POST | /articles | Create article | Yes |
| PUT | /articles/{id} | Update article | Yes |
| DELETE | /articles/{id} | Delete article | Yes |

### Users

| Method | Path | Description | Auth |
|---|---|---|---|
| GET | /users/me | Get current user profile | Yes |
| GET | /users | List users (limit, offset, search) | Admin |
| GET | /users/{id} | Get user by ID | Admin |
| PUT | /users/{id} | Update user | Yes |
| DELETE | /users/{id} | Delete user | Admin |

### Health

| Method | Path | Description | Auth |
|---|---|---|---|
| GET | /liveness | Health check | No |

## Authentication Flow

1. `POST /auth/login` with email and password
2. Receive `access_token` in response
3. Pass token in `Authorization: Bearer <token>` header for all protected requests
4. Token expires in 30 minutes