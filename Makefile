# Makefile Luigi

# These targets are not files

.PHONY: all help check.test_path clean clean-build clean-others clean-luigi clean-pyc clean-test pep8 test test.dev test.failfirst test.collect test.skip.covered test.integration coverage coverage.html coveralls

all: help

help:
	@echo 'Makefile *** Super Dados *** Makefile'

check.test_path:
	@if test "$(TEST_PATH)" = "" ; then echo "TEST_PATH is undefined. The default is tests."; fi

clean: clean-build clean-others clean-pyc clean-test clean-luigi

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr .eggs/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +

clean-others:
	@find . -name 'Thumbs.db' -exec rm -f {} \;

clean-luigi:
	@find input/ -maxdepth 1 -mindepth 1 -type d -exec rm -rf '{}' \;
	@find output/ -maxdepth 1 -mindepth 1 -type d -exec rm -rf '{}' \;

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	@rm -fr .tox/
	@rm -f .coverage
	@rm -fr htmlcov/

pep8:
	@pycodestyle --filename="*.py" .

### TESTS

test: check.test_path
	@py.test -s $(TEST_PATH) --cov --cov-report term-missing --basetemp=tests/media --disable-pytest-warnings

test.dev: check.test_path
	@py.test -s $(TEST_PATH) --cov --cov-fail-under 70 --cov-report term-missing --basetemp=tests/media --disable-pytest-warnings

test.failfirst: check.test_path
	@py.test -s -x $(TEST_PATH) --basetemp=tests/media --disable-pytest-warnings

test.collect: check.test_path
	@py.test -s $(TEST_PATH) --basetemp=tests/media --collect-only --disable-pytest-warnings

test.skip.covered: check.test_path
	@py.test -s $(TEST_PATH) --cov --cov-report term:skip-covered --doctest-modules --basetemp=tests/media --disable-pytest-warnings

test.integration: check.test_path
	@py.test -s $(TEST_PATH) --integration --cov --cov-report term:skip-covered --doctest-modules --basetemp=tests/media --disable-pytest-warnings

coverage: check.test_path test

coverage.html: check.test_path
	@py.test -s $(TEST_PATH) --cov --cov-report html --doctest-modules --basetemp=tests/media --disable-pytest-warnings

coveralls: coverage
	@coveralls
