# AWS (EC2) Deployment

## Live Server

The application is deployed and accessible at:

```
http://35.156.68.160:8000
```

## Swagger

```
http://35.156.68.160:8000/docs
```

Same Swagger UI as local — login with test credentials, authorize with token, use endpoints.

## Postman

Import files from `postman/` directory (see [Local Setup — Postman](local-setup.md#postman) for instructions). Select the **EC2** environment in the top-right corner — all requests will point to `http://35.156.68.160:8000`.

## CI/CD Pipeline

Deployment is automated via GitHub Actions (`.github/workflows/deploy.yml`).

### On Pull Request to main:

1. **test** — installs dependencies, runs pytest
2. **smoke-test** — builds Docker image, starts container, checks `/liveness` endpoint

Both must pass before the PR can be merged.

### On Push to main (after merge):

1. **test** — runs pytest
2. **build-and-push** — builds Docker image, pushes to AWS ECR
3. **deploy** — SSH into EC2, pulls new image from ECR, restarts containers

### Infrastructure

| Component | Details |
|---|---|
| Container Registry | AWS ECR (`797890596022.dkr.ecr.eu-central-1.amazonaws.com/notes-manager`) |
| Server | AWS EC2 (t3.medium, Ubuntu, eu-central-1) |
| Static IP | 35.156.68.160 (Elastic IP) |
| Ports | 22 (SSH), 8000 (API) |

### GitHub Secrets

The following secrets are configured in the repository:

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user credentials |
| `AWS_SECRET_ACCESS_KEY` | IAM user credentials |
| `AWS_REGION` | eu-central-1 |
| `ECR_REPOSITORY` | notes-manager |
| `EC2_HOST` | 35.156.68.160 |
| `EC2_SSH_KEY` | SSH private key for EC2 |