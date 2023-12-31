.. _getting-started:

Getting Started
===============

This section will provide some starting points for using the library.

For installation instructions, see :ref:`installation`.

.. _getting-started-hydro:

Hydro
-----

This module contains the tools for one-dimensional hydro models. See below for some basic usage examples.  

Hydro1D
^^^^^^^

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

.. raw:: html

   <iframe src="_static/hydro_1d.html" height=650px" width="100%"></iframe>

Model files can be written by providing either a ``pd.DataFrame``, ``dict`` or several ``np.ndarray``.

.. _getting-started-rt:

RT
--

`(Not yet implemented)`

.. _getting-started-tracer:

Tracer
------

`(Not yet implemented)`
