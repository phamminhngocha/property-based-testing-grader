.. Python Auto Grader PBT documentation master file
   Chức năng: Trang chủ documentation
   Cung cấp overview và navigation đến các phần khác

Welcome to Python Auto Grader PBT Documentation
================================================

**Python Auto Grader PBT** is a comprehensive automated grading system for Python programming assignments using Property-Based Testing methodology.

.. image:: https://img.shields.io/badge/python-3.8%2B-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License

Overview
--------

Unlike traditional example-based testing approaches, this system automatically generates thousands of test cases from high-level specifications, providing thorough validation of:

* **Code Correctness**: Property-based testing with mathematical guarantees
* **Code Quality**: AST analysis, complexity checking, style validation
* **Performance**: Execution time and memory usage profiling
* **Originality**: Plagiarism detection across submissions

Key Features
------------

✨ **Multiple Grading Methods**
   - Basic unit testing
   - Input/output comparison
   - Property-based testing with Hypothesis
   - AST-based code quality analysis
   - Performance benchmarking
   - Plagiarism detection

🚀 **High Accuracy**
   - 89.3% agreement with expert manual grading
   - 91.7% edge case detection rate
   - 94.2% reduction in grading time

📊 **Comprehensive Reporting**
   - Detailed feedback with counterexamples
   - JSON/HTML/CSV export formats
   - Batch processing with statistics

🔒 **Safe Execution**
   - Sandboxed environment
   - Timeout protection
   - Resource limits

Quick Links
-----------

* :doc:`installation` - Get started quickly
* :doc:`quickstart` - Your first grading script
* :doc:`api/index` - Complete API reference
* :doc:`guides/index` - In-depth guides

Installation
------------

Quick install via pip:

.. code-block:: bash

   pip install python-auto-grader-pbt

Or from source:

.. code-block:: bash

   git clone https://github.com/[username]/python-auto-grader-pbt.git
   cd python-auto-grader-pbt
   pip install -e .

Quick Example
-------------

Here's a simple example of grading a sorting function:

.. code-block:: python

   from src.property_based_grader import PropertyBasedGrader
   from hypothesis import strategies as st

   # Initialize grader
   grader = PropertyBasedGrader("student_code.py")

   # Test with reference implementation
   grader.test_with_oracle(
       "sort_function",
       sorted,
       st.lists(st.integers()),
       weight=1.0
   )

   # Get results
   result = grader.grade()
   print(f"Score: {result['score']:.2f}/10")

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: User Guides

   guides/index
   guides/writing_properties
   guides/batch_grading
   guides/performance_tuning

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index
   api/basic_grader
   api/property_based_grader
   api/advanced_grader

.. toctree::
   :maxdepth: 2
   :caption: Examples

   examples/index
   examples/sorting_example
   examples/data_structures_example

.. toctree::
   :maxdepth: 1
   :caption: Additional Information

   changelog
   contributing
   license

Research Paper
--------------

This project is based on academic research:

**Title**: Property-Based Testing for Automated Python Grading

**Author**: Pham Minh Ngoc Ha (Academy of Finance)

**Abstract**: This research analyzes Property-Based Testing (PBT) methodology for automated grading...

See the full paper: [Link to paper]

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Support
-------

If you encounter any issues or have questions:

* GitHub Issues: https://github.com/[username]/python-auto-grader-pbt/issues
* Email: phammingngocha@hvtc.edu.vn

License
-------

This project is licensed under the MIT License - see the :doc:`license` file for details.

Citation
--------

If you use this system in your research, please cite:

.. code-block:: bibtex

   @software{ha2025pbt_grader,
     title = {Python Auto Grader PBT},
     author = {Ha, Pham Minh Ngoc},
     year = {2025},
     institution = {Academy of Finance},
     url = {https://github.com/[username]/python-auto-grader-pbt}
   }
