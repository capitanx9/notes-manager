# =============================================================================
#  Local Development Environment (Poetry)
#
#  Commands for setting up the local Python environment and running tests.
#  These are NOT required to run the application — Docker handles that.
#
#  Use these when you want to:
#  - Run tests locally before pushing (make test)
#  - Check code coverage before creating a PR (make coverage)
#
#  Prerequisites:
#  - Python 3.10+
#  - Poetry (auto-installed by make install if missing)
# =============================================================================

install:
	@if ! command -v poetry >/dev/null 2>&1; then \
		echo "Installing Poetry..."; \
		curl -sSL https://install.python-poetry.org | python3 - 2>/dev/null \
			&& echo "Poetry installed." \
			|| echo "Poetry installation failed. Requires Python 3.10+."; \
	fi
	@if command -v poetry >/dev/null 2>&1; then \
		poetry install --no-root; \
	fi

test:
	$(POETRY) run pytest -v --disable-warnings

coverage:
	$(POETRY) run pytest --cov=src/notes_manager --cov-report=term-missing --disable-warnings