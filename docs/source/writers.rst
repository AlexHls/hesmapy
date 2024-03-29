.. _writers:

Writing Hesmapy files
=====================

Hesmapy provides several functions to write hesma files, either from a ``pd.DataFrame``, a ``dict`` or several ``np.array``.
Internally, the ``dict`` and ``np.array`` are converted to a ``pd.DataFrame`` before writing the hesma file.
The following examples show how to write hesma files from a ``pd.DataFrame``, for the other variants please refer to the API documentation.

.. _writers-hydro:

Hydro
-----


Hydro1D
^^^^^^^

Assume you have some simulation data:

.. code-block:: python

    import pandas as pd

    data = pd.DataFrame(
        {
            "radius": [1, 2, 3, 4, 5],
            "density": [1, 2, 3, 4, 5],
            "pressure": [1, 2, 3, 4, 5],
            "temperature": [1, 2, 3, 4, 5],
            "mass": [1, 2, 3, 4, 5],
            "velocity": [1, 2, 3, 4, 5],
            "time": [1, 2, 3, 4, 5],
            "xHe": [0.1, 0.2, 0.3, 0.4, 0.5],
            "xNi56": [0.1, 0.2, 0.3, 0.4, 0.5],  
        }
    )

You can write this data to a hesma file using the following code:

.. code-block:: python

    from hesmapy.writers.hydro1d import write_hydro1d_from_dataframe

    write_hydro1d_from_dataframe(data, "hydro1d.json")

You can optionally provide additional information such as units, sources etc.:

.. code-block:: python

    write_hydro1d_from_dataframe(
        data,
        "hydro1d.json",
        model_name="My Model",
        units={"radius": "km", "density": "g/cm^3"},
        sources={"bibcode": "2018ApJ...853..107S"},
    )


.. _writers-rt:

RT
--

Lightcurves
^^^^^^^^^^^

Assume you have some simulation data:

.. code-block:: python

    import pandas as pd

    data = pd.DataFrame(
        {
            "time": [1, 2, 3, 1, 2, 3],
            "band": ["B", "B", "B", "V", "V", "V"],
            "magnitude": [1, 2, 3, 2, 3, 4],
            "e_magnitude": [0.1, 0.2, 0.3, 0.2, 0.3, 0.4],
            "viewing_angle": [-1, -1, -1, -1, -1, -1],
        }
    )

Note that the data is not split into different colums for each band and viewing angle.
Instead the data has to contain the band and viewing angle information in separate columns.
For angle averaged data, the viewing angle column shoud contain ``-1``.

You can write this data to a hesma file using the following code:

.. code-block:: python

    from hesmapy.writers.rt import write_lightcurves_from_dataframe

    write_lightcurves_from_dataframe(data, "lightcurves.json")

You can optionally provide additional information such as units, sources etc. as well as derived quantities:

.. code-block:: python

   derived_data = pd.DataFrame(
        {
            "peak_mag": [1, 2],
            "peak_time": [1, 2],
            "rise_time": [1, 2],
            "decline_rate_15": [1, 2],
            "decline_rate_40": [1, 2],
            "band": ["B", "V"],
            "viewing_angle": [-1, -1],
        }
    )

    write_lightcurves_from_dataframe(
        data,
        "lightcurves.json",
        derived_data=derived_data,
        model_name="My Model",
        units={"time": "days", "B": "mag"},
        sources={"bibcode": "2018ApJ...853..107S"},
    )

Note that the derived data has to contain the band and viewing angle information in separate columns as well.
The column names of the ``units`` dictionary should match the ``band`` names in the ``data`` and ``derived_data`` DataFrames.