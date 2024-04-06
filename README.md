# Hesmapy

![PyPI - Version](https://img.shields.io/pypi/v/hesmapy)
![PyPI - Downloads](https://img.shields.io/pypi/dm/hesmapy)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10404977.svg)](https://doi.org/10.5281/zenodo.10404977)

HESMA Python - Tools for reading HESMA models

## Documentation
Full documentation can be found [here](https://alexhls.github.io/hesmapy/).

## Installation
Currently, the package is only available through ``pip``.
```
pip install hesmapy
```

In case you want to build the documentation, you'll need to install the optional dependencies as well.
See ``pyproject.toml`` for a list of needed packages (mostly ``sphinx`` related packages)

## Contents
``hesmapy`` contains three main modules, one for each of the main HESMA categories (Hydro, RT, Tracer).
It provides utilties to read and write files in the standardised HESMA file formats, as well as
some utilities such as plotting. These utilities are mostly intended for use by HESMA itself and 
might be rather limited in their functionality.

### Hydro

#### Hydro1D
This module contains the tools for one-dimensional hydro models. See below for some basic usage examples.  

Loading models:
```python
import hesmapy.base as hp
model = hp.load_hydro_1d("examples/hydro/hydro_1d.json")
```
Get the data from a model as a ``pd.DataFrame``:
```python
df = model.get_data()
```
Plot a model:
```
model.plot(show_plot=True)
```
Model files can be written by providing either a ``pd.DataFrame``, ``dict`` or several ``np.ndarray``.
See the documentation for more details.

### RT

#### Lightcurves
This module contains the tools for lightcurves and data derived from them. See below for some basic usage examples.

Loading models:
```python
import hesmapy.base as hp
model = hp.load_rt_lightcurve("examples/rt/rt_lightcurve.json")
```
Get the data from a model as a ``pd.DataFrame``:
```python
df = model.get_data()
```
Plot a model:
```
model.plot(show_plot=True)
```

#### Lightcurves
This module contains the tools for spectra(l timeseries). See below for some basic usage examples.

Loading models:
```python
import hesmapy.base as hp
model = hp.load_rt_spectrum("examples/rt/rt_spectrum.json")
```
Get the data from a model as a list of ``pd.DataFrame`` (one for each timestep):
```python
dfs = model.get_data()
```
Plot a model:
```
model.plot(show_plot=True)``````


Model files can be written by providing either a ``pd.DataFrame``, ``dict`` or several ``np.ndarray``.
See the documentation for more details.

### Tracer
*(Not yet implemented)*

