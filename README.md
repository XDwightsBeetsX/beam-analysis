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
twine upload dist/*
```

## Mechanical Requirements

- Curently `E, I, & L` as well as added loads must be in SI units  

- All loads on the beam must be inputted  
  - This does no solving  

## Build Requirements

- Check the `requirements.txt`:
  - `numpy`
  - `matplotlib`

### Samples

![image](https://user-images.githubusercontent.com/55027279/108810029-ca40dc00-756f-11eb-8061-dd7638527273.png)  
