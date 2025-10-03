.. Chức năng: API documentation cho AdvancedGrader và BatchGrader

Advanced Grader
===============

.. automodule:: src.advanced_grader
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The ``AdvancedGrader`` integrates all grading methods into a comprehensive system.

AdvancedGrader Class
--------------------

.. autoclass:: src.advanced_grader.AdvancedGrader
   :members:
   :special-members: __init__

Configuration
-------------

Default Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   {
       'weights': {
           'functionality': 0.40,    # PBT/Basic tests
           'code_quality': 0.20,     # AST analysis
           'performance': 0.20,      # Speed/memory
           'documentation': 0.10,    # Docstrings
           'style': 0.10            # PEP 8
       },
       'enable_pbt': True,
       'enable_performance': True,
       'enable_ast_analysis': True,
       'max_complexity': 10,
       'plagiarism_check': False,
       'timeout': 30
   }

Custom Configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   custom_config = {
       'weights': {
           'functionality': 0.60,
           'code_quality': 0.30,
           'performance': 0.10,
       },
       'max_complexity': 15,
       'enable_pbt': True,
   }

   grader = AdvancedGrader("student.py", config=custom_config)

Methods
-------

grade_comprehensive(reference_func, test_inputs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: src.advanced_grader.AdvancedGrader.grade_comprehensive

**Example:**

.. code-block:: python

   grader = AdvancedGrader("student.py")
   
   result = grader.grade_comprehensive(
       reference_func=sorted,
       test_inputs=[
           ([list(range(100))],),
           ([list(range(1000))],)
       ]
   )

generate_detailed_report(result)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: src.advanced_grader.AdvancedGrader.generate_detailed_report

export_results_json(output_file)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: src.advanced_grader.AdvancedGrader.export_results_json

export_results_html(output_file)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: src.advanced_grader.AdvancedGrader.export_results_html

BatchGrader Class
-----------------

.. autoclass:: src.advanced_grader.BatchGrader
   :members:
   :special-members: __init__

grade_directory(directory, pattern, reference_func, test_inputs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: src.advanced_grader.BatchGrader.grade_directory

**Example:**

.. code-block:: python

   batch = BatchGrader()
   
   results = batch.grade_directory(
       directory="submissions/",
       pattern="student_*.py",
       reference_func=sorted,
       test_inputs=[...]
   )

detect_plagiarism(directory, pattern, threshold)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: src.advanced_grader.BatchGrader.detect_plagiarism

generate_summary_report()
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: src.advanced_grader.BatchGrader.generate_summary_report

export_batch_results(output_file)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: src.advanced_grader.BatchGrader.export_batch_results

Complete Examples
-----------------

Single File Grading
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.advanced_grader import AdvancedGrader

   # Custom configuration
   config = {
       'weights': {
           'functionality': 0.50,
           'code_quality': 0.30,
           'performance': 0.20,
       },
       'max_complexity': 12,
   }

   # Initialize
   grader = AdvancedGrader("student_code.py", config)

   # Reference implementation
   def reference_sort(arr):
       return sorted(arr)

   # Test inputs
   test_inputs = [
       ([list(range(100))],),
       ([list(range(500, 0, -1))],),
       ([[1, 3, 2, 5, 4]],),
   ]

   # Grade
   result = grader.grade_comprehensive(reference_sort, test_inputs)

   # Generate reports
   print(grader.generate_detailed_report(result))
   grader.export_results_html("report.html")
   grader.export_results_json("results.json")

Batch Processing
~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.advanced_grader import BatchGrader

   # Initialize batch grader
   batch = BatchGrader()

   # Grade all submissions
   results = batch.grade_directory(
       directory="submissions/",
       pattern="*.py",
       reference_func=sorted,
       test_inputs=[
           ([list(range(100))],),
           ([list(range(1000))],),
       ]
   )

   # Check for plagiarism
   plagiarism = batch.detect_plagiarism(
       directory="submissions/",
       threshold=0.8
   )

   if plagiarism:
       print("⚠️  Plagiarism detected:")
       for pair in plagiarism:
           print(f"  {pair['file1']} <-> {pair['file2']}")
           print(f"  Similarity: {pair['overall_similarity']:.1%}")

   # Generate reports
   print(batch.generate_summary_report())
   batch.export_batch_results("batch_results.csv")

With Custom Weights
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Configuration for algorithm assignment
   algo_config = {
       'weights': {
           'functionality': 0.50,  # Correctness is key
           'code_quality': 0.20,
           'performance': 0.30,    # Performance matters
       },
       'enable_pbt': True,
       'enable_performance': True,
       'max_complexity': 15,
   }

   # Configuration for code quality assignment
   quality_config = {
       'weights': {
           'functionality': 0.30,
           'code_quality': 0.50,   # Focus on quality
           'documentation': 0.20,
       },
       'enable_ast_analysis': True,
       'max_complexity': 8,  # Stricter
   }

Return Values
-------------

grade_comprehensive() Returns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   {
       'final_score': float,          # 0-10
       'max_score': float,            # 10.0
       'grade_letter': str,           # A+, A, B+, etc.
       'category_scores': {
           'functionality': float,
           'code_quality': float,
           'performance': float,
       },
       'weights': dict,               # Weight configuration
       'grading_time_seconds': float, # Time taken
       'timestamp': str,              # ISO format
   }

Grade Letter Scale
~~~~~~~~~~~~~~~~~~

============  ============
Score Range   Grade Letter
============  ============
9.0 - 10.0    A+
8.5 - 8.9     A
8.0 - 8.4     B+
7.0 - 7.9     B
6.5 - 6.9     C+
5.5 - 6.4     C
5.0 - 5.4     D+
4.0 - 4.9     D
0.0 - 3.9     F
============  ============

Best Practices
--------------

1. **Choose Appropriate Weights**

   .. code-block:: python

      # For algorithms: emphasize correctness and performance
      algo_weights = {
          'functionality': 0.50,
          'performance': 0.30,
          'code_quality': 0.20,
      }
      
      # For software design: emphasize quality
      design_weights = {
          'functionality': 0.30,
          'code_quality': 0.50,
          'documentation': 0.20,
      }

2. **Use Batch Processing**

   .. code-block:: python

      # Process all submissions at once
      batch = BatchGrader()
      batch.grade_directory("submissions/")

3. **Export Multiple Formats**

   .. code-block:: python

      # For students: HTML
      grader.export_results_html("report.html")
      
      # For analysis: JSON
      grader.export_results_json("data.json")
      
      # For spreadsheets: CSV
      batch.export_batch_results("grades.csv")

4. **Check Plagiarism**

   .. code-block:: python

      suspicious = batch.detect_plagiarism("submissions/", threshold=0.75)

5. **Test Configuration**

   .. code-block:: python

      # Test with known-good code first
      grader = AdvancedGrader("reference.py", config)
      result = grader.grade_comprehensive()
      assert result['final_score'] >= 9.0

Performance Considerations
--------------------------

* **Batch grading** is more efficient than individual files
* **Property-based testing** can be slow (adjust max_examples)
* **Performance testing** adds overhead (disable if not needed)
* Use **multiprocessing** for large batches (future feature)

Troubleshooting
---------------

**Issue: Grading takes too long**

Solution: Reduce test cases or disable performance testing

.. code-block:: python

   config = {'enable_performance': False}

**Issue: All scores are too low**

Solution: Adjust weights or lower complexity threshold

.. code-block:: python

   config = {'max_complexity': 15}

**Issue: Plagiarism false positives**

Solution: Increase similarity threshold

.. code-block:: python

   batch.detect_plagiarism("dir/", threshold=0.9)

See Also
--------

* :doc:`property_based_grader` - Property-based testing details
* :doc:`performance_grader` - Performance testing details
* :doc:`plagiarism_detector` - Plagiarism detection details
* :doc:`../guides/batch_grading` - Batch grading guide
