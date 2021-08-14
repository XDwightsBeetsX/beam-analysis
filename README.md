# beam-analysis

[![Build Status](https://travis-ci.com/XDwightsBeetsX/beam_analysis.svg?token=ojR96vWaxNB8o4NF9oGN&branch=master)](https://travis-ci.com/XDwightsBeetsX/beam_analysis)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/XDwightsBeetsX/beam_analysis.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/XDwightsBeetsX/beam_analysis/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/XDwightsBeetsX/beam_analysis.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/XDwightsBeetsX/beam_analysis/alerts/)  
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![PyPI version](https://badge.fury.io/py/beam-analysis.svg)](https://badge.fury.io/py/beam-analysis)
[![PyPi downloads](https://pypip.in/d/beam-analysis/badge.png)](https://crate.io/packages/beam-analysis/)

Perform engineering analysis on beams with diagrams for shear, moments, angle, and deflection  

## Usage

```shell
pip install beam-analysis
```

```shell
git clone https://github.com/XDwightsBeetsX/beam-analysis
```

***Check out some demos [here](beam_analysis/docs/demos.md)!***

***Double check the [requirements.txt](requirements.txt) if you run into usage problems***

## Mechanical Requirements

- Currently reactions are not solved for... :caution:
  - *All loads and reactions must be inputted*
- Boundary conditions currently required:
  - one angle *AND* one deflection parameter
  - *OR* two deflection parameters
- Beam weight is not accounted for by default
  - represent it with a distributed load

## Continuous development using `twine`

This project is maintained on PYPI via releases through twine...

```shell
python setup.py sdist bdist_wheel
twine upload -r testpypi dist/* -u $username -p $password
twine upload -r pypi dist/* -u $username -p $password
```
