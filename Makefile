PYTHON ?= python3

.PHONY: verify figures setup

setup:
	$(PYTHON) -m pip install -r analysis/requirements.txt

verify:
	$(PYTHON) analysis/verify_release.py

figures:
	$(PYTHON) analysis/regenerate_figures.py
