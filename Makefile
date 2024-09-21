.PHONY: build clean test

clean:
	rm -f dist/*

format:
	isort src/runmd
	black src/runmd

lint:
	pylint src/runmd --exit-zero

build:
	python -m build
	pip install --force-reinstall dist/*.whl

test:
	pytest --cov=runmd --cov-report html tests/

prebuild: format lint

all: clean prebuild build test