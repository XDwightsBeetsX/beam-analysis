# beam_analysis

[![Build Status](https://travis-ci.com/XDwightsBeetsX/beam-analysis.svg?token=ojR96vWaxNB8o4NF9oGN&branch=master)](https://travis-ci.com/XDwightsBeetsX/beam-analysis)
 [![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/XDwightsBeetsX/beam-analysis.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/XDwightsBeetsX/beam-analysis/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/XDwightsBeetsX/beam-analysis.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/XDwightsBeetsX/beam-analysis/alerts/)

Perform engineering analysis on beams with diagrams for shear, moments, angle, and deflection  

## Usage

```shell
pip install beam_analysis
```

```shell
git clone https://github.com/XDwightsBeetsX/beam-analysis
```

### Continuous development using `twine`

```shell
python setup.py sdist bdist_wheel
twine upload dist/* -u {SECRET :)} -p {SECRET :)}
```

## Mechanical Requirements

- 2-D beams only  
- All loads and reactions must be inputted (no solving)  
- Boundary conditions currently required
  - must include one angle and one deflection condition
- Beam weight can be represented by a distributed load (not default)

## Build Requirements

- Check the `requirements.txt`:
  - `numpy`
  - `matplotlib`

## Samples

### Modeling Cantilever Beam

```python
# define beam parameters
E = 207 * 10**9
I = 2 * 10**-8
L = 1.0

# make the beam and add loads
B = Beam(L, E, I)
B.addPointLoad(0, 11)
B.addPointLoad(1, -10)
B.addAppliedMoment(0, 11*1.0)
B.addDistributedLoad(0, 1, -1.0)

# boundary conditions are required for angle and deflection analysis
B.addBoundaryCondition(0.0, "angle", 0.0)
B.addBoundaryCondition(0.0, "deflection", 0.0)

# run the analysis
B.analyze()
```
![image](https://user-images.githubusercontent.com/55027279/110195643-3ccd7980-7e04-11eb-8d6a-df83fc0e20db.png)
 
```shell
running...
E = 207000000000Pa
I = 2e-08m^4
L = 1.0m

**************************************** Analysis ****************************************
[BEAM_ANALYSIS] - [SINGULARITY] - running shear analysis: 11 + 0 + -1.0<x-0> + -10
[BEAM_ANALYSIS] - [SINGULARITY] - running moment analysis: 11<x-0> + 11.0 + (-1.0/2)<x-0>^2 + -10<x-1>
[BEAM_ANALYSIS] - [SINGULARITY] - running angle analysis: (11/2)<x-0>^2 + 11.0<x-0> + (-1.0/6)<x-0>^3 + (-10/2)<x-1>^2
[BEAM_ANALYSIS] - [SINGULARITY] - angle c1 found: 0.0
[BEAM_ANALYSIS] - [SINGULARITY] - running deflection analysis: (11/6)<x-0>^3 + (11.0/2)<x-0>^2 + (-1.0/24)<x-0>^4 + (-10/6)<x-1>^3
[BEAM_ANALYSIS] - [SINGULARITY] - deflection c1 found: 0.0
[BEAM_ANALYSIS] - [SINGULARITY] - deflection c2 found: 0.0
******************************************************************************************

REPORT:
Max shear:          11.0     [N]    @  0.0 [m]
Max moment:         21.5     [N-m]  @  1.0 [m]
Max angle:          -0.00395 [rad]  @  1.0 [m]
Max deflection:     -0.00176 [m]    @  1.0 [m]
```

### Modeling 3-pt Bending Beam

```python
# define beam parameters
E = 207 * 10**9
I = 2 * 10**-8
L = 1.0

# make the beam and add loads
B = Beam(L, E, I)
B.addPointLoad(0, 11)
B.addPointLoad(1, 11)
B.addPointLoad(0.5, -21)
B.addDistributedLoad(0, 1, -1.0)

# boundary conditions are required for angle and deflection analysis
B.addBoundaryCondition(0.5, "angle", 0.0)
B.addBoundaryCondition(0.0, "deflection", 0.0)

# run the analysis
B.analyze()
```

![image](https://user-images.githubusercontent.com/55027279/110196372-aef48d00-7e09-11eb-84d5-bf0972b2fe3a.png)

```shell
running...
E = 2.070e+04 [MPa]
I = 2.000e-08 [m^4]
L = 1.000 [m]

**************************************** Analysis ****************************************
[BEAM_ANALYSIS] - [SINGULARITY] - running shear analysis: 11 + -1.0<x-0> + -21 + 11
[BEAM_ANALYSIS] - [SINGULARITY] - running moment analysis: 11<x-0> + (-1.0/2)<x-0>^2 + -21<x-0.5> + 11<x-1>
[BEAM_ANALYSIS] - [SINGULARITY] - running angle analysis: (11/2)<x-0>^2 + (-1.0/6)<x-0>^3 + (-21/2)<x-0.5>^2 + (11/2)<x-1>^2
[BEAM_ANALYSIS] - [SINGULARITY] - angle c1 found: -1.3541666666666667
[BEAM_ANALYSIS] - [SINGULARITY] - running deflection analysis: (11/6)<x-0>^3 + (-1.0/24)<x-0>^4 + (-21/6)<x-0.5>^3 + (11/6)<x-1>^3
[BEAM_ANALYSIS] - [SINGULARITY] - deflection c1 found: -1.3541666666666667
[BEAM_ANALYSIS] - [SINGULARITY] - deflection c2 found: 0.0
******************************************************************************************

REPORT:
Max shear:          11.0     [N]    @  0.0 [m]
Max moment:         5.36974  [N-m]  @ 0.499 [m]
Max angle:          0.00033  [rad]  @  0.0 [m]
Max deflection:     0.00011  [m]    @ 0.499 [m]
```