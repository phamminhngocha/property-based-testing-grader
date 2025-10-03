"""
Advanced Grader - Hệ thống chấm điểm tích hợp toàn diện
Kết hợp tất cả các phương pháp: basic, IO, weighted, AST, PBT, plagiarism, performance
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import importlib.util

# Import các grader khác
from basic_grader import BasicGrader
from io_grader import IOGrader
from weighted_grader import WeightedGrader
from ast_grader import ASTGrader
from property_based_grader import PropertyBasedGrader
from plagiarism_detector import PlagiarismDetector
from performance_grader import PerformanceGrader


class AdvancedGrader:
    """
    Lớp chấm điểm nâng cao tích hợp tất cả phương pháp
    """
    
    def __init__(self, student_file: str, config: Optional[Dict] = None):
        """
        Khởi tạo advanced grader
        
        Args:
            student_file: Đường dẫn đến file code sinh viên
            config: Cấu hình chấm điểm
        """
        self.student_file = student_file
        self.config = config or self.default_config()
        self.results = {}
        self.grading_time = None
        
    @staticmethod
    def default_config() -> Dict:
        """
        Cấu hình mặc định
        
        Returns:
            Dictionary cấu hình
        """
        return {
            'weights': {
                'functionality': 0.40,    # Kiểm tra chức năng (PBT/Basic)
                'code_quality': 0.20,     # Chất lượng code (AST)
                'performance': 0.20,      # Hiệu năng
                'documentation': 0.10,    # Tài liệu
                'style': 0.10            # Phong cách code
            },
            'enable_pbt': True,
            'enable_performance': True,
            'enable_ast_analysis': True,
            'max_complexity': 10,
            'plagiarism_check': False,
            'timeout': 30
        }
    
    def grade_functionality(self) -> Dict[str, Any]:
        """
        Chấm điểm chức năng sử dụng Property-Based Testing
        
        Returns:
            Dictionary chứa kết quả
        """
        if not self.config.get('enable_pbt'):
            return {'score': 0, 'skipped': True}
        
        try:
            pbt_grader = PropertyBasedGrader(self.student_file)
            
            # Thêm các test tùy theo cấu hình
            # (Ví dụ này giả định có hàm add và sort_list)
            
            # Test các thuộc tính toán học
            from hypothesis import strategies as st
            
            pbt_grader.test_commutativity("add", st.integers(), weight=0.2)
            pbt_grader.test_associativity("add", st.integers(), weight=0.2)
            pbt_grader.test_identity("add", 0, st.integers(), weight=0.1)
            
            # Test với oracle
            pbt_grader.test_with_oracle(
                "sort_list", 
                sorted, 
                st.lists(st.integers()),
                weight=0.5
            )
            
            result = pbt_grader.grade()
            
            return {
                'score': result['score'],
                'passed': result['passed_tests'],
                'total': result['total_tests'],
                'details': result['test_results']
            }
        except Exception as e:
            return {
                'score': 0,
                'error': str(e)
            }
    
    def grade_code_quality(self) -> Dict[str, Any]:
        """
        Chấm điểm chất lượng code (AST analysis)
        
        Returns:
            Dictionary chứa kết quả
        """
        if not self.config.get('enable_ast_analysis'):
            return {'score': 0, 'skipped': True}
        
        try:
            ast_grader = ASTGrader(self.student_file)
            
            structure_requirements = {
                'functions': 2,
                'loops': 1,
                'conditionals': 1
            }
            
            result = ast_grader.grade(
                check_complexity=True,
                check_structure=True,
                check_naming=True,
                check_docs=True,
                structure_requirements=structure_requirements,
                max_complexity=self.config.get('max_complexity', 10)
            )
            
            return {
                'score': result['score'],
                'breakdown': {
                    'complexity': result['results'].get('complexity', {}).get('score', 0),
                    'structure': result['results'].get('structure', {}).get('score', 0),
                    'naming': result['results'].get('naming', {}).get('score', 0),
                    'documentation': result['results'].get('documentation', {}).get('score', 0)
                }
            }
        except Exception as e:
            return {
                'score': 0,
                'error': str(e)
            }
    
    def grade_performance(self, reference_func, test_inputs: List) -> Dict[str, Any]:
        """
        Chấm điểm hiệu năng
        
        Args:
            reference_func: Hàm tham chiếu
            test_inputs: Danh sách test inputs
            
        Returns:
            Dictionary chứa kết quả
        """
        if not self.config.get('enable_performance'):
            return {'score': 0, 'skipped': True}
        
        try:
            perf_grader = PerformanceGrader(self.student_file)
            result = perf_grader.grade_performance(
                'sort_list',  # Tên hàm cần đánh giá
                reference_func,
                test_inputs
            )
            
            return {
                'score': result['score'],
                'comparison': result.get('comparison', {})
            }
        except Exception as e:
            return {
                'score': 0,
                'error': str(e)
            }
    
    def grade_comprehensive(self, reference_func=None, 
                          test_inputs: List = None) -> Dict[str, Any]:
        """
        Chấm điểm toàn diện
        
        Args:
            reference_func: Hàm tham chiếu cho performance testing
            test_inputs: Test inputs cho performance testing
            
        Returns:
            Dictionary chứa kết quả tổng hợp
        """
        start_time = datetime.now()
        
        # 1. Chấm chức năng
        func_result = self.grade_functionality()
        self.results['functionality'] = func_result
        
        # 2. Chấm chất lượng code
        quality_result = self.grade_code_quality()
        self.results['code_quality'] = quality_result
        
        # 3. Chấm hiệu năng (nếu có reference func)
        if reference_func and test_inputs:
            perf_result = self.grade_performance(reference_func, test_inputs)
            self.results['performance'] = perf_result
        else:
            self.results['performance'] = {'score': 0, 'skipped': True}
        
        # Tính điểm tổng
        weights = self.config['weights']
        total_score = 0
        total_weight = 0
        
        for category, weight in weights.items():
            if category in ['functionality', 'code_quality', 'performance']:
                result = self.results.get(category, {})
                if not result.get('skipped', False):
                    score = result.get('score', 0)
                    total_score += score * weight
                    total_weight += weight
        
        # Chuẩn hóa điểm
        final_score = (total_score / total_weight) if total_weight > 0 else 0
        
        end_time = datetime.now()
        self.grading_time = (end_time - start_time).total_seconds()
        
        return {
            'final_score': round(final_score, 2),
            'max_score': 10.0,
            'grade_letter': self.calculate_letter_grade(final_score),
            'category_scores': {
                'functionality': func_result.get('score', 0),
                'code_quality': quality_result.get('score', 0),
                'performance': self.results['performance'].get('score', 0)
            },
            'weights': weights,
            'grading_time_seconds': self.grading_time,
            'timestamp': end_time.isoformat()
        }
    
    @staticmethod
    def calculate_letter_grade(score: float) -> str:
        """
        Chuyển điểm số thành điểm chữ
        
        Args:
            score: Điểm số (0-10)
            
        Returns:
            Điểm chữ
        """
        if score >= 9.0:
            return 'A+'
        elif score >= 8.5:
            return 'A'
        elif score >= 8.0:
            return 'B+'
        elif score >= 7.0:
            return 'B'
        elif score >= 6.5:
            return 'C+'
        elif score >= 5.5:
            return 'C'
        elif score >= 5.0:
            return 'D+'
        elif score >= 4.0:
            return 'D'
        else:
            return 'F'
    
    def generate_detailed_report(self, result: Dict[str, Any]) -> str:
        """
        Tạo báo cáo chi tiết
        
        Args:
            result: Kết quả từ grade_comprehensive()
            
        Returns:
            Chuỗi báo cáo
        """
        report = []
        report.append("=" * 80)
        report.append("COMPREHENSIVE GRADING REPORT")
        report.append("=" * 80)
        report.append(f"File: {self.student_file}")
        report.append(f"Timestamp: {result['timestamp']}")
        report.append(f"Grading Time: {result['grading_time_seconds']:.2f}s")
        report.append("")
        
        report.append(f"FINAL SCORE: {result['final_score']:.2f}/10 ({result['grade_letter']})")
        report.append("")
        
        report.append("CATEGORY BREAKDOWN:")
        report.append("-" * 80)
        
        for category, score in result['category_scores'].items():
            weight = result['weights'].get(category, 0)
            weighted = score * weight
            report.append(f"{category.upper():20s}: {score:5.2f}/10 "
                         f"(weight: {weight:.0%}, weighted: {weighted:.2f})")
        
        report.append("")
        report.append("DETAILED RESULTS:")
        report.append("-" * 80)
        
        # Functionality details
        if 'functionality' in self.results:
            func = self.results['functionality']
            report.append("\n1. FUNCTIONALITY")
            if 'error' in func:
                report.append(f"   ERROR: {func['error']}")
            elif not func.get('skipped'):
                report.append(f"   Score: {func['score']:.2f}/10")
                report.append(f"   Tests Passed: {func.get('passed', 0)}/{func.get('total', 0)}")
                
                if 'details' in func:
                    report.append("   Test Results:")
                    for test in func['details']:
                        status = "✓" if test.get('passed') else "✗"
                        report.append(f"     {status} {test.get('test', 'unknown')}: "
                                    f"{test.get('score', 0):.2f}/10")
        
        # Code quality details
        if 'code_quality' in self.results:
            quality = self.results['code_quality']
            report.append("\n2. CODE QUALITY")
            if 'error' in quality:
                report.append(f"   ERROR: {quality['error']}")
            elif not quality.get('skipped'):
                report.append(f"   Score: {quality['score']:.2f}/10")
                
                if 'breakdown' in quality:
                    report.append("   Breakdown:")
                    for aspect, score in quality['breakdown'].items():
                        report.append(f"     {aspect.capitalize():15s}: {score:.2f}/10")
        
        # Performance details
        if 'performance' in self.results:
            perf = self.results['performance']
            report.append("\n3. PERFORMANCE")
            if 'error' in perf:
                report.append(f"   ERROR: {perf['error']}")
            elif perf.get('skipped'):
                report.append("   SKIPPED")
            else:
                report.append(f"   Score: {perf['score']:.2f}/10")
                
                if 'comparison' in perf:
                    comp = perf['comparison']
                    report.append(f"   Average Score: {comp.get('average_score', 0):.2f}/10")
                    report.append(f"   Tests: {comp.get('test_count', 0)}")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def export_results_json(self, output_file: str):
        """
        Xuất kết quả ra file JSON
        
        Args:
            output_file: Đường dẫn file output
        """
        result = self.grade_comprehensive()
        
        export_data = {
            'student_file': self.student_file,
            'final_score': result['final_score'],
            'grade_letter': result['grade_letter'],
            'timestamp': result['timestamp'],
            'grading_time': result['grading_time_seconds'],
            'category_scores': result['category_scores'],
            'detailed_results': self.results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    def export_results_html(self, output_file: str):
        """
        Xuất kết quả ra file HTML
        
        Args:
            output_file: Đường dẫn file output
        """
        result = self.grade_comprehensive()
        
        html = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grading Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px
