"""
Weighted Grader - Chấm điểm có trọng số
Cho phép gán trọng số khác nhau cho các nhóm test
"""

import importlib.util
from typing import Dict, List, Any, Callable
import traceback


class WeightedGrader:
    """Lớp chấm điểm có trọng số cho các nhóm test"""
    
    def __init__(self, student_file: str):
        """
        Khởi tạo bộ chấm điểm có trọng số
        
        Args:
            student_file: Đường dẫn đến file code sinh viên
        """
        self.student_file = student_file
        self.student_module = None
        self.test_groups = []
        
    def load_student_code(self) -> bool:
        """Tải module code của sinh viên"""
        try:
            spec = importlib.util.spec_from_file_location(
                "student", self.student_file
            )
            self.student_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.student_module)
            return True
        except Exception as e:
            print(f"Lỗi: {e}")
            return False
    
    def add_test_group(self, name: str, tests: List[Callable], 
                       weight: float):
        """
        Thêm nhóm test với trọng số
        
        Args:
            name: Tên nhóm test
            tests: Danh sách các hàm test
            weight: Trọng số (0-1 hoặc 0-100)
        """
        self.test_groups.append({
            'name': name,
            'tests': tests,
            'weight': weight
        })
    
    def run_test_group(self, group: Dict) -> Dict[str, Any]:
        """
        Chạy một nhóm test
        
        Args:
            group: Dictionary chứa thông tin nhóm test
            
        Returns:
            Kết quả nhóm test
        """
        passed = 0
        total = len(group['tests'])
        errors = []
        
        for test_func in group['tests']:
            try:
                test_func(self.student_module)
                passed += 1
            except AssertionError as e:
                errors.append({
                    'test': test_func.__name__,
                    'error': str(e)
                })
            except Exception as e:
                errors.append({
                    'test': test_func.__name__,
                    'error': f"Runtime error: {str(e)}"
                })
        
        success_rate = passed / total if total > 0 else 0
        weighted_score = success_rate * group['weight']
        
        return {
            'name': group['name'],
            'passed': passed,
            'total': total,
            'success_rate': success_rate,
            'weight': group['weight'],
            'weighted_score': weighted_score,
            'errors': errors
        }
    
    def grade(self, max_score: float = 10.0) -> Dict[str, Any]:
        """
        Chấm điểm tất cả các nhóm test
        
        Args:
            max_score: Điểm tối đa
            
        Returns:
            Kết quả chấm điểm chi tiết
        """
        if not self.load_student_code():
            return {
                'score': 0.0,
                'max_score': max_score,
                'error': 'Không thể tải code sinh viên'
            }
        
        group_results = []
        total_weight = sum(g['weight'] for g in self.test_groups)
        total_weighted_score = 0
        
        for group in self.test_groups:
            result = self.run_test_group(group)
            group_results.append(result)
            total_weighted_score += result['weighted_score']
        
        # Chuẩn hóa điểm
        if total_weight > 0:
            normalized_score = (total_weighted_score / total_weight) * max_score
        else:
            normalized_score = 0
        
        return {
            'score': round(normalized_score, 2),
            'max_score': max_score,
            'total_weight': total_weight,
            'total_weighted_score': total_weighted_score,
            'group_results': group_results
        }
    
    def generate_report(self, result: Dict[str, Any]) -> str:
        """Tạo báo cáo chi tiết"""
        report = []
        report.append("=" * 70)
        report.append("BÁO CÁO CHẤM ĐIỂM CÓ TRỌNG SỐ")
        report.append("=" * 70)
        report.append(f"Điểm cuối: {result['score']}/{result['max_score']}")
        report.append(f"Tổng trọng số: {result['total_weight']}")
        report.append("")
        
        for gr in result['group_results']:
            report.append(f"Nhóm: {gr['name']}")
            report.append(f"  Tests passed: {gr['passed']}/{gr['total']}")
            report.append(f"  Tỷ lệ thành công: {gr['success_rate']:.1%}")
            report.append(f"  Trọng số: {gr['weight']}")
            report.append(f"  Điểm trọng số: {gr['weighted_score']:.2f}")
            
            if gr['errors']:
                report.append("  Lỗi:")
                for err in gr['errors']:
                    report.append(f"    - {err['test']}: {err['error']}")
            report.append("")
        
        return "\n".join(report)


# Ví dụ sử dụng
if __name__ == "__main__":
    # Định nghĩa các test functions
    def test_basic_add(module):
        assert module.add(2, 3) == 5, "add(2,3) should be 5"
        assert module.add(0, 0) == 0, "add(0,0) should be 0"
    
    def test_negative_add(module):
        assert module.add(-1, 1) == 0, "add(-1,1) should be 0"
        assert module.add(-5, -3) == -8, "add(-5,-3) should be -8"
    
    def test_edge_cases(module):
        assert module.add(1000000, 1) == 1000001
        assert module.add(-1000000, 1000000) == 0
    
    # Khởi tạo grader
    grader = WeightedGrader("student_code.py")
    
    # Thêm các nhóm test với trọng số
    grader.add_test_group("Basic Tests", [test_basic_add], weight=0.3)
    grader.add_test_group("Negative Numbers", [test_negative_add], weight=0.3)
    grader.add_test_group("Edge Cases", [test_edge_cases], weight=0.4)
    
    # Chấm điểm
    result = grader.grade()
    print(grader.generate_report(result))
