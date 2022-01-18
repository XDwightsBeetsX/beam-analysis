# beam-analysis

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![PyPI version](https://badge.fury.io/py/beam-analysis.svg)](https://badge.fury.io/py/beam-analysis)
[![Build Status](https://app.travis-ci.com/XDwightsBeetsX/beam-analysis.svg?branch=master)](https://app.travis-ci.com/XDwightsBeetsX/beam-analysis)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/XDwightsBeetsX/beam_analysis.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/XDwightsBeetsX/beam_analysis/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/XDwightsBeetsX/beam_analysis.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/XDwightsBeetsX/beam_analysis/alerts/)

Perform engineering analysis on beams with diagrams for shear, moments, angle, and deflection.

- [beam-analysis](#beam-analysis)
  - [Usage 💻](#usage-)
    - [Requirements ⚙️⚠️](#requirements-️️)
  - [Features](#features)
  - [Deployment with `twine` 👷🛠️](#deployment-with-twine-️)

## Usage 💻

```shell
pip install beam_analysis
```

```shell
git clone https://github.com/XDwightsBeetsX/beam-analysis
```

### Requirements ⚙️⚠️

- ***All loads and reactions must be inputted***
  - reaction loads are not solved for
- ***Boundary conditions required***
  - **one angle** *AND* **one deflection** value
  - *OR* **two deflection** parameters
- Beam weight is not accounted for by default
  - represent it with a distributed load

> ***If you run into usage problems, double check the [requirements.txt 🔐](requirements.txt)***  
> ***`numpy`*** and ***`matplotlib`*** are not default python libraries...

## Features

- Simple ***Beam construction*** from length ***`L`***, Young's modulus ***`E`***, and either a known, or calculated cross-section moment of inertia ***`I`***.

    ```python
    # cross-section with dimensions
    L = 3
    E = 207 * 10**6
    CS = CrossSection(CrossSectionTypes.CIRC, [.01])
    B = Beam(L, E, crossSection=CS)
    ```

    ```python
    # known properties
    L = 3
    E = 207 * 10**6
    I = 2 * 10**-4
    B = Beam(L, E, i=I)
    ```

- Easily add ***loads*** to the *`Beam`* in *XY* or *XZ* planes.

    ```python
    # general form of (location, magnitude, angle)
    B.addPointLoad(0, 10, 0)  # 0 deg -> XY plane
    B.addPointLoad(L, 10, 0)
    B.addDistributedLoad(0, L, -20, 90)  # 90 deg -> XZ plane
    B.addAppliedMoment(0, 5, 0)
    ```

- Add angle/deflection ***`BoundaryConditions`***.
  
    ```python
    B.addBoundaryCondition(L/2, BoundaryConditionTypes.ANGLE, 0)
    B.addBoundaryCondition(L, BoundaryConditionTypes.DEFLECTION, 0)
    ```

- ***Run*** the analysis! Optionally, write a ***results summary*** to file. This will be displayed in the console regardless.
  
    ```python
    B.runAnalysis(outputToFile=True)
    ```

  ***Check out some demos [here 📂](beam_analysis/docs/demos.md)!***

## Deployment with `twine` 👷🛠️

This project is maintained on [PYPI](https://pypi.org/project/beam-analysis/) via releases through twine...

1. update the ***`setup.py`*** with new version info and features.
2. upload the new version to ***PYPI***:

    ```shell
    python setup.py sdist bdist_wheel
    twine upload -r testpypi dist/* -u $username -p $password
    twine upload -r pypi dist/* -u $username -p $password
    ```
