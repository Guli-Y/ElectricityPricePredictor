# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

test:
	@coverage run -m pytest tests/*.py

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr electricity_price_predictor-*.dist-info
	@rm -fr electricity_price_predictor.egg-info

install:
	@pip install . -U

all: clean install test


uninstall:
	@python setup.py install --record files.txt
	@cat files.txt | xargs rm -rf
	@rm -f files.txt

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u lologibus2

pypi:
	@twine upload dist/* -u lologibus2
