Installation Guide
==================

Requirements
------------

* Python 3.8 or higher
* PyQt6 6.4.0 or higher

Installation Methods
--------------------

From PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~

Install the latest stable version from PyPI:

.. code-block:: bash

    pip install pyqt6-widgets-library

From Source
~~~~~~~~~~~

For development or to get the latest features:

.. code-block:: bash

    git clone https://github.com/madhusudanmewada/pyqt6-widgets-library.git
    cd pyqt6-widgets-library
    pip install -e .

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

If you plan to contribute or modify the library:

.. code-block:: bash

    git clone https://github.com/madhusudanmewada/pyqt6-widgets-library.git
    cd pyqt6-widgets-library
    pip install -e ".[dev]"

This installs additional development dependencies including:

* pytest for testing
* black for code formatting
* mypy for type checking
* flake8 for linting

Wheel Package Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have a wheel file:

.. code-block:: bash

    pip install pyqt6_widgets_library-1.1.0-py3-none-any.whl

Verification
------------

Verify your installation by running:

.. code-block:: python

    import pyqt_widgets
    print("PyQt6 Widgets Library installed successfully!")

Or run the demo application:

.. code-block:: bash

    pyqt6-widgets-demo

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**ImportError: No module named 'PyQt6'**

Make sure PyQt6 is installed:

.. code-block:: bash

    pip install PyQt6

**Qt platform plugin error**

On Linux, you might need additional packages:

.. code-block:: bash

    sudo apt-get install python3-pyqt6.qtwidgets

**Permission denied on macOS**

Use user installation:

.. code-block:: bash

    pip install --user pyqt6-widgets-library

Virtual Environment (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's recommended to use a virtual environment:

.. code-block:: bash

    python -m venv pyqt_env
    source pyqt_env/bin/activate  # On Windows: pyqt_env\Scripts\activate
    pip install pyqt6-widgets-library

Uninstallation
--------------

To remove the library:

.. code-block:: bash

    pip uninstall pyqt6-widgets-library