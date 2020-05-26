# load libs
from setuptools import setup
import productionize

# read in README.md
with open("description.md", "r") as fh:
    long_description = fh.read()

# catch the version
current_version = productionize.__version__

# define the setup
setup(name='productionize',
      version=current_version,
      description='Lightweight ML Deployment Platform',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/LJStroemsdoerfer/productionize',
      author='Lukas Jan Stroemsdoerfer',
      author_email='ljstroemsdoerfer@gmail.com',
      license='MIT',
      packages=['productionize'],
      zip_safe=False)