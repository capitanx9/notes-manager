install:
	@test -f .env || cp .env.example .env
	@if grep -q 'your-secret-key-here' .env 2>/dev/null; then \
		sed -i '' "s/your-secret-key-here/$$(openssl rand -hex 32)/" .env; \
		echo "Generated JWT_SECRET_KEY in .env"; \
	fi
	@if ! command -v poetry >/dev/null 2>&1; then \
		echo "Poetry not found. Installing..."; \
		curl -sSL https://install.python-poetry.org | python3 -; \
	fi
	poetry install --no-root

run:
	docker-compose up --build

stop:
	docker-compose down

restart:
	docker-compose down -v
	docker-compose up --build

docs:
	open http://localhost:8000/docs

info:
	@poetry env info