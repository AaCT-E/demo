.PHONY: run verify clean test lint format

run:
	python run_demo.py

verify:
	python verify_demo.py

test: run verify

clean:
	rm -rf outputs/*.json __pycache__ aacte/__pycache__ .pytest_cache

lint:
	python -m py_compile aacte/*.py run_demo.py verify_demo.py

format:
	@echo "No formatter configured (zero-dependency policy)."
