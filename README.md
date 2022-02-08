# beam-analysis

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![PyPI version](https://badge.fury.io/py/beam-analysis.svg)](https://badge.fury.io/py/beam-analysis)
[![Build Status](https://app.travis-ci.com/XDwightsBeetsX/beam-analysis.svg?branch=master)](https://app.travis-ci.com/XDwightsBeetsX/beam-analysis)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/XDwightsBeetsX/beam_analysis.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/XDwightsBeetsX/beam_analysis/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/XDwightsBeetsX/beam_analysis.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/XDwightsBeetsX/beam_analysis/alerts/)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FXDwightsBeetsX%2Fbeam-analysis&count_bg=%233D75C8&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=views&edge_flat=false)](https://hits.seeyoufarm.com)

Perform engineering analysis on beams with diagrams for shear, moments, angle, and deflection  

## Usage 💻

### Install

```shell
pip install beam_analysis
```

```shell
git clone https://github.com/XDwightsBeetsX/beam-analysis
```

### Sample Code

```python
E = 207 * 10**6
L = 1.0
CS = CrossSection(CrossSectionTypes.CIRC, [.01])
B = Beam(L, E, crossSection=CS)

B.addPointLoad(0, 11, 45)
B.addPointLoad(L/2, -20, 45)
B.addPointLoad(L, 11, 45)
B.addDistributedLoad(0, L, -2, 45)

B.addBoundaryCondition(L/2, BoundaryConditionTypes.ANGLE, 0)
B.addBoundaryCondition(L, BoundaryConditionTypes.DEFLECTION, 0)

B.runAnalysis(outputToFile=True)
```

## Mechanical Requirements ⚙️⚠️

- Currently reactions are not solved for...
  - All loads and reactions must be inputted
- Boundary conditions currently required
  - one angle *AND* one deflection value
  - *OR* two deflection parameters
- Beam weight is not accounted for by default
  - represent it with a distributed load

***Check out some demos [here 📂](beam_analysis/docs/demos.md)!***

***If you run into usage problems, double check the [requirements.txt 📄](requirements.txt)***

## Continuous development using `twine` 👷🛠️

This project is maintained on [PYPI](https://pypi.org/project/beam-analysis/) via releases through twine...

```shell
python setup.py sdist bdist_wheel
twine upload -r testpypi dist/* -u $username -p $password
twine upload -r pypi dist/* -u $username -p $password
```
