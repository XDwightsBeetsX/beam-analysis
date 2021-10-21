# beam-analysis

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![PyPI version](https://badge.fury.io/py/beam-analysis.svg)](https://badge.fury.io/py/beam-analysis)
[![Build Status](https://app.travis-ci.com/XDwightsBeetsX/beam-analysis.svg?branch=master)](https://app.travis-ci.com/XDwightsBeetsX/beam-analysis)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/XDwightsBeetsX/beam_analysis.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/XDwightsBeetsX/beam_analysis/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/XDwightsBeetsX/beam_analysis.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/XDwightsBeetsX/beam_analysis/alerts/)

Perform engineering analysis on beams with diagrams for shear, moments, angle, and deflection  

## Usage 💻

```shell
pip install beam_analysis
```

```shell
git clone https://github.com/XDwightsBeetsX/beam-analysis
```

## Mechanical Requirements ⚙️⚠️

- Currently reactions are not solved for...
  - All loads and reactions must be inputted
- Boundary conditions currently required
  - one angle *AND* one deflection value
  - *OR* two deflection parameters
- Beam weight is not accounted for by default
  - represent it with a distributed load

***Check out some demos [here 📂](docs/demos.md)!***

***If you run into usage problems, double check the [requirements.txt 🔐](requirements.txt)***

## Continuous development using `twine` 👷🛠️

This project is maintained on [PYPI](https://pypi.org/project/beam-analysis/) via releases through twine...

```shell
python setup.py sdist bdist_wheel
twine upload -r testpypi dist/* -u $username -p $password
twine upload -r pypi dist/* -u $username -p $password
```
