test:
	$(POETRY) run pytest -v --disable-warnings

coverage:
	$(POETRY) run pytest --cov=src/notes_manager --cov-report=term-missing --disable-warnings
