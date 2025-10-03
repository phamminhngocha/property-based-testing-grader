"""
AST Grader - Chấm điểm dựa trên phân tích cú pháp trừu tượng
Kiểm tra cấu trúc code, complexity, naming conventions
"""

import ast
import re
from typing import Dict, List, Any, Set
from pathlib import Path


class ASTGrader:
    """Lớp chấm điểm dựa trên phân tích AST"""
    
    def __init__(self, student_file: str):
        """
        Khởi tạo AST grader
        
        Args:
            student_file: Đường dẫn đến file code sinh viên
        """
        self.student_file = student_file
        self.tree = None
        self.code = None
        
    def load_and_parse(self) -> bool:
        """Đọc và parse file Python"""
        try:
            with open(self.student_file, 'r', encoding='utf-8') as f:
                self.code = f.read()
            self.tree = ast.parse(self.code)
            return True
        except SyntaxError as e:
            print(f"Lỗi cú pháp: {e}")
            return False
        except Exception as e:
            print(f"Lỗi: {e}")
            return False
    
    def check_complexity(self, max_complexity: int = 10) -> Dict[str, Any]:
        """
        Kiểm tra độ phức tạp McCabe Cyclomatic
        
        Args:
            max_complexity: Ngưỡng độ phức tạp tối đa
            
        Returns:
            Dictionary chứa kết quả
        """
        class ComplexityVisitor(ast.NodeVisitor):
            def __init__(self):
                self.complexity = 1
                self.function_complexities = {}
                self.current_function = None
                
            def visit_FunctionDef(self, node):
                old_func = self.current_function
                old_complexity = self.complexity
                
                self.current_function = node.name
                self.complexity = 1
                self.generic_visit(node)
                
                self.function_complexities[node.name] = self.complexity
                
                self.current_function = old_func
                self.complexity = old_complexity
                
            def visit_If(self, node):
                self.complexity += 1
                self.generic_visit(node)
            
            def visit_While(self, node):
                self.complexity += 1
                self.generic_visit(node)
            
            def visit_For(self, node):
                self.complexity += 1
                self.generic_visit(node)
            
            def visit_ExceptHandler(self, node):
                self.complexity += 1
                self.generic_visit(node)
            
            def visit_BoolOp(self, node):
                self.complexity += len(node.values) - 1
                self.generic_visit(node)
        
        visitor = ComplexityVisitor()
        visitor.visit(self.tree)
        
        violations = {
            func: comp 
            for func, comp in visitor.function_complexities.items() 
            if comp > max_complexity
        }
        
        avg_complexity = (sum(visitor.function_complexities.values()) / 
                         len(visitor.function_complexities) 
                         if visitor.function_complexities else 0)
        
        passed = len(violations) == 0
        score = max(0, 10 - len(violations) * 2)
        
        return {
            'passed': passed,
            'score': score,
            'average_complexity': avg_complexity,
            'function_complexities': visitor.function_complexities,
            'violations': violations
        }
    
    def check_code_structure(self, requirements: Dict[str, int]) -> Dict[str, Any]:
        """
        Kiểm tra cấu trúc code theo yêu cầu
        
        Args:
            requirements: Dictionary chứa yêu cầu (ví dụ: {'functions': 3})
            
        Returns:
            Dictionary chứa kết quả
        """
        class StructureVisitor(ast.NodeVisitor):
            def __init__(self):
                self.functions = []
                self.classes = []
                self.loops = []
                self.conditionals = []
                self.list_comprehensions = []
                self.decorators = []
                self.context_managers = []
                self.imports = []
                
            def visit_FunctionDef(self, node):
                self.functions.append(node.name)
                if node.decorator_list:
                    self.decorators.extend([
                        ast.unparse(d) for d in node.decorator_list
                    ])
                self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                self.classes.append(node.name)
                self.generic_visit(node)
            
            def visit_For(self, node):
                self.loops.append('for')
                self.generic_visit(node)
            
            def visit_While(self, node):
                self.loops.append('while')
                self.generic_visit(node)
            
            def visit_If(self, node):
                self.conditionals.append('if')
                self.generic_visit(node)
            
            def visit_ListComp(self, node):
                self.list_comprehensions.append(ast.unparse(node))
                self.generic_visit(node)
            
            def visit_With(self, node):
                self.context_managers.append('with')
                self.generic_visit(node)
            
            def visit_Import(self, node):
                self.imports.extend([alias.name for alias in node.names])
            
            def visit_ImportFrom(self, node):
                self.imports.append(node.module)
        
        visitor = StructureVisitor()
        visitor.visit(self.tree)
        
        found = {
            'functions': len(visitor.functions),
            'classes': len(visitor.classes),
            'loops': len(visitor.loops),
            'conditionals': len(visitor.conditionals),
            'list_comprehensions': len(visitor.list_comprehensions),
            'decorators': len(visitor.decorators),
            'context_managers': len(visitor.context_managers),
            'imports': len(visitor.imports)
        }
        
        violations = []
        satisfied = 0
        
        for key, required_count in requirements.items():
            actual_count = found.get(key, 0)
            if actual_count >= required_count:
                satisfied += 1
            else:
                violations.append({
                    'requirement': key,
                    'required': required_count,
                    'found': actual_count
                })
        
        total_requirements = len(requirements)
        score = (satisfied / total_requirements * 10) if total_requirements > 0 else 10
        
        return {
            'passed': len(violations) == 0,
            'score': score,
            'satisfied': satisfied,
            'total_requirements': total_requirements,
            'found': found,
            'violations': violations,
            'details': {
                'function_names': visitor.functions,
                'class_names': visitor.classes
            }
        }
    
    def check_naming_conventions(self) -> Dict[str, Any]:
        """
        Kiểm tra quy tắc đặt tên (PEP 8)
        
        Returns:
            Dictionary chứa kết quả
        """
        class NamingVisitor(ast.NodeVisitor):
            def __init__(self):
                self.violations = []
                self.total_names = 0
                
            def check_snake_case(self, name: str, node_type: str, lineno: int):
                self.total_names += 1
                if node_type == 'class':
                    # Classes should be PascalCase
                    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
                        self.violations.append({
                            'name': name,
                            'type': node_type,
                            'line': lineno,
                            'issue': 'Should be PascalCase'
                        })
                else:
                    # Functions and variables should be snake_case
                    if not re.match(r'^[a-z_][a-z0-9_]*$', name):
                        self.violations.append({
                            'name': name,
                            'type': node_type,
                            'line': lineno,
                            'issue': 'Should be snake_case'
                        })
            
            def visit_FunctionDef(self, node):
                self.check_snake_case(node.name, 'function', node.lineno)
                self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                self.check_snake_case(node.name, 'class', node.lineno)
                self.generic_visit(node)
            
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Store):
                    self.check_snake_case(node.id, 'variable', node.lineno)
                self.generic_visit(node)
        
        visitor = NamingVisitor()
        visitor.visit(self.tree)
        
        compliance_rate = (
            1 - (len(visitor.violations) / visitor.total_names)
            if visitor.total_names > 0 else 1
        )
        score = compliance_rate * 10
        
        return {
            'passed': len(visitor.violations) == 0,
            'score': score,
            'compliance_rate': compliance_rate,
            'total_names': visitor.total_names,
            'violations': visitor.violations
        }
    
    def check_documentation(self) -> Dict[str, Any]:
        """
        Kiểm tra documentation (docstrings)
        
        Returns:
            Dictionary chứa kết quả
        """
        class DocVisitor(ast.NodeVisitor):
            def __init__(self):
                self.functions = []
                self.classes = []
                
            def visit_FunctionDef(self, node):
                docstring = ast.get_docstring(node)
                self.functions.append({
                    'name': node.name,
                    'has_docstring': docstring is not None,
                    'docstring_length': len(docstring) if docstring else 0
                })
                self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                docstring = ast.get_docstring(node)
                self.classes.append({
                    'name': node.name,
                    'has_docstring': docstring is not None,
                    'docstring_length': len(docstring) if docstring else 0
                })
                self.generic_visit(node)
        
        visitor = DocVisitor()
        visitor.visit(self.tree)
        
        total_items = len(visitor.functions) + len(visitor.classes)
        documented_items = sum(
            1 for item in visitor.functions + visitor.classes 
            if item['has_docstring']
        )
        
        if total_items > 0:
            coverage = documented_items / total_items
            avg_length = sum(
                item['docstring_length'] 
                for item in visitor.functions + visitor.classes 
                if item['has_docstring']
            ) / documented_items if documented_items > 0 else 0
            
            # Quality score based on coverage and length
            quality = min(1.0, avg_length / 50)  # Expect at least 50 chars
            score = (coverage * 0.7 + quality * 0.3) * 10
        else:
            coverage = 0
            avg_length = 0
            score = 0
        
        return {
            'passed': coverage >= 0.8,
            'score': score,
            'coverage': coverage,
            'average_length': avg_length,
            'documented': documented_items,
            'total': total_items,
            'details': {
                'functions': visitor.functions,
                'classes': visitor.classes
            }
        }
    
    def grade(self, 
              check_complexity: bool = True,
              check_structure: bool = True,
              check_naming: bool = True,
              check_docs: bool = True,
              structure_requirements: Dict[str, int] = None,
              max_complexity: int = 10) -> Dict[str, Any]:
        """
        Chấm điểm toàn diện
        
        Args:
            check_complexity: Kiểm tra độ phức tạp
            check_structure: Kiểm tra cấu trúc
            check_naming: Kiểm tra quy tắc đặt tên
            check_docs: Kiểm tra documentation
            structure_requirements: Yêu cầu về cấu trúc
            max_complexity: Độ phức tạp tối đa
            
        Returns:
            Kết quả chấm điểm chi tiết
        """
        if not self.load_and_parse():
            return {
                'score': 0,
                'error': 'Không thể parse file'
            }
        
        results = {}
        total_score = 0
        total_weight = 0
        
        if check_complexity:
            results['complexity'] = self.check_complexity(max_complexity)
            total_score += results['complexity']['score'] * 0.25
            total_weight += 0.25
        
        if check_structure and structure_requirements:
            results['structure'] = self.check_code_structure(structure_requirements)
            total_score += results['structure']['score'] * 0.25
            total_weight += 0.25
        
        if check_naming:
            results['naming'] = self.check_naming_conventions()
            total_score += results['naming']['score'] * 0.25
            total_weight += 0.25
        
        if check_docs:
            results['documentation'] = self.check_documentation()
            total_score += results['documentation']['score'] * 0.25
            total_weight += 0.25
        
        final_score = total_score / total_weight if total_weight > 0 else 0
        
        return {
            'score': round(final_score, 2),
            'max_score': 10.0,
            'results': results
        }


# Ví dụ sử dụng
if __name__ == "__main__":
    grader = ASTGrader("student_code.py")
    
    structure_req = {
        'functions': 3,
        'classes': 1,
        'loops': 2
    }
    
    result = grader.grade(structure_requirements=structure_req)
    print(f"Điểm: {result['score']}/10")
    
    for category, details in result['results'].items():
        print(f"\n{category.upper()}: {details['score']:.1f}/10")
        if not details['passed']:
            print(f"  Violations: {details.get('violations', [])}")
