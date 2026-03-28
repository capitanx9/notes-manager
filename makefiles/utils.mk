# =============================================================================
#  Utilities
# =============================================================================

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache dist build *.egg-info
	find . -name "*.pyc" -delete
	@echo "Clean done."