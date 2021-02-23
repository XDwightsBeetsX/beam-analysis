# beam-analysis  :construction_worker:  

[![Build Status](https://travis-ci.com/XDwightsBeetsX/beam-analysis.svg?token=ojR96vWaxNB8o4NF9oGN&branch=master)](https://travis-ci.com/XDwightsBeetsX/beam-analysis)  
Perform engineering analysis on beams with diagrams for shear, moments, angle, and deflection  

## Usage

```shell
pip install beam-analysis
```

### Continuous development using `twine`

```shell
python setup.py sdist
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
