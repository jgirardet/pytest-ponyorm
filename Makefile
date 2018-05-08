.PHONY: build

MODULE:=pytest_ponyorm.py


dev:
	pipenv install -r requirements.txt --python 3.6 --skip-lock
	pipenv install -e . --skip-lock

style: isort yapf

isort:
	pipenv run isort -y

yapf:
	pipenv run yapf --recursive -i $(MODULE)

checks:
	pipenv check
	
deploy: build
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

build: sdist wheels

shell:
	pipenv run apistar shell

sdist:
	python setup.py sdist

wheels:
		python setup.py bdist_wheel

test:
	pipenv run pytest 

	
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -rf .pytest_cache/



# aliases to gracefully handle typos on poor dev's terminal
check: checks
devel: dev
develop: dev
dist: dists
install: install-system
pypi: pypi-publish
styles: style
test: test-unit
unittest: test-unit
wheel: wheels
