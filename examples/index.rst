.. Chức năng: Trang chủ Examples
   Giới thiệu và liệt kê tất cả các examples

Examples Gallery
================

This section contains practical, real-world examples demonstrating how to use the grading system.

Overview
--------

Examples are organized by assignment type and difficulty level:

* **Beginner**: Simple functions and basic algorithms
* **Intermediate**: Data structures and moderate complexity
* **Advanced**: Complex algorithms and system design

Example Categories
------------------

.. toctree::
   :maxdepth: 2

   sorting_example
   data_structures_example
   mathematical_functions_example
   string_processing_example
   graph_algorithms_example
   file_processing_example

Quick Reference
---------------

Sorting Algorithms
~~~~~~~~~~~~~~~~~~

Learn how to grade sorting implementations with:

* Property-based testing
* Performance benchmarking
* Custom invariants

:doc:`sorting_example`

Data Structures
~~~~~~~~~~~~~~~

Grade implementations of:

* Stacks and Queues
* Linked Lists
* Trees and Graphs

:doc:`data_structures_example`

Mathematical Functions
~~~~~~~~~~~~~~~~~~~~~~

Test mathematical functions with:

* Algebraic properties
* Numerical accuracy
* Edge cases

:doc:`mathematical_functions_example`

String Processing
~~~~~~~~~~~~~~~~~

Grade string manipulation with:

* Pattern matching
* Transformation validation
* Unicode handling

:doc:`string_processing_example`

Graph Algorithms
~~~~~~~~~~~~~~~~

Test graph algorithms including:

* DFS and BFS
* Shortest paths
* Minimum spanning trees

:doc:`graph_algorithms_example`

File Processing
~~~~~~~~~~~~~~~

Grade file handling code:

* Reading and writing
* Error handling
* Data validation

:doc:`file_processing_example`

Example Structure
-----------------

Each example includes:

1. **Assignment Description**: What students need to implement
2. **Student Code**: Sample submission to grade
3. **Grading Script**: Complete grading implementation
4. **Reference Solution**: Correct implementation for comparison
5. **Expected Output**: What the grader should produce
6. **Variations**: Alternative approaches and configurations

Running Examples
----------------

All examples can be run directly:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/[username]/python-auto-grader-pbt.git
   cd python-auto-grader-pbt

   # Navigate to examples
   cd examples/sorting_assignment/

   # Run the grader
   python grade_sorting.py

Complete Example Structure
--------------------------

.. code-block:: text

   examples/
   ├── sorting_assignment/
   │   ├── assignment.md           # Assignment description
   │   ├── student_code.py         # Student submission
   │   ├── reference_solution.py   # Correct implementation
   │   ├── grade_sorting.py        # Grading script
   │   └── README.md              # Instructions
   ├── data_structures/
   │   ├── stack_implementation/
   │   ├── queue_implementation/
   │   └── linked_list/
   └── ...

Next Steps
----------

* Start with :doc:`sorting_example` for beginners
* See :doc:`data_structures_example` for intermediate level
* Explore :doc:`graph_algorithms_example` for advanced topics
* Check :doc:`../api/index` for API details
