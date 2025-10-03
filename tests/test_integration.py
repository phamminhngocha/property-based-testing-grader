"""
tests/test_integration.py - Integration tests
Chức năng: Test tích hợp giữa các components
"""

import pytest
import os
from src.advanced_grader import AdvancedGrader, BatchGrader


@pytest.mark.integration
class TestAdvancedGraderIntegration:
    """Integration tests for AdvancedGrader."""
    
    def test_comprehensive_grading_workflow(self, sample_student_code, 
                                          mock_reference_function,
                                          mock_performance_test_inputs):
        """
        Test: Complete comprehensive grading workflow.
        Verify: All components work together.
        """
        grader = AdvancedGrader(sample_student_code)
        
        result = grader.grade_comprehensive(
            reference_func=mock_reference_function,
            test_inputs=mock_performance_test_inputs
        )
        
        # Verify result structure
        assert 'final_score' in result
        assert 'max_score' in result
        assert 'grade_letter' in result
        assert 'category_scores' in result
        assert 'grading_time_seconds' in result
        
        # Verify scores are valid
        assert 0 <= result['final_score'] <= result['max_score']
        assert result['grade_letter'] in ['A+', 'A', 'B+', 'B', 'C+', 
                                           'C', 'D+', 'D', 'F']
    
    def test_export_json(self, sample_student_code, temp_dir):
        """
        Test: JSON export functionality.
        Verify: Valid JSON is generated.
        """
        import json
        
        grader = AdvancedGrader(sample_student_code)
        grader.grade_comprehensive()
        
        json_path = os.path.join(temp_dir, "result.json")
        grader.export_results_json(json_path)
        
        # Verify file exists and is valid JSON
        assert os.path.exists(json_path)
        
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        assert 'final_score' in data
        assert 'student_file' in data
    
    def test_export_html(self, sample_student_code, temp_dir):
        """
        Test: HTML export functionality.
        Verify: Valid HTML is generated.
        """
        grader = AdvancedGrader(sample_student_code)
        grader.grade_comprehensive()
        
        html_path = os.path.join(temp_dir, "report.html")
        grader.export_results_html(html_path)
        
        # Verify file exists and contains HTML
        assert os.path.exists(html_path)
        
        with open(html_path, 'r') as f:
            content = f.read()
        
        assert '<html' in content.lower()
        assert 'final score' in content.lower()


@pytest.mark.integration
class TestBatchGraderIntegration:
    """Integration tests for BatchGrader."""
    
    def test_batch_grading_multiple_files(self, temp_dir, 
                                         mock_reference_function,
                                         mock_performance_test_inputs):
        """
        Test: Batch grading of multiple submissions.
        Verify: All files are graded correctly.
        """
        # Create multiple student files
        for i in range(3):
            code = f'''
def sort_list(lst):
    return sorted(lst)

def add(a, b):
    return a + b + {i}  # Slight variation
'''
            filepath = os.path.join(temp_dir, f"student_{i}.py")
            with open(filepath, 'w') as f:
                f.write(code)
        
        # Batch grade
        batch = BatchGrader()
        results = batch.grade_directory(
            directory=temp_dir,
            pattern="student_*.py",
            reference_func=mock_reference_function,
            test_inputs=mock_performance_test_inputs
        )
        
        # Verify results
        assert len(results) == 3
        for result in results:
            assert 'final_score' in result
            assert 'file' in result
    
    def test_plagiarism_detection_integration(self, temp_dir):
        """
        Test: Plagiarism detection across submissions.
        Verify: Similar code is detected.
        """
        # Create two very similar files
        code1 = '''
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
'''
        
        code2 = '''
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y
'''
        
        # Save files
        with open(os.path.join(temp_dir, "student1.py"), 'w') as f:
            f.write(code1)
        
        with open(os.path.join(temp_dir, "student2.py"), 'w') as f:
            f.write(code2)
        
        # Detect plagiarism
        batch = BatchGrader()
        results = batch.detect_plagiarism(temp_dir, threshold=0.7)
        
        # Should detect similarity
        assert len(results) > 0
        assert results[0]['overall_similarity'] > 0.7
    
    def test_batch_export_csv(self, temp_dir):
        """
        Test: CSV export for batch results.
        Verify: Valid CSV is generated.
        """
        import csv
        
        # Create sample file
        code = 'def add(a, b): return a + b'
        with open(os.path.join(temp_dir, "student.py"), 'w') as f:
            f.write(code)
        
        # Batch grade
        batch = BatchGrader()
        batch.grade_directory(temp_dir, "student.py")
        
        # Export CSV
        csv_path = os.path.join(temp_dir, "results.csv")
        batch.export_batch_results(csv_path)
        
        # Verify CSV
        assert os.path.exists(csv_path)
        
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) > 0
        assert 'Final Score' in rows[0]


@pytest.mark.integration
@pytest.mark.slow
class TestEndToEndWorkflow:
    """End-to-end workflow tests."""
    
    def test_complete_assignment_grading(self, temp_dir):
        """
        Test: Complete assignment grading workflow.
        Simulate real assignment grading scenario.
        """
        # Create assignment
        assignment_code = '''
def bubble_sort(arr):
    """Bubble sort implementation."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
'''
        
        filepath = os.path.join(temp_dir, "assignment.py")
        with open(filepath, 'w') as f:
            f.write(assignment_code)
        
        # Grade with full pipeline
        config = {
            'weights': {
                'functionality': 0.50,
                'code_quality': 0.30,
                'performance': 0.20,
            },
            'enable_pbt': True,
            'enable_ast_analysis': True,
            'max_complexity': 15,
        }
        
        grader = AdvancedGrader(filepath, config)
        
        result = grader.grade_comprehensive(
            reference_func=sorted,
            test_inputs=[
                ([list(range(50))],),
                ([list(range(50, 0, -1))],),
            ]
        )
        
        # Generate all reports
        text_report = grader.generate_detailed_report(result)
        
        json_path = os.path.join(temp_dir, "full_result.json")
        grader.export_results_json(json_path)
        
        html_path = os.path.join(temp_dir, "full_report.html")
        grader.export_results_html(html_path)
        
        # Verify all outputs
        assert result['final_score'] >= 0
        assert len(text_report) > 0
        assert os.path.exists(json_path)
        assert os.path.exists(html_path)
