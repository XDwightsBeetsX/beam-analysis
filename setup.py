import pathlib
from setuptools import setup, find_packages

# PACKAGE NAME
PKGNAME = "beam-analysis"

# VERSION
V = "1.0.0"

# AUTHOR
AUTH = "John Gutierrez"

# Short Description
SHORT_DESCR = "Perform engineering analysis on a beam"
LONG_DESCR = SHORT_DESCR  # placeholder

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README_FILE = "README.md"
README = (HERE / README_FILE).read_text()

# The text of the REQUIREMENTS file
REQUIREMENTS = []
REQUIREMENTS_FILE = f"{str(HERE)}/REQUIREMENTS.txt"
with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as req:
    lines = req.readlines()
    for line in lines:
        if line[0] != "#" and line.strip() != "":
            REQUIREMENTS.append(line.strip())

# GET README FOR LONG_DESCR
with open(README_FILE, "r", encoding="utf-8") as readme:
    LONG_DESCR = readme.read()

# SETUP
setup(
    name=PKGNAME,
    version=V,
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
