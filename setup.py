from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content if 'git+' not in x]

setup(name='electricity_price_predictor',
      version="1.0",
      description="Project Description",
      packages=find_packages(),
      test_suite = 'tests',
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      scripts=['scripts/electricity_price_predictor-run'],
      zip_safe=False)




REQUIRED_PACKAGES = [
    'streamlit==0.65.2']

setup(
    name='StreamlitApp',
    version='1.0',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='Streamlit App'
)
