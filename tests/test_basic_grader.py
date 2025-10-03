"""
tests/test_basic_grader.py - Unit tests for BasicGrader
Chức năng: Test tất cả functionality của BasicGrader class
"""

import pytest
from src.basic_grader import BasicGrader


class TestBasicGrader:
    """Test suite for BasicGrader class."""
    
    def test_initialization(self, sample_student_code):
        """
        Test: Grader initialization.
        Verify: Grader can be created with valid file.
        """
        grader = BasicGrader(sample_student_code)
        assert grader.student_file == sample_student_code
        assert grader.student_module is None
        assert grader.test_results == []
    
    def test_load_student_code_success(self, sample_student_code):
        """
        Test: Loading valid student code.
        Verify: Code loads successfully and module is accessible.
        """
        grader = BasicGrader(sample_student_code)
        result = grader.load_student_code()
        
        assert result is True
        assert grader.student_module is not None
        assert hasattr(grader.student_module, 'add')
        assert hasattr(grader.student_module, 'multiply')
    
    def test_load_student_code_failure(self, temp_dir):
        """
        Test: Loading non-existent file.
        Verify: Returns False and handles error gracefully.
        """
        import os
        nonexistent_file = os.path.join(temp_dir, "nonexistent.py")
        
        grader = BasicGrader(nonexistent_file)
        result = grader.load_student_code()
        
        assert result is False
    
    def test_grade_all_pass(self, sample_student_code, basic_test_cases):
        """
        Test: Grading with all tests passing.
        Verify: Correct score calculation and statistics.
        """
        grader = BasicGrader(sample_student_code)
        result = grader.grade(basic_test_cases)
        
        assert result['score'] == 10.0
        assert result['max_score'] == 10.0
        assert result['passed'] == len(basic_test_cases)
        assert result['total'] == len(basic_test_cases)
        assert result['failures'] == 0
        assert result['errors'] == 0
    
    def test_grade_some_failures(self, sample_buggy_code):
        """
        Test: Grading with some test failures.
        Verify: Partial score and failure tracking.
        """
        test_cases = [
            {'function': 'add', 'inputs': [2, 3], 'expected': 5},
            {'function': 'add', 'inputs': [1, 1], 'expected': 2},
        ]
        
        grader = BasicGrader(sample_buggy_code)
        result = grader.grade(test_cases)
        
        assert result['score'] < result['max_score']
        assert result['passed'] < result['total']
        assert result['failures'] > 0 or result['errors'] > 0
    
    def test_grade_empty_test_cases(self, sample_student_code):
        """
        Test: Grading with empty test cases.
        Verify: Handles edge case gracefully.
        """
        grader = BasicGrader(sample_student_code)
        result = grader.grade([])
        
        assert result['score'] == 0
        assert result['total'] == 0
    
    def test_grade_function_not_found(self, sample_student_code):
        """
        Test: Grading function that doesn't exist.
        Verify: Error is caught and reported.
        """
        test_cases = [
            {'function': 'nonexistent_func', 'inputs': [1, 2], 'expected': 3}
        ]
        
        grader = BasicGrader(sample_student_code)
        result = grader.grade(test_cases)
        
        assert result['score'] == 0
        assert result['errors'] > 0
    
    def test_grade_with_custom_max_score(self, sample_student_code, basic_test_cases):
        """
        Test: Grading with custom max score.
        Verify: Score scales correctly.
        """
        grader = BasicGrader(sample_student_code)
        result = grader.grade(basic_test_cases, max_score=20.0)
        
        assert result['max_score'] == 20.0
        assert result['score'] == 20.0  # All pass
    
    def test_grade_division_by_zero(self, sample_buggy_code):
        """
        Test: Handling runtime errors (division by zero).
        Verify: Error is caught and counted.
        """
        test_cases = [
            {'function': 'divide', 'inputs': [10, 0], 'expected': None}
        ]
        
        grader = BasicGrader(sample_buggy_code)
        result = grader.grade(test_cases)
        
        assert result['errors'] > 0
        assert result['score'] == 0
    
    @pytest.mark.parametrize("inputs,expected", [
        ([2, 3], 5),
        ([0, 0], 0),
        ([-1, 1], 0),
        ([100, 200], 300),
    ])
    def test_grade_parameterized(self, sample_student_code, inputs, expected):
        """
        Test: Parameterized testing of add function.
        Verify: Multiple input combinations work correctly.
        """
        test_cases = [
            {'function': 'add', 'inputs': inputs, 'expected': expected}
        ]
        
        grader = BasicGrader(sample_student_code)
        result = grader.grade(test_cases)
        
        assert result['passed'] == 1


class TestBasicGraderEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_syntax_error_in_student_code(self, temp_dir):
        """
        Test: Student code with syntax error.
        Verify: Load fails gracefully.
        """
        import os
        
        code = '''
def bad_function(
    # Missing closing parenthesis
    return 1
'''
        filepath = os.path.join(temp_dir, "syntax_error.py")
        with open(filepath, 'w') as f:
            f.write(code)
        
        grader = BasicGrader(filepath)
        result = grader.load_student_code()
        
        assert result is False
    
    def test_infinite_loop_protection(self, temp_dir):
        """
        Test: Protection against infinite loops.
        Verify: Test times out appropriately.
        Note: This test uses timeout mechanism.
        """
        pytest.skip("Requires timeout implementation")
    
    def test_memory_intensive_code(self, temp_dir):
        """
        Test: Handling memory-intensive code.
        Verify: Doesn't crash the grader.
        """
        pytest.skip("Requires memory limit implementation")


class TestBasicGraderIntegration:
    """Integration tests for BasicGrader."""
    
    @pytest.mark.integration
    def test_complete_grading_workflow(self, sample_student_code, basic_test_cases):
        """
        Test: Complete grading workflow from start to finish.
        Verify: All steps work together correctly.
        """
        # Create grader
        grader = BasicGrader(sample_student_code)
        
        # Load code
        assert grader.load_student_code() is True
        
        # Grade
        result = grader.grade(basic_test_cases)
        
        # Verify comprehensive results
        assert 'score' in result
        assert 'max_score' in result
        assert 'passed' in result
        assert 'total' in result
        assert 'failures' in result
        assert 'errors' in result
        assert 'details' in result
        
        # Verify score is reasonable
        assert 0 <= result['score'] <= result['max_score']
        assert result['passed'] <= result['total']
