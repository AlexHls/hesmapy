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
| ------|-------------|------|----------|
| ``name`` | Name of the simulation, e.g. 'wd_m090_r0' | String | Yes |   
| ``schema`` | ``json`` schema used for the creation of the file | String | No |  
