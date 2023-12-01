=======
Hesmapy
=======

.. image:: https://badge.fury.io/py/hesmapy.svg
    :target: https://badge.fury.io/py/hesmapy
    :alt: Latest PyPI version

HESMA Python - Tools for reading HESMA models

Documentation
=============

Full documentation can be found [here](https://alexhls.github.io/hesmapy/).

Installation
============

Currently, the package is only available through ``pip``.

.. code-block:: bash

    pip install hesmapy

In case you want to build the documentation, you'll need to install the optional dependencies as well.
See ``pyproject.toml`` for a list of needed packages (mostly ``sphinx`` related packages)

Contents
========

``hesmapy`` contains three main modules, one for each of the main HESMA categories (Hydro, RT, Tracer).
It provides utilties to read and write files in the standardised HESMA file formats, as well as
some utilities such as plotting. These utilities are mostly intended for use by HESMA itself and 
might be rather limited in their functionality.

Hydro
-----

Hydro1D
^^^^^^^
This module contains the tools for one-dimensional hydro models. See below for some basic usage examples.  

Loading models:

.. code-block:: python

    import hesmapy.base as hp
    model = hp.load_hydro_1d("examples/hydro/hydro_1d.json")

Get the data from a model as a ``pd.DataFrame``:

.. code-block:: python

    df = model.get_data()

Plot a model:

.. code-block:: python

    model.plot(show_plot=True)

Model files can be written by providing either a ``pd.DataFrame``, ``dict`` or several ``np.ndarray``.
See the documentation for more details.

RT
--
`(Not yet implemented)`

Tracer
------
`(Not yet implemented)`
