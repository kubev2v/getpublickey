lint:
	isort --check src/*
	black --check src
    
format:
	isort src/*
	black src

test:
	python -m unittest src/test_*
