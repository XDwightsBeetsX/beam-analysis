import pathlib
from setuptools import setup

# Package name
PKGNAME = "beam-analysis"

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# The text of the REQUIREMENTS file
REQUIREMENTS = (HERE / "REQUIREMENTS.txt").read_text()

# This call to setup() does all the work
setup(
    name=PKGNAME,
    version="1.0.0",
    description="Perform engineering analysis on a beam",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/XDwightsBeetsX/beam-analysis",
    author="John Gutierrez",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8.5",
    ],
    packages=[f"{PKGNAME}"],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            f"{PKGNAME}=Beam.__main__:main",
        ]
    },
)