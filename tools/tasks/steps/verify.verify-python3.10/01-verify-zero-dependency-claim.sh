python -c "import sys; print(f'Python {sys.version}')"
# Confirm no external packages are imported
python -m py_compile aacte/*.py run_demo.py verify_demo.py
