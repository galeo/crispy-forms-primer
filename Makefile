.PHONY: build

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg
	@rm -fr *.egg-info


clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +


build:
	@python setup.py bdist_wheel
