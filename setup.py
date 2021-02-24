import pathlib
from setuptools import setup, find_packages

# PACKAGE NAME
PKGNAME = "beam-analysis"

# VERSION
V = "1.0.0"

# AUTHOR
AUTH = "John Gutierrez"

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# KEYWORDS about the pkg
KEYWORDS = ['beam', 'analysis', 'engineering']

# Short Description
SHORT_DESCR = "Perform engineering analysis on a beam"

# The text of the README file
README_FILE = str(HERE) + "/readme.md"
print(f"[LOG] - Searching for readme: '{README_FILE}'")
with open(README_FILE, "r", encoding="utf-8") as readme:
    LONG_DESCR = readme.read()
    print(f"[LOG] - Found readme")

# The text of the REQUIREMENTS file
REQUIREMENTS = []
REQUIREMENTS_FILE = str(HERE) + "/requirements.txt"
print(f"[LOG] - Searching for requirements: '{REQUIREMENTS_FILE}'")
with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as req:
    lines = req.readlines()
    for line in lines:
        if line[0] != "#" and line.strip() != "":
            REQUIREMENTS.append(line.strip())
    print(f"[LOG] - Found requirements")


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
    keywords=KEYWORDS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=("tests",)),
    python_requires='>=3.6',
)
