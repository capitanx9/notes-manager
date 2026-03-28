install:
	@test -f .env || cp .env.example .env
	@if grep -q 'your-secret-key-here' .env 2>/dev/null; then \
		sed -i '' "s/your-secret-key-here/$$(openssl rand -hex 32)/" .env; \
		echo "Generated JWT_SECRET_KEY in .env"; \
	fi
	$(POETRY) install --no-root

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
	@$(POETRY) env info