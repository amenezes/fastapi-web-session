.DEFAULT_GOAL := about
VERSION := $(shell cat fastapi_web_session/__init__.py | grep '__version__ ' | cut -d'"' -f 2)

lint:
ifeq ($(SKIP_STYLE), )
	@echo "> running isort..."
	isort fastapi_web_session
	isort tests
	isort examples
	@echo "> running black..."
	black fastapi_web_session
	black tests
	black examples
endif
	@echo "> running flake8..."
	flake8 fastapi_web_session
	flake8 tests
	@echo "> running mypy..."
	mypy fastapi_web_session

tests:
	@echo "> unittest"
	python -m pytest -vv --no-cov-on-fail --color=yes --durations=10 --cov-report xml --cov-report term --cov=fastapi_web_session tests

docs:
	@echo "> generate project documentation..."
	@cp README.md docs/index.md
	mkdocs build
	mkdocs serve

about:
	@echo "> fastapi_web_session: $(VERSION)"
	@echo ""
	@echo "make lint         - Runs: [isort > black > flake8 > mypy]"
	@echo "make tests        - Runs: tests."
	@echo "make ci           - Runs: [lint > tests]"
	@echo "make docs         - Generate project documentation."
	@echo ""
	@echo "mailto: alexandre.fmenezes@gmail.com"

ci: lint tests
ifeq ($(GITHUB_HEAD_REF), false)
	@echo "> download CI dependencies"
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	@echo "> uploading report..."
	codecov --file coverage.xml -t $$CODECOV_TOKEN
	./cc-test-reporter format-coverage -t coverage.py -o codeclimate.json
	./cc-test-reporter upload-coverage -i codeclimate.json -r $$CC_TEST_REPORTER_ID
endif

all: ci


.PHONY: lint tests ci docs install-deps tox all
