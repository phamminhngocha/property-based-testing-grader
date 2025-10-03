"""
Basic Grader - Phương pháp chấm điểm cơ bản với unittest
Sử dụng unittest để kiểm tra các test cases cơ bản
"""

import unittest
import importlib.util
import sys
import io
from typing import Dict, Any, List
from contextlib import redirect_stdout, redirect_stderr


class BasicGrader:
    """Lớp chấm điểm cơ bản sử dụng unittest"""
    
    def __init__(self, student_file: str):
        """
        Khởi tạo bộ chấm điểm
        
        Args:
            student_file: Đường dẫn đến file code sinh viên
        """
        self.student_file = student_file
        self.student_module = None
        self.test_results = []
        
    def load_student_code(self) -> bool:
        """
        Tải module code của sinh viên
        
        Returns:
            True nếu tải thành công, False nếu thất bại
        """
        try:
            spec = importlib.util.spec_from_file_location(
                "student_module", 
                self.student_file
            )
            self.student_module = importlib.util.module_from_spec(spec)
            sys.modules["student_module"] = self.student_module
            spec.loader.exec_module(self.student_module)
            return True
        except Exception as e:
            print(f"Lỗi khi tải code sinh viên: {e}")
            return False
    
    def create_test_class(self, test_cases: List[Dict]) -> type:
        """
        Tạo test class động từ danh sách test cases
        
        Args:
            test_cases: Danh sách các test case
            
        Returns:
            Test class động
        """
        def create_test_method(func_name, inputs, expected):
            def test(self):
                func = getattr(self.student_module, func_name)
                result = func(*inputs)
                self.assertEqual(result, expected)
            return test
        
        # Tạo dictionary chứa các test methods
        test_methods = {'student_module': self.student_module}
        
        for i, tc in enumerate(test_cases):
            test_name = f"test_{tc['function']}_{i}"
            test_methods[test_name] = create_test_method(
                tc['function'], 
                tc['inputs'], 
                tc['expected']
            )
        
        # Tạo test class động
        return type('DynamicTestClass', (unittest.TestCase,), test_methods)
    
    def grade(self, test_cases: List[Dict], max_score: float = 10.0) -> Dict[str, Any]:
        """
        Chấm điểm dựa trên test cases
        
        Args:
            test_cases: Danh sách test cases
            max_score: Điểm tối đa
            
        Returns:
            Dictionary chứa kết quả chấm điểm
        """
        if not self.load_student_code():
            return {
                'score': 0.0,
                'max_score': max_score,
                'passed': 0,
                'total': len(test_cases),
                'error': 'Không thể tải code sinh viên'
            }
        
        # Tạo test class
        TestClass = self.create_test_class(test_cases)
        
        # Chạy tests
        suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
        runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=2)
        result = runner.run(suite)
        
        # Tính điểm
        total = result.testsRun
        passed = total - len(result.failures) - len(result.errors)
        score = (passed / total) * max_score if total > 0 else 0
        
        return {
            'score': round(score, 2),
            'max_score': max_score,
            'passed': passed,
            'total': total,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'details': {
                'failures': [str(f) for f in result.failures],
                'errors': [str(e) for e in result.errors]
            }
        }


# Ví dụ sử dụng
if __name__ == "__main__":
    # Định nghĩa test cases
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
        },
        {
            'function': 'add',
            'inputs': [-1, 1],
            'expected': 0
        }
    ]
    
    # Chấm điểm
    grader = BasicGrader("student_code.py")
    result = grader.grade(test_cases)
    
    print(f"Điểm: {result['score']}/{result['max_score']}")
    print(f"Test passed: {result['passed']}/{result['total']}")
