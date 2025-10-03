"""
Performance Grader - Đánh giá hiệu năng code
Đo thời gian thực thi, memory usage, complexity
"""

import time
import tracemalloc
import importlib.util
import sys
from typing import Dict, Any, List, Callable, Tuple
import statistics
import gc


class PerformanceGrader:
    """Lớp đánh giá hiệu năng code"""
    
    def __init__(self, student_file: str):
        """
        Khởi tạo performance grader
        
        Args:
            student_file: Đường dẫn đến file code sinh viên
        """
        self.student_file = student_file
        self.student_module = None
        
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
            print(f"Error loading code: {e}")
            return False
    
    def measure_execution_time(self, func: Callable, args: Tuple, 
                              iterations: int = 100) -> Dict[str, float]:
        """
        Đo thời gian thực thi
        
        Args:
            func: Hàm cần đo
            args: Tham số đầu vào
            iterations: Số lần chạy
            
        Returns:
            Dictionary chứa các thống kê thời gian
        """
        times = []
        
        for _ in range(iterations):
            gc.collect()  # Chạy garbage collector trước mỗi test
            
            start = time.perf_counter()
            try:
                func(*args)
            except Exception as e:
                return {
                    'error': str(e),
                    'mean': float('inf'),
                    'median': float('inf'),
                    'min': float('inf'),
                    'max': float('inf'),
                    'std': float('inf')
                }
            end = time.perf_counter()
            
            times.append(end - start)
        
        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'min': min(times),
            'max': max(times),
            'std': statistics.stdev(times) if len(times) > 1 else 0,
            'samples': len(times)
        }
    
    def measure_memory_usage(self, func: Callable, args: Tuple) -> Dict[str, int]:
        """
        Đo memory usage
        
        Args:
            func: Hàm cần đo
            args: Tham số đầu vào
            
        Returns:
            Dictionary chứa thông tin memory
        """
        gc.collect()
        tracemalloc.start()
        
        try:
            func(*args)
            current, peak = tracemalloc.get_traced_memory()
        except Exception as e:
            tracemalloc.stop()
            return {
                'error': str(e),
                'current': -1,
                'peak': -1
            }
        
        tracemalloc.stop()
        
        return {
            'current_bytes': current,
            'peak_bytes': peak,
            'current_mb': current / (1024 * 1024),
            'peak_mb': peak / (1024 * 1024)
        }
    
    def compare_with_reference(self, student_func: Callable,
                              reference_func: Callable,
                              test_inputs: List[Tuple],
                              time_weight: float = 0.6,
                              memory_weight: float = 0.4) -> Dict[str, Any]:
        """
        So sánh hiệu năng với hàm tham chiếu
        
        Args:
            student_func: Hàm sinh viên
            reference_func: Hàm tham chiếu
            test_inputs: Danh sách các test inputs
            time_weight: Trọng số thời gian
            memory_weight: Trọng số memory
            
        Returns:
            Dictionary chứa kết quả so sánh
        """
        results = []
        
        for input_data in test_inputs:
            # Đo thời gian
            student_time = self.measure_execution_time(student_func, input_data, 50)
            reference_time = self.measure_execution_time(reference_func, input_data, 50)
            
            if 'error' in student_time:
                time_score = 0
                time_ratio = float('inf')
            else:
                time_ratio = reference_time['mean'] / student_time['mean']
                time_score = min(10, time_ratio * 10)
            
            # Đo memory
            student_memory = self.measure_memory_usage(student_func, input_data)
            reference_memory = self.measure_memory_usage(reference_func, input_data)
            
            if 'error' in student_memory:
                memory_score = 0
                memory_ratio = float('inf')
            else:
                if student_memory['peak_bytes'] > 0:
                    memory_ratio = (reference_memory['peak_bytes'] / 
                                   student_memory['peak_bytes'])
                    memory_score = min(10, memory_ratio * 10)
                else:
                    memory_ratio = 1.0
                    memory_score = 10
            
            # Điểm tổng hợp
            combined_score = (time_score * time_weight + 
                            memory_score * memory_weight)
            
            results.append({
                'input': str(input_data),
                'student_time': student_time,
                'reference_time': reference_time,
                'time_ratio': time_ratio,
                'time_score': time_score,
                'student_memory': student_memory,
                'reference_memory': reference_memory,
                'memory_ratio': memory_ratio,
                'memory_score': memory_score,
                'combined_score': combined_score
            })
        
        # Tính điểm trung bình
        avg_score = statistics.mean(r['combined_score'] for r in results)
        
        return {
            'average_score': avg_score,
            'test_count': len(results),
            'detailed_results': results
        }
    
    def profile_function(self, func_name: str, args: Tuple,
                        iterations: int = 100) -> Dict[str, Any]:
        """
        Profile một hàm cụ thể
        
        Args:
            func_name: Tên hàm
            args: Tham số
            iterations: Số lần chạy
            
        Returns:
            Dictionary chứa profiling results
        """
        func = getattr(self.student_module, func_name, None)
        if func is None:
            return {
                'error': f'Function {func_name} not found'
            }
        
        time_stats = self.measure_execution_time(func, args, iterations)
        memory_stats = self.measure_memory_usage(func, args)
        
        return {
            'function': func_name,
            'time_statistics': time_stats,
            'memory_statistics': memory_stats
        }
    
    def grade_performance(self, func_name: str, reference_func: Callable,
                         test_inputs: List[Tuple],
                         max_score: float = 10.0) -> Dict[str, Any]:
        """
        Chấm điểm performance
        
        Args:
            func_name: Tên hàm sinh viên
            reference_func: Hàm tham chiếu
            test_inputs: Danh sách test inputs
            max_score: Điểm tối đa
            
        Returns:
            Dictionary chứa kết quả chấm điểm
        """
        if not self.load_student_code():
            return {
                'score': 0.0,
                'error': 'Cannot load student code'
            }
        
        student_func = getattr(self.student_module, func_name, None)
        if student_func is None:
            return {
                'score': 0.0,
                'error': f'Function {func_name} not found'
            }
        
        comparison = self.compare_with_reference(
            student_func, reference_func, test_inputs
        )
        
        # Chuẩn hóa điểm
        normalized_score = (comparison['average_score'] / 10.0) * max_score
        
        return {
            'score': round(normalized_score, 2),
            'max_score': max_score,
            'comparison': comparison
        }
    
    def generate_report(self, result: Dict[str, Any]) -> str:
        """
        Tạo báo cáo performance
        
        Args:
            result: Kết quả từ grade_performance()
            
        Returns:
            Chuỗi báo cáo
        """
        report = []
        report.append("=" * 80)
        report.append("PERFORMANCE GRADING REPORT")
        report.append("=" * 80)
        
        if 'error' in result:
            report.append(f"ERROR: {result['error']}")
            return "\n".join(report)
        
        report.append(f"Score: {result['score']:.2f}/{result['max_score']}")
        report.append("")
        
        comparison = result['comparison']
        report.append(f"Tests run: {comparison['test_count']}")
        report.append(f"Average score: {comparison['average_score']:.2f}/10")
        report.append("")
        
        for i, test_result in enumerate(comparison['detailed_results'], 1):
            report.append(f"Test #{i}: {test_result['input']}")
            report.append(f"  Combined Score: {test_result['combined_score']:.2f}/10")
            
            # Time stats
            st = test_result['student_time']
            rt = test_result['reference_time']
            if 'error' not in st:
                report.append(f"  Time:")
                report.append(f"    Student:   {st['mean']*1000:.3f}ms (±{st['std']*1000:.3f}ms)")
                report.append(f"    Reference: {rt['mean']*1000:.3f}ms (±{rt['std']*1000:.3f}ms)")
                report.append(f"    Ratio: {test_result['time_ratio']:.2f}x")
                report.append(f"    Score: {test_result['time_score']:.2f}/10")
            
            # Memory stats
            sm = test_result['student_memory']
            rm = test_result['reference_memory']
            if 'error' not in sm:
                report.append(f"  Memory:")
                report.append(f"    Student Peak:   {sm['peak_mb']:.2f} MB")
                report.append(f"    Reference Peak: {rm['peak_mb']:.2f} MB")
                report.append(f"    Ratio: {test_result['memory_ratio']:.2f}x")
                report.append(f"    Score: {test_result['memory_score']:.2f}/10")
            
            report.append("")
        
        return "\n".join(report)


### Thử nghiệm
##if __name__ == "__main__":
##    grader = PerformanceGrader("student_code.py")
##    
##    # Reference implementation
##    def reference_sort(arr):
##        return sorted(arr)
##    
##    # Test inputs với kích thước khác nhau
##    test_inputs = [
##        ([list(range(100))],),
##        ([list(range(1000))],),
##        ([list(range(10000))],)
##    ]
##    
##    result = grader.grade_performance("my_sort", reference_sort, test_inputs)
##    print(grader.generate_report(result))
##
