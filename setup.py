from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]


setup(name='electricity_price_predictor',
      version="1.0",
      description="Module for forecasting 2days-ahead electricity prices in DK1",
      url = 'https://github.com/Guli-Y/ElectricityPricePredictor',
      author = 'Guli-Y',
      author_email = 'g.yimingjiang@gmail.com',
      packages=find_packages(),
      test_suite = 'tests',
      install_requires=requirements,
      include_package_data=True,
      scripts=['scripts/electricity_price_predictor-run'],
      zip_safe=False)
