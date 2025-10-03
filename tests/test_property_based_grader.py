"""
tests/test_property_based_grader.py - Unit tests for PropertyBasedGrader
Chức năng: Test property-based testing functionality
"""

import pytest
from hypothesis import strategies as st, given, settings
from src.property_based_grader import PropertyBasedGrader


class TestPropertyBasedGrader:
    """Test suite for PropertyBasedGrader."""
    
    def test_initialization(self, sample_student_code):
        """Test grader initialization."""
        grader = PropertyBasedGrader(sample_student_code)
        
        assert grader.student_file == sample_student_code
        assert grader.student_module is None
        assert grader.test_results == []
    
    def test_load_student_code(self, sample_student_code):
        """Test loading student code."""
        grader = PropertyBasedGrader(sample_student_code)
        result = grader.load_student_code()
        
        assert result is True
        assert grader.student_module is not None
    
    def test_commutativity_pass(self, sample_student_code):
        """
        Test: Commutativity test with commutative function.
        Verify: Test passes for add function.
        """
        grader = PropertyBasedGrader(sample_student_code)
        grader.load_student_code()
        
        result = grader.test_commutativity(
            "add",
            st.integers(min_value=-100, max_value=100),
            weight=1.0
        )
        
        assert result['passed'] is True
        assert result['score'] == 10.0
        assert result['test'] == 'commutativity'
    
    def test_associativity_pass(self, sample_student_code):
        """
        Test: Associativity test with associative function.
        Verify: Test passes for add function.
        """
        grader = PropertyBasedGrader(sample_student_code)
        grader.load_student_code()
        
        result = grader.test_associativity(
            "add",
            st.integers(min_value=-100, max_value=100),
            weight=1.0
        )
        
        assert result['passed'] is True
        assert result['score'] == 10.0
    
    def test_identity_pass(self, sample_student_code):
        """
        Test: Identity element test.
        Verify: 0 is identity for addition.
        """
        grader = PropertyBasedGrader(sample_student_code)
        grader.load_student_code()
        
        result = grader.test_identity(
            "add",
            0,
            st.integers(min_value=-100, max_value=100),
            weight=1.0
        )
        
        assert result['passed'] is True
        assert result['score'] == 10.0
    
    def test_idempotence_pass(self, sample_student_code):
        """
        Test: Idempotence test with sorting.
        Verify: Sorting twice gives same result.
        """
        grader = PropertyBasedGrader(sample_student_code)
        grader.load_student_code()
        
        result = grader.test_idempotence(
            "sort_list",
            st.lists(st.integers(), max_size=50),
            weight=1.0
        )
        
        assert result['passed'] is True
    
    def test_oracle_pass(self, sample_student_code):
        """
        Test: Oracle-based testing.
        Verify: Student function matches reference.
        """
        grader = PropertyBasedGrader(sample_student_code)
        grader.load_student_code()
        
        result = grader.test_with_oracle(
            "sort_list",
            sorted,
            st.lists(st.integers(), max_size=50),
            weight=1.0
        )
        
        assert result['passed'] is True
        assert result['score'] == 10.0
    
    def test_custom_invariants_pass(self, sample_student_code):
        """
        Test: Custom invariant testing.
        Verify: Custom properties are checked.
        """
        grader = PropertyBasedGrader(sample_student_code)
        grader.load_student_code()
        
        def is_sorted(input_list, output_list):
            if len(output_list) <= 1:
                return True
            return all(output_list[i] <= output_list[i+1] 
                      for i in range(len(output_list)-1))
        
        def is_permutation(input_list, output_list):
            return sorted(input_list) == sorted(output_list)
        
        result = grader.test_custom_invariants(
            "sort_list",
            [is_sorted, is_permutation],
            st.lists(st.integers(), max_size=50),
            weight=1.0
        )
        
        assert result['passed'] is True
        assert result['passed_invariants'] == 2
        assert result['total_invariants'] == 2
    
    def test_function_not_found(self, sample_student_code):
        """
        Test: Testing non-existent function.
        Verify: Error is handled gracefully.
        """
        grader = PropertyBasedGrader(sample_student_code)
        grader.load_student_code()
        
        result = grader.test_commutativity(
            "nonexistent_function",
            st.integers(),
            weight=1.0
        )
        
        assert result['passed'] is False
        assert result['score'] == 0.0
        assert 'error' in result
    
    def test_grade_calculation(self, sample_student_code):
        """
        Test: Overall grade calculation.
        Verify: Weighted average is calculated correctly.
        """
        grader = PropertyBasedGrader(sample_student_code)
        grader.load_student_code()
        
        # Run multiple tests
        grader.test_commutativity("add", st.integers(), weight=0.3)
        grader.test_identity("add", 0, st.integers(), weight=0.2)
        grader.test_with_oracle("sort_list", sorted, 
                               st.lists(st.integers()), weight=0.5)
        
        result = grader.grade()
        
        assert 'score' in result
        assert 'max_score' in result
        assert result['max_score'] == 10.0
        assert 0 <= result['score'] <= 10.0
        assert result['total_tests'] == 3
    
    def test_generate_report(self, sample_student_code):
        """
        Test: Report generation.
        Verify: Report contains expected sections.
        """
        grader = PropertyBasedGrader(sample_student_code)
        grader.load_student_code()
        
        grader.test_commutativity("add", st.integers(), weight=1.0)
        grader.grade()
        
        report = grader.generate_report()
        
        assert "PROPERTY-BASED TESTING GRADING REPORT" in report
        assert "Final Score:" in report
        assert "Tests Passed:" in report
        assert "commutativity" in report


class TestPropertyBasedGraderFailures:
    """Test failure scenarios."""
    
    def test_commutativity_fail(self, temp_dir):
        """
        Test: Non-commutative function fails commutativity test.
        """
        import os
        
        code = '''
def subtract(a, b):
    return a - b
'''
        filepath = os.path.join(temp_dir, "noncommutative.py")
        with open(filepath, 'w') as f:
            f.write(code)
        
        grader = PropertyBasedGrader(filepath)
        grader.load_student_code()
        
        result = grader.test_commutativity(
            "subtract",
            st.integers(min_value=1, max_value=10),
            weight=1.0
        )
        
        assert result['passed'] is False
        assert result['score'] == 0.0
        assert 'failures' in result
    
    def test_custom_invariant_fail(self, temp_dir):
        """
        Test: Function violating custom invariant.
        """
        import os
        
        code = '''
def bad_sort(lst):
    return lst[::-1]  # Reverses instead of sorting
'''
        filepath = os.path.join(temp_dir, "bad_sort.py")
        with open(filepath, 'w') as f:
            f.write(code)
        
        grader = PropertyBasedGrader(filepath)
        grader.load_student_code()
        
        def is_sorted(input_list, output_list):
            if len(output_list) <= 1:
                return True
            return all(output_list[i] <= output_list[i+1] 
                      for i in range(len(output_list)-1))
        
        result = grader.test_custom_invariants(
            "bad_sort",
            [is_sorted],
            st.lists(st.integers(min_value=0, max_value=100), min_size=2),
            weight=1.0
        )
        
        assert result['passed'] is False


@pytest.mark.slow
class TestPropertyBasedGraderPerformance:
    """Performance-related tests."""
    
    def test_large_number_of_examples(self, sample_student_code):
        """
        Test: Handling large number of test examples.
        Verify: Completes in reasonable time.
        """
        grader = PropertyBasedGrader(sample_student_code)
        grader.load_student_code()
        
        # This will generate many test cases
        result = grader.test_with_oracle(
            "add",
            lambda a, b: a + b,
            st.integers(),
            weight=1.0
        )
        
        assert result is not None
