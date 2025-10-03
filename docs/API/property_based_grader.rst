.. Chức năng: API documentation cho PropertyBasedGrader

Property-Based Grader
=====================

.. automodule:: src.property_based_grader
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The ``PropertyBasedGrader`` uses Hypothesis to automatically generate thousands of test cases from property specifications.

Class Reference
---------------

.. autoclass:: src.property_based_grader.PropertyBasedGrader
   :members:
   :special-members: __init__

Core Methods
------------

test_commutativity(func_name, strategy, weight)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test if function is commutative: ``f(a,b) == f(b,a)``

.. automethod:: src.property_based_grader.PropertyBasedGrader.test_commutativity

**Parameters:**

* ``func_name`` (str): Name of function to test
* ``strategy``: Hypothesis strategy for generating inputs
* ``weight`` (float): Weight for scoring (default: 1.0)

**Example:**

.. code-block:: python

   from hypothesis import strategies as st
   
   grader.test_commutativity("add", st.integers(), weight=0.3)

test_associativity(func_name, strategy, weight)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test if function is associative: ``f(f(a,b),c) == f(a,f(b,c))``

.. automethod:: src.property_based_grader.PropertyBasedGrader.test_associativity

**Example:**

.. code-block:: python

   grader.test_associativity("add", st.integers(), weight=0.3)

test_identity(func_name, identity_value, strategy, weight)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test identity element: ``f(a, identity) == a``

.. automethod:: src.property_based_grader.PropertyBasedGrader.test_identity

**Example:**

.. code-block:: python

   # Test that 0 is identity for addition
   grader.test_identity("add", 0, st.integers(), weight=0.2)
   
   # Test that 1 is identity for multiplication
   grader.test_identity("multiply", 1, st.integers(), weight=0.2)

test_monotonicity(func_name, strategy, weight)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test monotonicity: ``a <= b => f(a) <= f(b)``

.. automethod:: src.property_based_grader.PropertyBasedGrader.test_monotonicity

test_idempotence(func_name, strategy, weight)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test idempotence: ``f(f(a)) == f(a)``

.. automethod:: src.property_based_grader.PropertyBasedGrader.test_idempotence

test_with_oracle(func_name, oracle, strategy, weight)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compare student function with reference implementation.

.. automethod:: src.property_based_grader.PropertyBasedGrader.test_with_oracle

**Example:**

.. code-block:: python

   # Compare with Python's built-in sorted
   grader.test_with_oracle(
       "my_sort",
       sorted,
       st.lists(st.integers()),
       weight=0.5
   )

test_custom_invariants(func_name, invariants, strategy, weight)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test custom invariant functions.

.. automethod:: src.property_based_grader.PropertyBasedGrader.test_custom_invariants

**Example:**

.. code-block:: python

   def is_sorted(input_list, output_list):
       return all(output_list[i] <= output_list[i+1] 
                  for i in range(len(output_list)-1))
   
   def is_permutation(input_list, output_list):
       return sorted(input_list) == sorted(output_list)
   
   grader.test_custom_invariants(
       "my_sort",
       [is_sorted, is_permutation],
       st.lists(st.integers()),
       weight=0.4
   )

Utility Methods
---------------

grade()
~~~~~~~

Calculate final score from all tests.

.. automethod:: src.property_based_grader.PropertyBasedGrader.grade

generate_report()
~~~~~~~~~~~~~~~~~

Generate detailed text report.

.. automethod:: src.property_based_grader.PropertyBasedGrader.generate_report

Complete Example
----------------

Grading a Sorting Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.property_based_grader import PropertyBasedGrader
   from hypothesis import strategies as st

   # Initialize grader
   grader = PropertyBasedGrader("student_sorting.py")

   # Define invariants
   def is_sorted(input_list, output_list):
       if len(output_list) <= 1:
           return True
       return all(output_list[i] <= output_list[i+1] 
                  for i in range(len(output_list)-1))

   def is_permutation(input_list, output_list):
       return sorted(input_list) == sorted(output_list)

   # Test 1: Idempotence (sorting twice gives same result)
   grader.test_idempotence(
       "my_sort",
       st.lists(st.integers(), max_size=50),
       weight=0.2
   )

   # Test 2: Compare with reference
   grader.test_with_oracle(
       "my_sort",
       sorted,
       st.lists(st.integers(), max_size=100),
       weight=0.4
   )

   # Test 3: Custom invariants
   grader.test_custom_invariants(
       "my_sort",
       [is_sorted, is_permutation],
       st.lists(st.integers(), max_size=100),
       weight=0.4
   )

   # Get results
   result = grader.grade()
   print(grader.generate_report())

Hypothesis Strategies
---------------------

Common strategies for test data generation:

Basic Types
~~~~~~~~~~~

.. code-block:: python

   from hypothesis import strategies as st

   # Integers
   st.integers()                      # Any integer
   st.integers(min_value=0)          # Non-negative
   st.integers(min_value=0, max_value=100)  # Range

   # Floats
   st.floats()
   st.floats(min_value=0.0, max_value=1.0)

   # Booleans
   st.booleans()

   # Text
   st.text()
   st.text(alphabet='abc', min_size=1, max_size=10)

Collections
~~~~~~~~~~~

.. code-block:: python

   # Lists
   st.lists(st.integers())
   st.lists(st.integers(), min_size=1, max_size=100)

   # Tuples
   st.tuples(st.integers(), st.text())

   # Dictionaries
   st.dictionaries(st.text(), st.integers())

   # Sets
   st.sets(st.integers())

Custom Strategies
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Non-empty lists
   non_empty_lists = st.lists(st.integers(), min_size=1)

   # Sorted lists
   sorted_lists = st.lists(st.integers()).map(sorted)

   # Positive integers
   positive_ints = st.integers(min_value=1)

   # Email addresses
   emails = st.emails()

Best Practices
--------------

1. **Choose Appropriate Properties**

   Good properties are:
   
   * Universal (true for all valid inputs)
   * Easy to check
   * Independent of implementation

2. **Use Multiple Properties**

   .. code-block:: python

      # Test multiple aspects
      grader.test_with_oracle(...)      # Correctness
      grader.test_idempotence(...)      # Stability
      grader.test_custom_invariants(...) # Specific requirements

3. **Set Reasonable Weights**

   .. code-block:: python

      grader.test_with_oracle(..., weight=0.5)      # 50%
      grader.test_commutativity(..., weight=0.3)    # 30%
      grader.test_identity(..., weight=0.2)         # 20%

4. **Limit Test Size**

   .. code-block:: python

      # For performance
      st.lists(st.integers(), max_size=100)

5. **Handle Edge Cases**

   .. code-block:: python

      # Include empty lists, None, etc.
      st.lists(st.integers(), min_size=0)

Return Value
------------

The ``grade()`` method returns:

.. code-block:: python

   {
       'score': float,                 # Final score (0-10)
       'max_score': float,             # Maximum (10.0)
       'total_score': float,           # Raw weighted score
       'max_possible': float,          # Max possible raw score
       'passed_tests': int,            # Number of passed tests
       'total_tests': int,             # Total tests run
       'test_results': [               # Detailed results
           {
               'test': str,            # Test name
               'passed': bool,         # Pass/fail status
               'score': float,         # Score for this test
               'function': str,        # Function tested
               'failures': list        # Sample failures (if any)
           },
           ...
       ]
   }

Common Pitfalls
---------------

1. **Non-deterministic Functions**

   Problem: Function uses random or time-dependent values
   
   Solution: Mock or control randomness

2. **Side Effects**

   Problem: Function modifies global state
   
   Solution: Use custom invariants to check state

3. **Slow Functions**

   Problem: Tests timeout
   
   Solution: Reduce max_examples or increase deadline

4. **Incorrect Properties**

   Problem: Property is too strict or too loose
   
   Solution: Test property with known-good code first

See Also
--------

* :doc:`../guides/writing_properties` - Guide to writing good properties
* `Hypothesis Documentation <https://hypothesis.readthedocs.io/>`_
* :doc:`basic_grader` - Simpler alternative
