.. Chức năng: Ví dụ chi tiết về grading sorting algorithms

Sorting Algorithm Example
=========================

This comprehensive example shows how to grade sorting algorithm implementations.

Assignment Description
----------------------

**Objective**: Implement a sorting function that sorts a list of integers in ascending order.

**Requirements**:

1. Function name: ``my_sort(lst)``
2. Input: List of integers (may be empty)
3. Output: Sorted list in ascending order
4. Must handle edge cases (empty lists, single elements, duplicates)
5. Performance: Should handle lists up to 10,000 elements efficiently

**Constraints**:

* Time complexity: O(n log n) or better
* Space complexity: O(n)
* No use of built-in ``sorted()`` or ``list.sort()``

Student Code Example
--------------------

Good Implementation
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # student_good.py
   """
   Student: Alice Smith
   ID: 12345
   Assignment: Sorting Algorithm
   """

   def my_sort(lst):
       """
       Sort a list using merge sort algorithm.
       
       Args:
           lst: List of integers to sort
           
       Returns:
           Sorted list in ascending order
       """
       if len(lst) <= 1:
           return lst
       
       # Divide
       mid = len(lst) // 2
       left = my_sort(lst[:mid])
       right = my_sort(lst[mid:])
       
       # Conquer
       return merge(left, right)
   
   def merge(left, right):
       """Merge two sorted lists."""
       result = []
       i = j = 0
       
       while i < len(left) and j < len(right):
           if left[i] <= right[j]:
               result.append(left[i])
               i += 1
           else:
               result.append(right[j])
               j += 1
       
       result.extend(left[i:])
       result.extend(right[j:])
       return result

Buggy Implementation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # student_buggy.py
   """
   Student: Bob Jones
   Assignment: Sorting Algorithm
   """

   def my_sort(lst):
       """Sort using bubble sort with a bug."""
       if not lst:
           return lst
       
       n = len(lst)
       for i in range(n):
           for j in range(n - 1):  # BUG: Should be n-i-1
               if lst[j] > lst[j + 1]:
                   lst[j], lst[j + 1] = lst[j + 1], lst[j]
       
       return lst

Reference Solution
------------------

.. code-block:: python

   # reference_solution.py
   """
   Reference implementation for comparison.
   """

   def reference_sort(lst):
       """
       Reference sorting implementation using Python's built-in.
       Used as oracle for property-based testing.
       """
       return sorted(lst)

Grading Script
--------------

Complete Grading Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # grade_sorting.py
   """
   Comprehensive grading script for sorting assignment.
   """

   from src.property_based_grader import PropertyBasedGrader
   from src.performance_grader import PerformanceGrader
   from src.ast_grader import ASTGrader
   from src.advanced_grader import AdvancedGrader
   from hypothesis import strategies as st
   import sys

   def grade_sorting_basic(student_file):
       """
       Basic grading using property-based testing.
       """
       print("=" * 70)
       print("SORTING ASSIGNMENT - BASIC GRADING")
       print("=" * 70)
       
       grader = PropertyBasedGrader(student_file)
       
       # Define custom invariants
       def is_sorted(input_list, output_list):
           """Check if output is sorted."""
           if len(output_list) <= 1:
               return True
           return all(output_list[i] <= output_list[i+1] 
                      for i in range(len(output_list)-1))
       
       def is_permutation(input_list, output_list):
           """Check if output is permutation of input."""
           return sorted(input_list) == sorted(output_list)
       
       def preserves_length(input_list, output_list):
           """Check if length is preserved."""
           return len(input_list) == len(output_list)
       
       # Test 1: Idempotence (sorting twice gives same result)
       print("\n[Test 1] Testing idempotence...")
       grader.test_idempotence(
           "my_sort",
           st.lists(st.integers(), max_size=100),
           weight=0.2
       )
       
       # Test 2: Correctness with oracle
       print("[Test 2] Testing correctness with oracle...")
       grader.test_with_oracle(
           "my_sort",
           sorted,
           st.lists(st.integers(), max_size=100),
           weight=0.4
       )
       
       # Test 3: Custom invariants
       print("[Test 3] Testing custom invariants...")
       grader.test_custom_invariants(
           "my_sort",
           [is_sorted, is_permutation, preserves_length],
           st.lists(st.integers(), max_size=100),
           weight=0.4
       )
       
       # Calculate results
       result = grader.grade()
       print("\n" + grader.generate_report())
       
       return result

   def grade_sorting_performance(student_file):
       """
       Performance grading for sorting.
       """
       print("\n" + "=" * 70)
       print("PERFORMANCE TESTING")
       print("=" * 70)
       
       perf_grader = PerformanceGrader(student_file)
       
       # Test inputs of increasing size
       test_inputs = [
           ([list(range(100))],),           # Already sorted
           ([list(range(100, 0, -1))],),    # Reverse sorted
           ([list(range(1000))],),          # Larger input
           ([[5, 2, 8, 1, 9, 3, 7, 4, 6]],),  # Random
       ]
       
       result = perf_grader.grade_performance(
           "my_sort",
           sorted,
           test_inputs,
           max_score=10.0
       )
       
       print(perf_grader.generate_report(result))
       return result

   def grade_sorting_code_quality(student_file):
       """
       Code quality grading for sorting.
       """
       print("\n" + "=" * 70)
       print("CODE QUALITY ANALYSIS")
       print("=" * 70)
       
       ast_grader = ASTGrader(student_file)
       
       # Requirements for sorting assignment
       structure_requirements = {
           'functions': 1,  # At least my_sort function
           'loops': 1,      # Should have at least one loop
       }
       
       result = ast_grader.grade(
           check_complexity=True,
           check_structure=True,
           check_naming=True,
           check_docs=True,
           structure_requirements=structure_requirements,
           max_complexity=15  # Allow moderate complexity
       )
       
       print(f"\nCode Quality Score: {result['score']:.2f}/10")
       
       # Print breakdown
       if 'results' in result:
           for category, details in result['results'].items():
               print(f"\n{category.upper()}:")
               print(f"  Score: {details.get('score', 0):.2f}/10")
               if not details.get('passed', False):
                   print(f"  Issues: {details.get('violations', [])}")
       
       return result

   def grade_sorting_comprehensive(student_file):
       """
       Comprehensive grading using AdvancedGrader.
       """
       print("\n" + "=" * 70)
       print("COMPREHENSIVE GRADING")
       print("=" * 70)
       
       # Custom configuration for sorting assignment
       config = {
           'weights': {
               'functionality': 0.50,  # Correctness is most important
               'code_quality': 0.20,
               'performance': 0.30,    # Performance matters for sorting
           },
           'enable_pbt': True,
           'enable_performance': True,
           'enable_ast_analysis': True,
           'max_complexity': 15,
       }
       
       grader = AdvancedGrader(student_file, config)
       
       # Test inputs for performance
       test_inputs = [
           ([list(range(100))],),
           ([list(range(500, 0, -1))],),
           ([list(range(1000))],),
       ]
       
       result = grader.grade_comprehensive(
           reference_func=sorted,
           test_inputs=test_inputs
       )
       
       # Print detailed report
       print(grader.generate_detailed_report(result))
       
       # Export results
       grader.export_results_json("sorting_result.json")
       grader.export_results_html("sorting_report.html")
       
       return result

   def main():
       """Main grading function."""
       if len(sys.argv) < 2:
           print("Usage: python grade_sorting.py <student_file.py>")
           print("\nExample: python grade_sorting.py student_good.py")
           sys.exit(1)
       
       student_file = sys.argv[1]
       
       print(f"\nGrading file: {student_file}\n")
       
       # Choose grading method
       print("Select grading method:")
       print("1. Basic (Property-Based Testing only)")
       print("2. With Performance Testing")
       print("3. With Code Quality Analysis")
       print("4. Comprehensive (All methods)")
       
       choice = input("\nEnter choice (1-4) [default: 4]: ").strip() or "4"
       
       if choice == "1":
           grade_sorting_basic(student_file)
       elif choice == "2":
           grade_sorting_basic(student_file)
           grade_sorting_performance(student_file)
       elif choice == "3":
           grade_sorting_basic(student_file)
           grade_sorting_code_quality(student_file)
       else:
           grade_sorting_comprehensive(student_file)

   if __name__ == "__main__":
       main()

Running the Example
-------------------

Basic Grading
~~~~~~~~~~~~~

.. code-block:: bash

   # Grade the good implementation
   python grade_sorting.py student_good.py

   # Grade the buggy implementation
   python grade_sorting.py student_buggy.py

Expected Output (Good Implementation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ======================================================================
   SORTING ASSIGNMENT - BASIC GRADING
   ======================================================================

   [Test 1] Testing idempotence...
   [Test 2] Testing correctness with oracle...
   [Test 3] Testing custom invariants...

   ======================================================================
   PROPERTY-BASED TESTING GRADING REPORT
   ======================================================================
   Final Score: 10.00/10
   Tests Passed: 3/3

   ✓ PASS - idempotence
     Function: my_sort
     Score: 10.00/10

   ✓ PASS - oracle
     Function: my_sort
     Score: 10.00/10

   ✓ PASS - custom_invariants
     Function: my_sort
     Score: 10.00/10
     Invariant results:
       ✓ is_sorted
       ✓ is_permutation
       ✓ preserves_length

Expected Output (Buggy Implementation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ======================================================================
   PROPERTY-BASED TESTING GRADING REPORT
   ======================================================================
   Final Score: 6.50/10
   Tests Passed: 1/3

   ✓ PASS - idempotence
     Function: my_sort
     Score: 10.00/10

   ✗ FAIL - oracle
     Function: my_sort
     Score: 3.50/10
     Sample failures:
       - Input: [5, 2, 8, 1, 9]
         Student: [1, 2, 5, 8, 9]
         Oracle: [1, 2, 5, 8, 9]
       - Input: [10, 5, 3, 8, 2]
         Student: [2, 3, 5, 8, 10]
         Oracle: [2, 3, 5, 8, 10]

   ✗ FAIL - custom_invariants
     Function: my_sort
     Score: 6.67/10
     Invariant results:
       ✓ is_sorted
       ✓ is_permutation
       ✗ preserves_length

Batch Grading Example
----------------------

Grade Multiple Submissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # batch_grade_sorting.py
   """
   Batch grade all sorting submissions.
   """

   from src.advanced_grader import BatchGrader

   def batch_grade_sorting():
       """Grade all submissions in directory."""
       
       # Initialize batch grader
       batch = BatchGrader({
           'weights': {
               'functionality': 0.50,
               'code_quality': 0.20,
               'performance': 0.30,
           }
       })
       
       # Grade all submissions
       print("Grading all submissions...")
       results = batch.grade_directory(
           directory="submissions/sorting/",
           pattern="student_*.py",
           reference_func=sorted,
           test_inputs=[
               ([list(range(100))],),
               ([list(range(1000))],),
           ]
       )
       
       # Check plagiarism
       print("\nChecking for plagiarism...")
       plagiarism = batch.detect_plagiarism(
           directory="submissions/sorting/",
           threshold=0.80
       )
       
       if plagiarism:
           print("\n⚠️  PLAGIARISM DETECTED:")
           for pair in plagiarism:
               print(f"  {pair['file1']} <-> {pair['file2']}")
               print(f"  Similarity: {pair['overall_similarity']:.1%}\n")
       
       # Generate reports
       print(batch.generate_summary_report())
       batch.export_batch_results("sorting_batch_results.csv")
       
       print("\n✅ Batch grading complete!")
       print("Results saved to: sorting_batch_results.csv")

   if __name__ == "__main__":
       batch_grade_sorting()

Run Batch Grading
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python batch_grade_sorting.py

Variations and Extensions
--------------------------

Test Different Algorithms
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Test specific algorithm characteristics
   
   def is_stable_sort(input_list, output_list):
       """Check if sort is stable."""
       #
