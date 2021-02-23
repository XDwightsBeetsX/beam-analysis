import pathlib
from setuptools import setup, find_packages

# PACKAGE NAME
PKGNAME = "beam-analysis"

# AUTHOR
AUTH = "John Gutierrez"

# Short Description
SHORT_DESCR = "Perform engineering analysis on a beam"
LONG_DESCR = SHORT_DESCR  # placeholder

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "readme.md").read_text()

# The text of the REQUIREMENTS file
REQUIREMENTS = (HERE / "requirements.txt").read_text()

# GET README FOR LONG_DESCR
with open("readme.md", "r", encoding="utf-8") as fh:
    LONG_DESCR = fh.read()

# SETUP
setup(
    name=PKGNAME,
    version="1.0.0",
    author=AUTH,
    description=SHORT_DESCR,
    long_description=LONG_DESCR,
    long_description_content_type="text/markdown",
    url="https://github.com/XDwightsBeetsX/beam-analysis",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(),
    python_requires='>=3.6',
)
