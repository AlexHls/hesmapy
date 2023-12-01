.. _installation:

Installation
============

In case you don't have a Python environment set up, create one using

.. code-block:: bash

   python3 -m venv hesmapy
   source hesmapy/bin/activate

Other environments are also possible, e.g. using Anaconda.
The minimum required Python version is 3.11.

Install the package using pip:

.. code-block:: bash

   pip install hesmapy

If you want to use the latest development version, you can install it directly from GitHub:

.. code-block:: bash

   git clone https://github.com/AlexHls/hesmapy
   cd hesmapy
   pip install -e .

This should install all dependencies automatically.
If you want to build the documentation, you also need to install the documentation dependencies:

.. code-block:: bash

   pip install sphinx sphinx-book-theme sphinx-copybutton
