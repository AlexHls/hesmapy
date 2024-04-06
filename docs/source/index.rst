.. Hesmapy documentation master file, created by
   sphinx-quickstart on Thu Nov 30 13:18:42 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Hesmapy's documentation!
===================================

.. image:: _static/landing.png
        :alt: Hesmapy Landing Image

.. image:: https://img.shields.io/pypi/v/hesmapy.svg
        :target: https://pypi.python.org/pypi/hesmapy
        :alt: PyPI version

.. image:: https://img.shields.io/pypi/dm/hesmapy
        :target: https://pypi.python.org/pypi/hesmapy
        :alt: PyPI - Downloads

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.10935383.svg
        :target: https://doi.org/10.5281/zenodo.10935383

Hesmapy is a Python package providing a set of tools to work with the data from the HESMA.
It introduces a new data sturcture for the HESMA data in an attempt to make the data more accessible and easier to work with.
For the more simple data, tools such as plotting are provided.
These utilities, however, are mostly intended for use by HESMA iself and might be rather limited in their functionality.
Moreover it provides loaders for the more complex data types such as raw binary data and HDF5 files.

Contents
--------

.. toctree::
    :maxdepth: 1

    installation
    getting_started
    writers


API Reference
-------------

.. toctree::
   :maxdepth: 2

   modules/modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
