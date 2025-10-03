.. Chức năng: Trang chủ API Reference
   Liệt kê tất cả các modules và classes

API Reference
=============

This section contains the complete API reference for all modules and classes.

Overview
--------

The Python Auto Grader PBT provides several grading modules:

**Core Graders**

* :doc:`basic_grader` - Simple unit test-based grading
* :doc:`io_grader` - Input/output comparison grading
* :doc:`weighted_grader` - Weighted test group grading
* :doc:`ast_grader` - Code quality analysis
* :doc:`property_based_grader` - Property-based testing grader
* :doc:`performance_grader` - Performance benchmarking
* :doc:`advanced_grader` - Integrated comprehensive grading

**Utilities**

* :doc:`plagiarism_detector` - Code similarity detection
* :doc:`utils` - Utility functions

Module Index
------------

.. toctree::
   :maxdepth: 2

   basic_grader
   io_grader
   weighted_grader
   ast_grader
   property_based_grader
   plagiarism_detector
   performance_grader
   advanced_grader
   utils

Quick Reference
---------------

Basic Grader
~~~~~~~~~~~~

.. code-block:: python

   from src.basic_grader import BasicGrader
   
   grader = BasicGrader("student_file.py")
   result = grader.grade(test_cases)

Property-Based Grader
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.property_based_grader import PropertyBasedGrader
   
   grader = PropertyBasedGrader("student_file.py")
   grader.test_commutativity("func", strategy)
   result = grader.grade()

Advanced Grader
~~~~~~~~~~~~~~~

.. code-block:: python

   from src.advanced_grader import AdvancedGrader
   
   grader = AdvancedGrader("student_file.py")
   result = grader.grade_comprehensive()

Common Patterns
---------------

Pattern 1: Simple Grading
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.basic_grader import BasicGrader
   
   test_cases = [
       {'function': 'add', 'inputs': [1, 2], 'expected': 3}
   ]
   
   grader = BasicGrader("student.py")
   result = grader.grade(test_cases, max_score=10.0)

Pattern 2: Property Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.property_based_grader import PropertyBasedGrader
   from hypothesis import strategies as st
   
   grader = PropertyBasedGrader("student.py")
   grader.test_with_oracle("sort", sorted, st.lists(st.integers()))
   result = grader.grade()

Pattern 3: Batch Grading
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.advanced_grader import BatchGrader
   
   batch = BatchGrader()
   batch.grade_directory("submissions/", "*.py")
   batch.export_batch_results("results.csv")

See Also
--------

* :doc:`../guides/index` - User guides and tutorials
* :doc:`../examples/index` - Complete examples
