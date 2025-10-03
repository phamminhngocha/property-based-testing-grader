"""
Property-Based Grader - Chấm điểm dựa trên thuộc tính với Hypothesis
Tự động tạo hàng nghìn test cases từ đặc tả thuộc tính
"""

from hypothesis import given, strategies as st, settings, example
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
import importlib.util
import sys
from typing import Callable, Any, List, Dict
import traceback


class PropertyBasedGrader:
    """Lớp chấm điểm dựa trên Property-Based Testing"""
    
    def __init__(self, student_file: str):
        """
        Khởi tạo PBT grader
        
        Args:
            student_file: Đường dẫn đến file code sinh viên
        """
        self.student_file = student_file
        self.student_module = None
        self.test_results = []
        
    def load_student_code(self) -> bool:
        """Tải module code của sinh viên"""
        try:
            spec = importlib.util.spec_from_file_location(
                "student", self.student_file
            )
            self.student_module = importlib.util.module_from_spec(spec)
            sys.modules["student"] = self.student_module
            spec.loader.exec_module(self.student_module)
            return True
        except Exception as e:
            print(f"Lỗi khi tải code: {e}")
            return False
    
    def test_commutativity(self, func_name: str, strategy, 
                          weight: float = 1.0) -> Dict[str, Any]:
        """
        Kiểm tra tính giao hoán: f(a, b) == f(b, a)
        
        Args:
            func_name: Tên hàm cần kiểm tra
            strategy: Hypothesis strategy để tạo dữ liệu
            weight: Trọng số điểm
            
        Returns:
            Dictionary chứa kết quả
        """
        func = getattr(self.student_module, func_name, None)
        if func is None:
            return {
                'test': 'commutativity',
                'passed': False,
                'score': 0.0,
                'error': f'Function {func_name} not found'
            }
        
        failures = []
        
        @given(strategy, strategy)
        @settings(max_examples=1000, deadline=1000)
        def test(a, b):
            try:
                result1 = func(a, b)
                result2 = func(b, a)
                assert result1 == result2, \
                    f"f({a},{b})={result1} != f({b},{a})={result2}"
            except AssertionError as e:
                failures.append(str(e))
                raise
            except Exception as e:
                failures.append(f"Runtime error: {e}")
                raise AssertionError(f"Error: {e}")
        
        try:
            test()
            result = {
                'test': 'commutativity',
                'passed': True,
                'score': 10.0 * weight,
                'function': func_name
            }
        except Exception:
            result = {
                'test': 'commutativity',
                'passed': False,
                'score': 0.0,
                'function': func_name,
                'failures': failures[:5]  # Chỉ lưu 5 lỗi đầu
            }
        
        self.test_results.append(result)
        return result
    
    def test_associativity(self, func_name: str, strategy,
                          weight: float = 1.0) -> Dict[str, Any]:
        """
        Kiểm tra tính kết hợp: f(f(a,b),c) == f(a,f(b,c))
        
        Args:
            func_name: Tên hàm cần kiểm tra
            strategy: Hypothesis strategy
            weight: Trọng số điểm
            
        Returns:
            Dictionary chứa kết quả
        """
        func = getattr(self.student_module, func_name, None)
        if func is None:
            return {
                'test': 'associativity',
                'passed': False,
                'score': 0.0,
                'error': f'Function {func_name} not found'
            }
        
        failures = []
        
        @given(strategy, strategy, strategy)
        @settings(max_examples=1000, deadline=1000)
        def test(a, b, c):
            try:
                left = func(func(a, b), c)
                right = func(a, func(b, c))
                assert left == right, \
                    f"f(f({a},{b}),{c})={left} != f({a},f({b},{c}))={right}"
            except AssertionError as e:
                failures.append(str(e))
                raise
        
        try:
            test()
            result = {
                'test': 'associativity',
                'passed': True,
                'score': 10.0 * weight,
                'function': func_name
            }
        except Exception:
            result = {
                'test': 'associativity',
                'passed': False,
                'score': 0.0,
                'function': func_name,
                'failures': failures[:5]
            }
        
        self.test_results.append(result)
        return result
    
    def test_identity(self, func_name: str, identity_value: Any,
                     strategy, weight: float = 1.0) -> Dict[str, Any]:
        """
        Kiểm tra phần tử đơn vị: f(a, identity) == a
        
        Args:
            func_name: Tên hàm
            identity_value: Giá trị đơn vị (ví dụ: 0 cho phép cộng)
            strategy: Hypothesis strategy
            weight: Trọng số
            
        Returns:
            Dictionary chứa kết quả
        """
        func = getattr(self.student_module, func_name, None)
        if func is None:
            return {
                'test': 'identity',
                'passed': False,
                'score': 0.0,
                'error': f'Function {func_name} not found'
            }
        
        failures = []
        
        @given(strategy)
        @settings(max_examples=500)
        def test(a):
            try:
                result1 = func(a, identity_value)
                result2 = func(identity_value, a)
                assert result1 == a, f"f({a},{identity_value})={result1} != {a}"
                assert result2 == a, f"f({identity_value},{a})={result2} != {a}"
            except AssertionError as e:
                failures.append(str(e))
                raise
        
        try:
            test()
            result = {
                'test': 'identity',
                'passed': True,
                'score': 10.0 * weight,
                'function': func_name
            }
        except Exception:
            result = {
                'test': 'identity',
                'passed': False,
                'score': 0.0,
                'function': func_name,
                'failures': failures[:5]
            }
        
        self.test_results.append(result)
        return result
    
    def test_monotonicity(self, func_name: str, strategy,
                         weight: float = 1.0) -> Dict[str, Any]:
        """
        Kiểm tra tính đơn điệu: a <= b => f(a) <= f(b)
        
        Args:
            func_name: Tên hàm
            strategy: Hypothesis strategy
            weight: Trọng số
            
        Returns:
            Dictionary chứa kết quả
        """
        func = getattr(self.student_module, func_name, None)
        if func is None:
            return {
                'test': 'monotonicity',
                'passed': False,
                'score': 0.0,
                'error': f'Function {func_name} not found'
            }
        
        failures = []
        
        @given(strategy, strategy)
        @settings(max_examples=1000)
        def test(a, b):
            try:
                if a <= b:
                    fa = func(a)
                    fb = func(b)
                    assert fa <= fb, \
                        f"{a}<={b} but f({a})={fa} > f({b})={fb}"
            except AssertionError as e:
                failures.append(str(e))
                raise
        
        try:
            test()
            result = {
                'test': 'monotonicity',
                'passed': True,
                'score': 10.0 * weight,
                'function': func_name
            }
        except Exception:
            result = {
                'test': 'monotonicity',
                'passed': False,
                'score': 0.0,
                'function': func_name,
                'failures': failures[:5]
            }
        
        self.test_results.append(result)
        return result
    
    def test_idempotence(self, func_name: str, strategy,
                        weight: float = 1.0) -> Dict[str, Any]:
        """
        Kiểm tra tính lũy đẳng: f(f(a)) == f(a)
        
        Args:
            func_name: Tên hàm
            strategy: Hypothesis strategy
            weight: Trọng số
            
        Returns:
            Dictionary chứa kết quả
        """
        func = getattr(self.student_module, func_name, None)
        if func is None:
            return {
                'test': 'idempotence',
                'passed': False,
                'score': 0.0,
                'error': f'Function {func_name} not found'
            }
        
        failures = []
        
        @given(strategy)
        @settings(max_examples=500)
        def test(a):
            try:
                once = func(a)
                twice = func(once)
                assert once == twice, \
                    f"f(f({a}))={twice} != f({a})={once}"
            except AssertionError as e:
                failures.append(str(e))
                raise
        
        try:
            test()
            result = {
                'test': 'idempotence',
                'passed': True,
                'score': 10.0 * weight,
                'function': func_name
            }
        except Exception:
            result = {
                'test': 'idempotence',
                'passed': False,
                'score': 0.0,
                'function': func_name,
                'failures': failures[:5]
            }
        
        self.test_results.append(result)
        return result
    
    def test_with_oracle(self, func_name: str, oracle: Callable,
                        strategy, weight: float = 1.0) -> Dict[str, Any]:
        """
        Kiểm tra với reference implementation
        
        Args:
            func_name: Tên hàm sinh viên
            oracle: Hàm tham chiếu
            strategy: Hypothesis strategy
            weight: Trọng số
            
        Returns:
            Dictionary chứa kết quả
        """
        student_func = getattr(self.student_module, func_name, None)
        if student_func is None:
            return {
                'test': 'oracle',
                'passed': False,
                'score': 0.0,
                'error': f'Function {func_name} not found'
            }
        
        failures = []
        
        @given(strategy)
        @settings(max_examples=1000, deadline=2000)
        def test(input_data):
            try:
                student_result = student_func(input_data)
                oracle_result = oracle(input_data)
                assert student_result == oracle_result, \
                    f"Input: {input_data}\nStudent: {student_result}\nOracle: {oracle_result}"
            except AssertionError as e:
                failures.append(str(e))
                raise
            except Exception as e:
                failures.append(f"Runtime error: {e}")
                raise AssertionError(f"Error: {e}")
        
        try:
            test()
            result = {
                'test': 'oracle',
                'passed': True,
                'score': 10.0 * weight,
                'function': func_name
            }
        except Exception:
            # Tính điểm dựa trên tỷ lệ thất bại
            failure_rate = len(failures) / 1000
            partial_score = max(0, 10.0 * (1 - failure_rate) * weight)
            result = {
                'test': 'oracle',
                'passed': False,
                'score': partial_score,
                'function': func_name,
                'failure_rate': failure_rate,
                'failures': failures[:5]
            }
        
        self.test_results.append(result)
        return result
    
    def test_custom_invariants(self, func_name: str, 
                              invariants: List[Callable],
                              strategy, weight: float = 1.0) -> Dict[str, Any]:
        """
        Kiểm tra các bất biến tùy chỉnh
        
        Args:
            func_name: Tên hàm
            invariants: Danh sách các hàm kiểm tra bất biến
            strategy: Hypothesis strategy
            weight: Trọng số
            
        Returns:
            Dictionary chứa kết quả
        """
        func = getattr(self.student_module, func_name, None)
        if func is None:
            return {
                'test': 'custom_invariants',
                'passed': False,
                'score': 0.0,
                'error': f'Function {func_name} not found'
            }
        
        invariant_results = []
        
        for invariant in invariants:
            failures = []
            
            @given(strategy)
            @settings(max_examples=500)
            def test(input_data):
                try:
                    result = func(input_data)
                    assert invariant(input_data, result), \
                        f"Invariant {invariant.__name__} violated"
                except AssertionError as e:
                    failures.append(str(e))
                    raise
            
            try:
                test()
                invariant_results.append({
                    'invariant': invariant.__name__,
                    'passed': True
                })
            except Exception:
                invariant_results.append({
                    'invariant': invariant.__name__,
                    'passed': False,
                    'failures': failures[:3]
                })
        
        passed_count = sum(1 for r in invariant_results if r['passed'])
        total_count = len(invariants)
        score = (passed_count / total_count * 10.0 * weight) if total_count > 0 else 0
        
        result = {
            'test': 'custom_invariants',
            'passed': passed_count == total_count,
            'score': score,
            'function': func_name,
            'passed_invariants': passed_count,
            'total_invariants': total_count,
            'invariant_results': invariant_results
        }
        
        self.test_results.append(result)
        return result
    
    def grade(self) -> Dict[str, Any]:
        """
        Tính điểm cuối cùng
        
        Returns:
            Dictionary chứa tổng kết điểm
        """
        if not self.load_student_code():
            return {
                'score': 0.0,
                'max_score': 10.0,
                'error': 'Cannot load student code'
            }
        
        if not self.test_results:
            return {
                'score': 0.0,
                'max_score': 10.0,
                'error': 'No tests run'
            }
        
        total_score = sum(r.get('score', 0) for r in self.test_results)
        total_tests = len(self.test_results)
        max_possible = total_tests * 10.0
        
        normalized_score = (total_score / max_possible * 10.0) if max_possible > 0 else 0
        
        passed_tests = sum(1 for r in self.test_results if r.get('passed', False))
        
        return {
            'score': round(normalized_score, 2),
            'max_score': 10.0,
            'total_score': total_score,
            'max_possible': max_possible,
            'passed_tests': passed_tests,
            'total_tests': total_tests,
            'test_results': self.test_results
        }
    
    def generate_report(self) -> str:
        """
        Tạo báo cáo chi tiết
        
        Returns:
            Chuỗi báo cáo
        """
        result = self.grade()
        
        report = []
        report.append("=" * 70)
        report.append("PROPERTY-BASED TESTING GRADING REPORT")
        report.append("=" * 70)
        report.append(f"Final Score: {result['score']:.2f}/{result['max_score']}")
        report.append(f"Tests Passed: {result['passed_tests']}/{result['total_tests']}")
        report.append("")
        
        for test_result in result['test_results']:
            status = "✓ PASS" if test_result.get('passed') else "✗ FAIL"
            report.append(f"{status} - {test_result['test'].upper()}")
            report.append(f"  Function: {test_result.get('function', 'N/A')}")
            report.append(f"  Score: {test_result.get('score', 0):.2f}/10")
            
            if not test_result.get('passed') and 'failures' in test_result:
                report.append("  Sample failures:")
                for failure in test_result['failures']:
                    report.append(f"    - {failure}")
            
            if 'invariant_results' in test_result:
                report.append("  Invariant results:")
                for inv in test_result['invariant_results']:
                    inv_status = "✓" if inv['passed'] else "✗"
                    report.append(f"    {inv_status} {inv['invariant']}")
            
            report.append("")
        
        return "\n".join(report)


### Thử nghiệm
##if __name__ == "__main__":
##    grader = PropertyBasedGrader("student_code.py")
##    
##    # Test 1: Tính giao hoán của phép cộng
##    grader.test_commutativity("add", st.integers(), weight=0.2)
##    
##    # Test 2: Tính kết hợp của phép cộng
##    grader.test_associativity("add", st.integers(), weight=0.2)
##    
##    # Test 3: Phần tử đơn vị (0 cho phép cộng)
##    grader.test_identity("add", 0, st.integers(), weight=0.2)
##    
##    # Test 4: So sánh với hàm chuẩn
##    grader.test_with_oracle("sort_list", sorted, 
##                           st.lists(st.integers()), weight=0.4)
##    
##    # In báo cáo
##    print(grader.generate_report())
##
