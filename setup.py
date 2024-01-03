from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A useless prograrm for people with ocd.'
LONG_DESCRIPTION = 'A package that organizes your python imports into third party imports, built-in imports, local imports.'

# Setting up
setup(
    name="pretty_imports",
    version=VERSION,
    author="aabansen",
    author_email="crescentrayyt@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['stdlib-list'],
    keywords=['python', 'imports', 'pretty', 'organize'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)