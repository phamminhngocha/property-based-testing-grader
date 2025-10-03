.. Chức năng: Ví dụ grading data structures (Stack, Queue, LinkedList)

Data Structures Example
=======================

This example demonstrates grading implementations of basic data structures.

Assignment: Stack Implementation
---------------------------------

Assignment Description
~~~~~~~~~~~~~~~~~~~~~~

**Objective**: Implement a Stack data structure with the following operations:

* ``push(item)``: Add item to top of stack
* ``pop()``: Remove and return top item
* ``peek()``: Return top item without removing
* ``is_empty()``: Check if stack is empty
* ``size()``: Return number of items

**Requirements**:

1. Use a list as internal storage
2. Raise ``IndexError`` when popping from empty stack
3. All operations should be O(1) except size() which can be O(n)
4. Include docstrings

Student Code
~~~~~~~~~~~~

Good Implementation
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # student_stack_good.py
   """
   Stack implementation using list.
   Student: Alice
   """

   class Stack:
       """
       Stack implementation using Python list.
       
       Last-In-First-Out (LIFO) data structure.
       """
       
       def __init__(self):
           """Initialize empty stack."""
           self._items = []
       
       def push(self, item):
           """
           Add item to top of stack.
           
           Args:
               item: Item to add
           """
           self._items.append(item)
       
       def pop(self):
           """
           Remove and return top item.
           
           Returns:
               Top item from stack
               
           Raises:
               IndexError: If stack is empty
           """
           if self.is_empty():
               raise IndexError("pop from empty stack")
           return self._items.pop()
       
       def peek(self):
           """
           Return top item without removing.
           
           Returns:
               Top item from stack
               
           Raises:
               IndexError: If stack is empty
           """
           if self.is_empty():
               raise IndexError("peek at empty stack")
           return self._items[-1]
       
       def is_empty(self):
           """Check if stack is empty."""
           return len(self._items) == 0
       
       def size(self):
           """Return number of items in stack."""
           return len(self._items)

Buggy Implementation
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # student_stack_buggy.py
   """
   Stack with bugs.
   """

   class Stack:
       def __init__(self):
           self._items = []
       
       def push(self, item):
           self._items.append(item)
       
       def pop(self):
           # BUG: Doesn't check if empty
           return self._items.pop()
       
       def peek(self):
           return self._items[-1]
       
       def is_empty(self):
           # BUG: Wrong logic
           return len(self._items) > 0
       
       def size(self):
           return len(self._items)

Grading Script
--------------

Complete Stack Grading
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # grade_stack.py
   """
   Grade stack implementation using stateful testing.
   """

   from src.property_based_grader import PropertyBasedGrader
   from src.ast_grader import ASTGrader
   from hypothesis import strategies as st, given, settings
   from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
   import importlib.util

   class StackTester:
       """Test suite for Stack implementation."""
       
       def __init__(self, student_file):
           self.student_file = student_file
           self.load_student_class()
       
       def load_student_class(self):
           """Load student's Stack class."""
           spec = importlib.util.spec_from_file_location(
               "student_stack", self.student_file
           )
           module = importlib.util.module_from_spec(spec)
           spec.loader.exec_module(module)
           self.Stack = module.Stack
       
       def test_basic_operations(self):
           """Test basic push/pop operations."""
           stack = self.Stack()
           
           # Test empty stack
           assert stack.is_empty() == True, "New stack should be empty"
           assert stack.size() == 0, "New stack size should be 0"
           
           # Test push
           stack.push(1)
           assert stack.is_empty() == False, "Stack with item not empty"
           assert stack.size() == 1, "Size should be 1 after one push"
           assert stack.peek() == 1, "Peek should return pushed item"
           
           # Test multiple pushes
           stack.push(2)
           stack.push(3)
           assert stack.size() == 3, "Size should be 3"
           assert stack.peek() == 3, "Peek should return last pushed"
           
           # Test pop
           item = stack.pop()
           assert item == 3, "Pop should return last pushed item"
           assert stack.size() == 2, "Size should decrease after pop"
           
           return True
       
       def test_lifo_order(self):
           """Test Last-In-First-Out ordering."""
           stack = self.Stack()
           
           items = [1, 2, 3, 4, 5]
           for item in items:
               stack.push(item)
           
           popped = []
           while not stack.is_empty():
               popped.append(stack.pop())
           
           assert popped == list(reversed(items)), \
               "Should pop in LIFO order"
           
           return True
       
       def test_error_handling(self):
           """Test exception handling."""
           stack = self.Stack()
           
           # Pop from empty
           try:
               stack.pop()
               assert False, "Should raise IndexError on pop from empty"
           except IndexError:
               pass  # Expected
           
           # Peek at empty
           try:
               stack.peek()
               assert False, "Should raise IndexError on peek at empty"
           except IndexError:
               pass  # Expected
           
           return True
       
       @given(st.lists(st.integers()))
       @settings(max_examples=100)
       def test_property_size_matches_operations(self, items):
           """Property: size should match number of pushes."""
           stack = self.Stack()
           
           for item in items:
               stack.push(item)
           
           assert stack.size() == len(items), \
               "Size should match number of pushed items"
       
       @given(st.lists(st.integers(), min_size=1))
       @settings(max_examples=100)
       def test_property_peek_idempotent(self, items):
           """Property: peek should not change stack."""
           stack = self.Stack()
           
           for item in items:
               stack.push(item)
           
           size_before = stack.size()
           peeked1 = stack.peek()
           peeked2 = stack.peek()
           size_after = stack.size()
           
           assert peeked1 == peeked2, "Peek should return same value"
           assert size_before == size_after, "Peek shouldn't change size"
       
       def run_all_tests(self):
           """Run all tests and return results."""
           results = {
               'basic_operations': False,
               'lifo_order': False,
               'error_handling': False,
               'property_size': False,
               'property_peek': False,
           }
           
           # Basic tests
           try:
               results['basic_operations'] = self.test_basic_operations()
           except Exception as e:
               print(f"Basic operations failed: {e}")
           
           try:
               results['lifo_order'] = self.test_lifo_order()
           except Exception as e:
               print(f"LIFO order failed: {e}")
           
           try:
               results['error_handling'] = self.test_error_handling()
           except Exception as e:
               print(f"Error handling failed: {e}")
           
           # Property tests
           try:
               self.test_property_size_matches_operations()
               results['property_size'] = True
           except Exception as e:
               print(f"Size property failed: {e}")
           
           try:
               self.test_property_peek_idempotent()
               results['property_peek'] = True
           except Exception as e:
               print(f"Peek property failed: {e}")
           
           return results

   def grade_stack(student_file):
       """Grade stack implementation."""
       print("=" * 70)
       print("STACK IMPLEMENTATION GRADING")
       print("=" * 70)
       
       tester = StackTester(student_file)
       results = tester.run_all_tests()
       
       # Calculate score
       passed = sum(results.values())
       total = len(results)
       score = (passed / total) * 10
       
       # Print results
       print(f"\nResults:")
       for test_name, passed in results.items():
           status = "✓ PASS" if passed else "✗ FAIL"
           print(f"  {status} - {test_name}")
       
       print(f"\nFunctionality Score: {score:.2f}/10")
       print(f"Tests Passed: {passed}/{total}")
       
       # Code quality analysis
       print("\n" + "=" * 70)
       print("CODE QUALITY ANALYSIS")
       print("=" * 70)
       
       ast_grader = ASTGrader(student_file)
       
       quality_result = ast_grader.grade(
           check_complexity=True,
           check_naming=True,
           check_docs=True,
           structure_requirements={'classes': 1, 'functions': 5}
       )
       
       print(f"\nCode Quality Score: {quality_result['score']:.2f}/10")
       
       # Final score
       final_score = (score * 0.7 + quality_result['score'] * 0.3)
       print(f"\n{'=' * 70}")
       print(f"FINAL SCORE: {final_score:.2f}/10")
       print(f"{'=' * 70}")
       
       return final_score

   if __name__ == "__main__":
       import sys
       if len(sys.argv) < 2:
           print("Usage: python grade_stack.py <student_file.py>")
           sys.exit(1)
       
       grade_stack(sys.argv[1])

Stateful Testing Example
-------------------------

Advanced Stateful Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # stateful_stack_test.py
   """
   Advanced stateful testing for Stack.
   """

   from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
   from hypothesis import strategies as st
   import importlib.util

   class StackStateMachine(RuleBasedStateMachine):
       """
       Stateful testing using Hypothesis state machines.
       Automatically generates sequences of operations.
       """
       
       def __init__(self, Stack):
           super().__init__()
           self.Stack = Stack
           self.stack = Stack()
           self.model = []  # Reference implementation
       
       @rule(item=st.integers())
       def push(self, item):
           """Rule: push an item."""
           self.stack.push(item)
           self.model.append(item)
       
       @rule()
       def pop(self):
           """Rule: pop an item (if not empty)."""
           if self.model:
               result = self.stack.pop()
               expected = self.model.pop()
               assert result == expected, \
                   f"Pop returned {result}, expected {expected}"
       
       @rule()
       def peek(self):
           """Rule: peek at top item (if not empty)."""
           if self.model:
               result = self.stack.peek()
               expected = self.model[-1]
               assert result == expected, \
                   f"Peek returned {result}, expected {expected}"
       
       @invariant()
       def size_matches(self):
           """Invariant: size matches model."""
           assert self.stack.size() == len(self.model), \
               f"Size {self.stack.size()} != {len(self.model)}"
       
       @invariant()
       def emptiness_matches(self):
           """Invariant: is_empty matches model."""
           assert self.stack.is_empty() == (len(self.model) == 0), \
               "is_empty() inconsistent with actual state"

   def run_stateful_test(student_file):
       """Run stateful testing."""
       # Load student's Stack
       spec = importlib.util.spec_from_file_location("student", student_file)
       module = importlib.util.module_from_spec(spec)
       spec.loader.exec_module(module)
       
       # Create test class
       TestStack = type('TestStack', (StackStateMachine,), {
           '__init__': lambda self: StackStateMachine.__init__(self, module.Stack)
       })
       
       # Run tests
       TestStack.TestCase.settings = settings(max_examples=100)
       suite = unittest.TestLoader().loadTestsFromTestCase(TestStack.TestCase)
       runner = unittest.TextTestRunner()
       result = runner.run(suite)
       
       return result.wasSuccessful()

Running the Example
-------------------

.. code-block:: bash

   # Grade good implementation
   python grade_stack.py student_stack_good.py

   # Grade buggy implementation
   python grade_stack.py student_stack_buggy.py

   # Run stateful tests
   python stateful_stack_test.py student_stack_good.py

Expected Output
---------------

Good Implementation
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ======================================================================
   STACK IMPLEMENTATION GRADING
   ======================================================================

   Results:
     ✓ PASS - basic_operations
     ✓ PASS - lifo_order
     ✓ PASS - error_handling
     ✓ PASS - property_size
     ✓ PASS - property_peek

   Functionality Score: 10.00/10
   Tests Passed: 5/5

   ======================================================================
   CODE QUALITY ANALYSIS
   ======================================================================

   Code Quality Score: 9.50/10

   ======================================================================
   FINAL SCORE: 9.85/10
   ======================================================================

Buggy Implementation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ======================================================================
   STACK IMPLEMENTATION GRADING
   ======================================================================

   Basic operations failed: pop from empty stack
   LIFO order failed: pop from empty stack
   Error handling failed: Should raise IndexError on pop from empty

   Results:
     ✗ FAIL - basic_operations
     ✗ FAIL - lifo_order
     ✗ FAIL - error_handling
     ✓ PASS - property_size
     ✗ FAIL - property_peek

   Functionality Score: 2.00/10
   Tests Passed: 1/5

   ======================================================================
   FINAL SCORE: 3.25/10
   ======================================================================

Queue Implementation
--------------------

Similar grading can be applied to Queue (FIFO):

.. code-block:: python

   # Test FIFO property
   def test_fifo_order(queue, items):
       for item in items:
           queue.enqueue(item)
       
       dequeued = []
       while not queue.is_empty():
           dequeued.append(queue.dequeue())
       
       assert dequeued == items, "Should dequeue in FIFO order"

LinkedList Implementation
-------------------------

For LinkedList, test:

* Node insertion/deletion
* Traversal
* Search operations
* Edge cases (empty list, single node)

See Also
--------

* :doc:`sorting_example` - Simpler grading example
* :doc:`graph_algorithms_example` - More complex structures
* :doc:`../api/property_based_grader` - API reference
