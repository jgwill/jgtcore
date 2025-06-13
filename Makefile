version := $(shell python3 -c 'import jgtcore; print(jgtcore.__version__)')

.PHONY: venv
venv:
	[ -d .venv ] || python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip

.PHONY: piplocal
piplocal:
	pip install -e '.[dev]'

.PHONY: develop
develop: venv piplocal

.PHONY: format
format:
	isort jgtcore tests *.py
	black jgtcore tests *.py

.PHONY: test
test:
	pytest tests/ -v
	coverage run -m pytest tests/
	coverage report

.PHONY: clean
clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -f
	rm -Rf dist
	rm -Rf build
	rm -Rf *.egg-info
	rm -Rf .pytest_cache
	rm -Rf .coverage

.PHONY: dist
dist: clean
	python3 -m build

.PHONY: pypi-release
pypi-release:
	twine upload dist/*

.PHONY: pre-release
pre-release:
	make dist
	make bump_version

.PHONY: release
release:
	git tag $(version)
	git push 
	git push --tags
	make pypi-release

.PHONY: dev-pypi-release
dev-pypi-release:
	twine --version
	twine upload --repository pypi-dev dist/*

.PHONY: dev-release
dev-release:
	make bump_version
	make dist
	make dev-pypi-release

.PHONY: dev-release-plus
dev-release-plus:
	make dev-release
	twine upload dist/*

.PHONY: bump_version
bump_version:
	python3 bump_version.py

.PHONY: quick-release
quick-release:
	make test
	make bump_version
	make dist
	make pypi-release
