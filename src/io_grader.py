"""
IO Grader - Chấm điểm dựa trên Input/Output
Kiểm tra đầu ra của chương trình với các đầu vào khác nhau
"""

import subprocess
import sys
import os
from typing import List, Tuple, Dict, Any
from pathlib import Path


class IOGrader:
    """Lớp chấm điểm dựa trên Input/Output"""
    
    def __init__(self, student_file: str, timeout: int = 5):
        """
        Khởi tạo bộ chấm điểm IO
        
        Args:
            student_file: Đường dẫn đến file code sinh viên
            timeout: Thời gian timeout (giây)
        """
        self.student_file = student_file
        self.timeout = timeout
        
    def run_with_input(self, input_data: str) -> Tuple[str, str, int]:
        """
        Chạy file Python với input data
        
        Args:
            input_data: Dữ liệu đầu vào
            
        Returns:
            Tuple (stdout, stderr, return_code)
        """
        try:
            result = subprocess.run(
                [sys.executable, self.student_file],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "TIMEOUT", -1
        except Exception as e:
            return "", str(e), -1
    
    def compare_output(self, actual: str, expected: str, 
                       ignore_whitespace: bool = True,
                       case_sensitive: bool = True) -> bool:
        """
        So sánh output thực tế với expected
        
        Args:
            actual: Output thực tế
            expected: Output mong đợi
            ignore_whitespace: Bỏ qua khoảng trắng
            case_sensitive: Phân biệt hoa thường
            
        Returns:
            True nếu khớp, False nếu không
        """
        if ignore_whitespace:
            actual = actual.strip()
            expected = expected.strip()
        
        if not case_sensitive:
            actual = actual.lower()
            expected = expected.lower()
        
        return actual == expected
    
    def grade(self, test_cases: List[Dict[str, str]], 
              max_score: float = 10.0,
              partial_credit: bool = True) -> Dict[str, Any]:
        """
        Chấm điểm dựa trên test cases IO
        
        Args:
            test_cases: Danh sách test cases với 'input' và 'expected'
            max_score: Điểm tối đa
            partial_credit: Cho phép điểm từng phần
            
        Returns:
            Dictionary chứa kết quả chấm điểm
        """
        if not os.path.exists(self.student_file):
            return {
                'score': 0.0,
                'max_score': max_score,
                'error': 'File không tồn tại'
            }
        
        results = []
        passed = 0
        
        for i, tc in enumerate(test_cases):
            stdout, stderr, returncode = self.run_with_input(tc['input'])
            
            if stderr == "TIMEOUT":
                results.append({
                    'test': i + 1,
                    'status': 'TIMEOUT',
                    'input': tc['input'],
                    'expected': tc['expected'],
                    'actual': None
                })
            elif returncode != 0:
                results.append({
                    'test': i + 1,
                    'status': 'ERROR',
                    'input': tc['input'],
                    'expected': tc['expected'],
                    'actual': stdout,
                    'error': stderr
                })
            else:
                match = self.compare_output(stdout, tc['expected'])
                if match:
                    passed += 1
                    results.append({
                        'test': i + 1,
                        'status': 'PASS',
                        'input': tc['input'],
                        'expected': tc['expected'],
                        'actual': stdout
                    })
                else:
                    results.append({
                        'test': i + 1,
                        'status': 'FAIL',
                        'input': tc['input'],
                        'expected': tc['expected'],
                        'actual': stdout
                    })
        
        # Tính điểm
        total = len(test_cases)
        if partial_credit:
            score = (passed / total) * max_score if total > 0 else 0
        else:
            score = max_score if passed == total else 0
        
        return {
            'score': round(score, 2),
            'max_score': max_score,
            'passed': passed,
            'total': total,
            'results': results
        }
    
    def generate_report(self, result: Dict[str, Any]) -> str:
        """
        Tạo báo cáo chi tiết
        
        Args:
            result: Kết quả từ phương thức grade()
            
        Returns:
            Chuỗi báo cáo
        """
        report = []
        report.append("=" * 60)
        report.append("BÁO CÁO CHẤM ĐIỂM INPUT/OUTPUT")
        report.append("=" * 60)
        report.append(f"Điểm: {result['score']}/{result['max_score']}")
        report.append(f"Test passed: {result['passed']}/{result['total']}")
        report.append("")
        
        for r in result['results']:
            report.append(f"Test {r['test']}: {r['status']}")
            report.append(f"  Input: {repr(r['input'])}")
            report.append(f"  Expected: {repr(r['expected'])}")
            if r['status'] != 'TIMEOUT':
                report.append(f"  Actual: {repr(r['actual'])}")
            if r['status'] == 'ERROR':
                report.append(f"  Error: {r['error']}")
            report.append("")
        
        return "\n".join(report)


### Thử nghiệm
##if __name__ == "__main__":
##    test_cases = [
##        {
##            'input': "5\n3\n",
##            'expected': "8\n"
##        },
##        {
##            'input': "10\n-2\n",
##            'expected': "8\n"
##        },
##        {
##            'input': "0\n0\n",
##            'expected': "0\n"
##        }
##    ]
##    
##    grader = IOGrader("student_io_program.py")
##    result = grader.grade(test_cases)
##    print(grader.generate_report(result))
##
