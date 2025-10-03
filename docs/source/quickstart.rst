.. Chức năng: Hướng dẫn sử dụng nhanh
   Giúp người dùng bắt đầu trong 5 phút

Quick Start Guide
=================

This guide will get you started with Python Auto Grader PBT in 5 minutes.

Your First Grading Script
--------------------------

Step 1: Create a Student File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a file ``student_code.py`` with a simple function:

.. code-block:: python

   # student_code.py
   def add(a, b):
       """Add two numbers"""
       return a + b

   def sort_list(lst):
       """Sort a list"""
       return sorted(lst)

Step 2: Create a Grading Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create ``grade.py``:

.. code-block:: python

   from src.property_based_grader import PropertyBasedGrader
   from hypothesis import strategies as st

   # Initialize grader
   grader = PropertyBasedGrader("student_code.py")

   # Test 1: Commutativity of addition
   grader.test_commutativity("add", st.integers(), weight=0.3)

   # Test 2: Identity element (0 for addition)
   grader.test_identity("add", 0, st.integers(), weight=0.2)

   # Test 3: Correctness against reference
   grader.test_with_oracle(
       "sort_list",
       sorted,
       st.lists(st.integers()),
       weight=0.5
   )

   # Get results
   result = grader.grade()

   # Print report
   print(grader.generate_report())

Step 3: Run the Grader
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python grade.py

You should see output like:

.. code-block:: text

   ======================================================================
   PROPERTY-BASED TESTING GRADING REPORT
   ======================================================================
   Final Score: 8.50/10
   Tests Passed: 2/3

   ✓ PASS - commutativity
     Function: add
     Score: 10.00/10

   ✓ PASS - identity
     Function: add
     Score: 10.00/10

   ✗ FAIL - oracle
     Function: sort_list
     Score: 5.50/10
     Sample failures:
       - Input: [3, 1, 2]
         Student: [1, 2, 3]
         Oracle: [1, 2, 3]

Common Use Cases
----------------

Use Case 1: Basic Function Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.basic_grader import BasicGrader

   test_cases = [
       {'function': 'add', 'inputs': [2, 3], 'expected': 5},
       {'function': 'add', 'inputs': [0, 0], 'expected': 0},
       {'function': 'add', 'inputs': [-1, 1], 'expected': 0},
   ]

   grader = BasicGrader("student_code.py")
   result = grader.grade(test_cases)

   print(f"Score: {result['score']}/10")

Use Case 2: Input/Output Programs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.io_grader import IOGrader

   test_cases = [
       {'input': "5\n3\n", 'expected': "8\n"},
       {'input': "10\n-2\n", 'expected': "8\n"},
   ]

   grader = IOGrader("student_program.py")
   result = grader.grade(test_cases)

   print(grader.generate_report(result))

Use Case 3: Code Quality Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.ast_grader import ASTGrader

   grader = ASTGrader("student_code.py")

   structure_req = {
       'functions': 3,
       'classes': 1,
       'loops': 2
   }

   result = grader.grade(
       structure_requirements=structure_req,
       max_complexity=10
   )

   print(f"Code Quality Score: {result['score']:.2f}/10")

Use Case 4: Batch Grading
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.advanced_grader import BatchGrader

   batch = BatchGrader()

   # Grade all files in directory
   batch.grade_directory("submissions/", "student_*.py")

   # Print summary
   print(batch.generate_summary_report())

   # Export to CSV
   batch.export_batch_results("results.csv")

Next Steps
----------

Now that you've created your first grading script:

* Learn about :doc:`guides/writing_properties` - Write better property tests
* Explore :doc:`api/index` - Understand all available features
* Check :doc:`examples/index` - See more complex examples

Tips for Success
----------------

1. **Start Simple**: Begin with basic tests, then add complexity
2. **Use Multiple Methods**: Combine different grading approaches
3. **Provide Feedback**: Use detailed reports to help students learn
4. **Test Your Tests**: Verify graders work with correct code first
5. **Adjust Weights**: Balance different aspects based on assignment goals

Common Mistakes to Avoid
-------------------------

❌ **Don't**: Test with only trivial inputs

✅ **Do**: Use property-based testing to generate diverse test cases

❌ **Don't**: Give 100% weight to functionality

✅ **Do**: Consider code quality, performance, and documentation

❌ **Don't**: Run untrusted code without sandboxing

✅ **Do**: Use timeout and resource limits

Getting Help
------------

* Check :doc:`guides/index` for detailed documentation
* See :doc:`examples/index` for more examples
* Open an issue on `GitHub <https://github.com/[username]/python-auto-grader-pbt/issues>`_
