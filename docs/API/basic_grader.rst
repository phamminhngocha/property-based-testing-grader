.. Chức năng: API documentation cho BasicGrader
   Auto-generated từ docstrings

Basic Grader
============

.. automodule:: src.basic_grader
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The ``BasicGrader`` class provides simple unit test-based grading functionality.

Class Reference
---------------

.. autoclass:: src.basic_grader.BasicGrader
   :members:
   :special-members: __init__

Methods
-------

__init__(student_file)
~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: src.basic_grader.BasicGrader.__init__

load_student_code()
~~~~~~~~~~~~~~~~~~~

.. automethod:: src.basic_grader.BasicGrader.load_student_code

create_test_class(test_cases)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: src.basic_grader.BasicGrader.create_test_class

grade(test_cases, max_score)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: src.basic_grader.BasicGrader.grade

Usage Examples
--------------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from src.basic_grader import BasicGrader

   # Define test cases
   test_cases = [
       {
           'function': 'add',
           'inputs': [2, 3],
           'expected': 5
       },
       {
           'function': 'add',
           'inputs': [0, 0],
           'expected': 0
       }
   ]

   # Create grader
   grader = BasicGrader("student_code.py")

   # Grade the submission
   result = grader.grade(test_cases, max_score=10.0)

   # Print results
   print(f"Score: {result['score']}/{result['max_score']}")
   print(f"Passed: {result['passed']}/{result['total']}")

Multiple Functions
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   test_cases = [
       {'function': 'add', 'inputs': [1, 2], 'expected': 3},
       {'function': 'multiply', 'inputs': [2, 3], 'expected': 6},
       {'function': 'subtract', 'inputs': [5, 3], 'expected': 2},
   ]

   grader = BasicGrader("student_code.py")
   result = grader.grade(test_cases)

With Error Handling
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   grader = BasicGrader("student_code.py")
   
   try:
       result = grader.grade(test_cases)
       if 'error' in result:
           print(f"Error: {result['error']}")
       else:
           print(f"Score: {result['score']}")
   except Exception as e:
       print(f"Grading failed: {e}")

Return Value
------------

The ``grade()`` method returns a dictionary with:

.. code-block:: python

   {
       'score': float,              # Score achieved (0-max_score)
       'max_score': float,          # Maximum possible score
       'passed': int,               # Number of tests passed
       'total': int,                # Total number of tests
       'failures': int,             # Number of failed tests
       'errors': int,               # Number of tests with errors
       'details': {
           'failures': list,        # List of failure messages
           'errors': list           # List of error messages
       }
   }

Test Case Format
----------------

Each test case must be a dictionary with:

* ``function`` (str): Name of the function to test
* ``inputs`` (list): List of arguments to pass to the function
* ``expected`` (any): Expected return value

.. code-block:: python

   {
       'function': 'function_name',
       'inputs': [arg1, arg2, ...],
       'expected': expected_result
   }

Best Practices
--------------

1. **Test Edge Cases**: Include boundary values and special cases

   .. code-block:: python

      test_cases = [
          {'function': 'divide', 'inputs': [10, 2], 'expected': 5},
          {'function': 'divide', 'inputs': [0, 1], 'expected': 0},
          {'function': 'divide', 'inputs': [5, 1], 'expected': 5},
      ]

2. **Organize Test Cases**: Group related tests

   .. code-block:: python

      basic_tests = [...]
      edge_cases = [...]
      all_tests = basic_tests + edge_cases

3. **Use Descriptive Names**: Make test cases self-documenting

4. **Handle Errors Gracefully**: Check for 'error' key in results

Limitations
-----------

* Only tests return values (not side effects)
* Cannot test interactive programs
* Limited to deterministic functions
* No support for testing exceptions

See Also
--------

* :doc:`property_based_grader` - More comprehensive testing
* :doc:`io_grader` - For testing interactive programs
* :doc:`weighted_grader` - For weighted test groups
