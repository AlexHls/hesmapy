# The HESMA Database File Schema

While the HESMA database accepts various file formats, it is recommended to upload data in a HESMA supported file format.
Not only does this allow for automatic visualization on the HESMA website, but more importantly it avoids having to deal
with a zoo of different (and possibly incredibly hard to parse) file formats.

Each model type (Hydro, RT, Tracer) has its own specification, see below.
For basic list data such as light curves or 1D density profiles, the file format is at its core a pure ``json`` file.
For more complex or larger data, e.g. 3D hydro models, data is stored in ``HDF5`` files.
While it is not strictly necessary to follow the specifications and labels listed below, it is strongly recommended
to use these schema as other fields will not be parsed by HESMA.

The only exception to this rule are the tracer files. Due to their nature (i.e. being extremely large files), they are
stored as raw binaries. In order to avoid a scenario where these files become essentially data waste once the producing
source code is lost, we enforce the rule that each tracer file must have an accompanying file reader script (or at least
its own file specification), preferably integrated into the ``hesmapy`` package.

Example files can be found in the respective ``examples/`` subdirectory.

## RT

Each radiative transfer (RT) model file can contain various data, from lightcurves to spectra as well as metadata.
In general, the RT file schema closely follows the specifications of the
[Open Supernova Catalog Schema](https://github.com/astrocatalogs/schema) where applicable.

The primary entry is the model name, containing only one object, i.e. a minimal viable file contains:
```json
{
    "rt_model_name": {}
}
```

Additionally, specifying a ``schema`` key containing a permanent URL to the specific version of this document used in
creating a ``json`` file (containing the corresponding commithash), and a name key (identical to the object field name):
```json
{
    "rt_model_name": {
        "schema": "https://github.com/AlexHls/hesmapy/blob/initial/SCHEMA.md"
        "name": "rt_model_name"
    }
}
```

## Hydro

Hydrodynamical simulations are stored depending on the dimensionality of the data. In particular, one-dimensional
simulations are stored as plain-text ``json`` files, whereas two- or three-dimensional simulations are stored
as ``HDF5`` files.

### One-dimensional hydro simulations

The schema for one-dimensional hydro simulations is similar to that of RT models. The primary entry is the simulation
name, containing only one object, i.e. a minimal viable file contains:
```json
{
    "hydro_sim_name": {}
}
```

Additionally, specifying a ``schema`` key containing a permanent URL to the specific version of this document used in
creating a ``json`` file (containing the corresponding commithash), and a name key (identical to the object field name):
```json
{
    "hydro_sim_name": {
        "schema": "https://github.com/AlexHls/hesmapy/blob/initial/SCHEMA.md"
        "name": "hydro_sim_name"
    }
}
```

Each file may contain various properties:

| Field | Description | Type | Required |  
|-------|-------------|------|----------|
| ``name`` | Name of the simulation, e.g. 'wd_m090_r0' | String | Yes |   
| ``schema`` | ``json`` schema used for the creation of the file | String | No |  
| ``sources`` | Bibliographic resources which relate to the models stored in the file | Array | No |
| ``units`` | Physical units of the data stored in the file. Mostly used for the correct plot label display | Object | No |
| ``data`` | Model data containing various physical quantities and timesteps | Array | Yes |

To be usable by ``hesmapy`` (in a meaningful way), a file needs to contain at least the ``name`` and ``data`` fields.
The above listed array and object fields (``sources``, ``units``, ``data``) contain a variety of other fields as listed below:

``sources``:
A file can contain multiple sources if the data collectively was produced throughout multiple publications.
If, however, separate subsets of data have been produced by individual publications, consider splitting up the data
into multiple files to ensure proper attributing of each subset to an individual reference.

| Field | Description | Type | Required |
|-------|-------------|------|----------|
| ``bibcode`` | Bibcode of the reference. Preferably in the ADS style | String | No |
| ``reference`` | Display name of the reference, e.g. Pakmor et al. (2022) | String | No |
| ``url`` | URL of the specified reference, preferably a DOI is provided | String | No |

``units``:
While the data itself is stored agnostic to any unit system, it can be useful to provide information on the provided units
(especially if the data is not stored in cgs-units). This information is mostly used to display the correct labels in
plots, if none are provided plots will only show *arb. unit*. As such it is **strongly** discouraged to store data with
different physical units in the same file as it will be impossible to tell which data point has which unit.

| Field | Description | Type | Required |
|-------|-------------|------|----------|
| ``radius`` | Unit of the radius data field | String | No |
| ``density`` | Unit of the density data field | String | No |
| ``pressure`` | Unit of the pressure data field | String | No |
| ``temperature`` | Unit of the temperature data field | String | No |
| ``mass`` | Unit of the mass data field | String | No |
| ``velocity`` | Unit of the velocity data field | String | No |
| ``time`` | Unit of the time data field | String | No |

``data``:
This field contains the actual model data. While various quantities can be provided, not all need to be present. However,
plotting will only work for quantities that have the same length as the ``radius`` quantity. To pass the validation,
the ``radius``, ``density`` and ``time`` fields need to be present. This is again mostly to ensure that the plotting works
correctly, rather than an actual data required. Most other functionality will work if, e.g., only ``pressure``
is given (within reason). Furthermore, at least two data points are required in a valid model.

| Field | Description | Type | Required |
|-------|-------------|------|----------|
| ``radius`` | The radius data field | String | Yes |
| ``density`` | The density data field | String | Yes |
| ``pressure`` | The pressure data field | String | No |
| ``temperature`` | The temperature data field | String | No |
| ``mass`` | The mass data field | String | No |
| ``velocity`` | The velocity data field | String | No |
| ``time`` | The time data field | String | Yes |

In addition, various abundances can be specified. Here the field names need to follow the regular expression ``\bx[a-zA-Z]{1,2}[0-9]{0,3}\b``, i.e. combinations of one or two letters followed by up to three integers, with a 'x' suffix. E.g. ``xNi56``, ``xC12`` and ``xHe`` are valid abundance fields.
For a valid example file, see the template file ``examples/hydro/hydro_1d.json``.

*Note*: It might seem a little unintuitive to store the data in a 'per data point' scheme instead of an array based approach.
However, this approach is much more robust in terms of missing data and unevenly shaped data. In particular when it comes
to creating the interactive plots or DataFrames, this approach allows to just fill missing points with NaN values, instead
of having to deal with unevenly shaped arrays.
