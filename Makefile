PYTHON ?= python

.PHONY: dist
dist:
	$(PYTHON) setup.py sdist bdist_wheel

.PHONY: upload
upload:
	$(PYTHON) -m twine upload dist/*


.PHONY: test
test:
	pytest

