MODULE := magic
BLUE='\033[0;34m'
NC='\033[0m'

run:
	@python -m $(MODULE)

test:
	@pytest

lint:
	@echo "\n${BLUE}Running Pylint against source and test files...${NC}\n"
	@pylint --rcfile=setup.cfg **/*.py || true
	@echo "\n${BLUE}Running Flake8 against source and test files...${NC}\n"
	@flake8 || true
	@echo "\n${BLUE}Running Bandit against source files...${NC}\n"
	@bandit -r --ini setup.cfg || true

clean:
	rm -rf .pytest_cache .coverage .pytest_cache coverage.xml

.PHONY: clean test