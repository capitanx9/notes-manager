# =============================================================================
#  Local Docker Environment
#
#  Commands for managing the local Docker containers (FastAPI + PostgreSQL).
#  These commands build and run the application inside Docker.
#  No Poetry or Python installation required — only Docker.
#
#  On first run, .env is created automatically from .env.example
#  with a randomly generated JWT_SECRET_KEY.
# =============================================================================

setup-env:
	@test -f .env || cp .env.example .env
	@if grep -q 'your-secret-key-here' .env 2>/dev/null; then \
		sed -i '' "s/your-secret-key-here/$$(openssl rand -hex 32)/" .env; \
		echo "Generated JWT_SECRET_KEY in .env"; \
	fi

run: setup-env
	docker-compose up --build

stop:
	docker-compose down

restart:
	docker-compose down -v
	docker-compose up --build

.PHONY: docs
docs:
	open http://localhost:8000/docs
