#.EXPORT_ALL_VARIABLES
SHELL:=/usr/bin/env bash

PROJECT_NAME ?= extract_financial_data
DOWNLOAD_DIR=/tmp
PYTHON3_VERSION=$(shell python3 --version | grep -oE '3\.[7-9]')
VENV_DIR='.venv'
PACKAGE_FILE_NAME?=$(PROJECT_NAME)
TIME_STAMP=$(shell date +"%y%m%d")
STACK_TIMESTAMP:=$(TIME_STAMP)

ifeq "$(PYTHON3_VERSION)" ""
$(error 'At least Python 3.7 is required.')
endif

######################
# Help
######################
define PROJECT_HELP_MSG
Usage:
	make help                       show this message.
								    To install run "make install". It''s recommended to run "make createVirtualEnvironment" and enter the virtual environment first.

	make clean                      remove intermediate files (see CLEANUP)

	make installForLocalDev         make a virtualenv in the base directory (see createVirtualEnvironment) and install dependencies.
	make createVirtualEnvironment   create a virtual environment in '${VENV_DIR}'.

	make list                       list all targets.

	make packageLambda              will package this repo for deployment to lambda. Best run in a fresh clone/install. This will install packages not avaiable in AWS Lambda to the current dir.

	make installVariableReplacer    will install variable replacer, making it avaiable by calling `replacer`

	make test						will run all unit tests and integration tests.

	make unitTestDebug              will run the unit tests in debug mode.

	make openReport                 will generate the unit test code coverage report and open it in Chrome.

	make lint                       will run all linters.

	make clean                      will delete all temporary files for this repo.
endef
export PROJECT_HELP_MSG

.PHONY: help
help:
	@printf "%s" "$$PROJECT_HELP_MSG" | less



######################
# Install Helpers
######################
.PHONY: install
install: requirements.txt
	@pip install -r requirements.txt

.PHONY: createVirtualEnvironment
createVirtualEnvironment:
	@test -d .venv || python3 -m venv --prompt $(PROJECT_NAME) ./$(VENV_DIR)
	@echo 'Environment created. Run "source ./$(VENV_DIR)/bin/activate" to activate the virtual environment.\n"deactivate" to exit it.'

.PHONY: installForLocalDev
installForLocalDev: createVirtualEnvironment requirements.txt
	@$(VENV_DIR)/bin/pip install --upgrade --requirement requirements.txt
	@echo 'Local install complete'



########################
# Testing & Lint
########################
TESTS_DIR=tests/unit
MIN_TEST_COVERAGE ?= 0
UNIT_TEST_REPORT_COMMON_FLAGS =
COVERAGE_DIR='coverage_data'
TEST_RESULTS_JSON_FILE?=/tmp/testResults.json
TEST_RESULTS_XML_FOLDER?=/tmp/unit_test_xml_results
PYTHONPATH=$(shell echo "`pwd`:$$PYTHONPATH")

.PHONY: test
test: unitTest integrationTests
	@echo 'Testing complete'

.coverage: cleanCoverage
	@PYTHONBREAKPOINT=0 \
	PYTHONPATH=$(PYTHONPATH) \
	coverage run --branch -m unittest discover --verbose --pattern '*_test.py' --start-directory $(TESTS_DIR) --top-level-directory '.'

.PHONY: unitTest
unitTest: .coverage
	@echo

.PHONY: unitTestReport
unitTestReport: .coverage
	@coverage xml -o $(COVERAGE_DIR)/unit_test_coverage.xml
	@coverage html --skip-covered --directory=$(COVERAGE_DIR)/unit_test_coverage_html
	coverage report --skip-covered --show-missing

.PHONY: unitTestFailUnder
unitTestFailUnder: .coverage
	coverage report --fail-under=$(MIN_TEST_COVERAGE) --skip-covered --show-missing 1>/dev/null

.PHONY: unitTestDebug
unitTestDebug:
	PYTHONPATH=$(PYTHONPATH) \
    python -m unittest discover --verbose --pattern '*_test.py' --start-directory $(TESTS_DIR) --top-level-directory '.'

.PHONY: unitTestJSON
unitTestJSON: cleanCoverage cleanTestResults
	@PYTHONBREAKPOINT=0 \
	PYTHONPATH=$(PYTHONPATH) \
	coverage run --branch -m tests.utils.unittest.json discover --verbose --pattern '*_test.py' --start-directory $(TESTS_DIR) --top-level-directory '.' 2> $(TEST_RESULTS_JSON_FILE)

.PHONY: integrationTests
integrationTests:
	@echo 'No integration tests here.'


.PHONY: openReport
openReport: unitTestReport
	open -a "Google Chrome" file://`pwd`/$(COVERAGE_DIR)/unit_test_coverage_html/index.html

.phony: pylint
pylint:
	@echo '###### Pylint #######'
	@find . -type d -name '.venv' -prune -o -type d -name '.git' -prune -o -name '*.py' -print -exec pylint --jobs=0 "{}" +
	@echo '#####################'

.phony: flake8
flake8:
	@echo '###### Flake8 #######'
	@find . -type d -name '.venv' -prune -o -type d -name '.git' -prune -o -name '*.py' -print -exec flake8 --jobs=0 "{}" +
	@echo '#####################'

.PHONY: lint
lint: pylint flake8
	@echo 'Linting with Flake8 and Pylint complete'



##########################
# Clean up
##########################
.PHONY: cleanPyc
cleanPyc:
	@echo 'Cleaning pyc files...'
	@find ./ -name "*.pyc" -delete

.PHONY: cleanPyCache
cleanPyCache:
	@echo 'Cleaning __pycache__ files...'
	@find ./ -name "__pycache__" -type d -delete

.PHONY: cleanTmp
cleanTmp:
	@echo 'Cleaning tmp files...'

.PHONY: cleanCoverage
cleanCoverage:
	@echo 'Cleaning coverage files...'
	@rm -rf $(COVERAGE_DIR)
	@rm -f .coverage

.PHONY: cleanTestResults
cleanTestResults:
	rm -f $(TEST_RESULTS_JSON_FILE)
	rm -rf $(TEST_RESULTS_XML_FOLDER)

.PHONY: clean
clean: cleanPyc cleanTmp cleanPyCache cleanCoverage
	@echo 'Clean.'



######################
# Help System
######################
.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
