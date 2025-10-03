.. Chức năng: Hướng dẫn cài đặt chi tiết
   Giải thích các phương pháp cài đặt khác nhau

Installation Guide
==================

This page provides detailed instructions for installing Python Auto Grader PBT.

Requirements
------------

System Requirements
~~~~~~~~~~~~~~~~~~~

* **Python**: 3.8 or higher
* **pip**: Latest version recommended
* **Git**: For installation from source (optional)
* **Operating System**: Windows, macOS, or Linux

Python Dependencies
~~~~~~~~~~~~~~~~~~~

The system requires the following Python packages:

* ``hypothesis`` >= 6.92.0 - Property-based testing framework
* ``pytest`` >= 7.4.0 - Testing framework
* ``pytest-cov`` >= 4.1.0 - Coverage plugin
* ``pytest-timeout`` >= 2.2.0 - Timeout handling

See ``requirements.txt`` for the complete list.

Installation Methods
--------------------

Method 1: Install from PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
   This method is not yet available until the package is published to PyPI.

.. code-block:: bash

   pip install python-auto-grader-pbt

Method 2: Install from GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Step 1**: Clone the repository

.. code-block:: bash

   git clone https://github.com/[username]/python-auto-grader-pbt.git
   cd python-auto-grader-pbt

**Step 2**: Create a virtual environment (recommended)

.. code-block:: bash

   # Create virtual environment
   python -m venv venv

   # Activate on Windows
   venv\Scripts\activate

   # Activate on macOS/Linux
   source venv/bin/activate

**Step 3**: Install the package

.. code-block:: bash

   # Install in development mode
   pip install -e .

   # Or install normally
   pip install .

Method 3: Install from ZIP
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Step 1**: Download the ZIP file from GitHub

**Step 2**: Extract the ZIP file

**Step 3**: Navigate to the extracted directory

.. code-block:: bash

   cd python-auto-grader-pbt-main

**Step 4**: Install

.. code-block:: bash

   pip install .

Development Installation
------------------------

For developers who want to contribute:

.. code-block:: bash

   # Clone repository
   git clone https://github.com/[username]/python-auto-grader-pbt.git
   cd python-auto-grader-pbt

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows

   # Install with dev dependencies
   pip install -e ".[dev]"

   # Verify installation
   pytest

This installs additional tools for development:

* ``black`` - Code formatter
* ``flake8`` - Linting tool
* ``mypy`` - Type checker
* ``pylint`` - Code quality checker

Verifying Installation
----------------------

To verify that the installation was successful:

.. code-block:: python

   # Test import
   from src.property_based_grader import PropertyBasedGrader
   from src.advanced_grader import AdvancedGrader

   print("Installation successful!")

Or run the test suite:

.. code-block:: bash

   pytest tests/

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Import Error: No module named 'hypothesis'**

Solution: Install hypothesis manually

.. code-block:: bash

   pip install hypothesis

**Permission Denied Error**

Solution: Use ``--user`` flag

.. code-block:: bash

   pip install --user python-auto-grader-pbt

**Python Version Too Old**

Solution: Upgrade Python to 3.8 or higher

.. code-block:: bash

   # Check Python version
   python --version

**SSL Certificate Error**

Solution: Use ``--trusted-host`` flag

.. code-block:: bash

   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org python-auto-grader-pbt

Getting Help
~~~~~~~~~~~~

If you encounter issues not covered here:

1. Check the `GitHub Issues <https://github.com/[username]/python-auto-grader-pbt/issues>`_
2. Create a new issue with:
   - Python version
   - Operating system
   - Full error message
   - Steps to reproduce

Next Steps
----------

After installation, proceed to:

* :doc:`quickstart` - Learn basic usage
* :doc:`guides/index` - Explore detailed guides
* :doc:`examples/index` - See practical examples
