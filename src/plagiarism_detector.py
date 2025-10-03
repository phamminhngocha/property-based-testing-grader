"""
Plagiarism Detector - Phát hiện đạo văn trong code
Sử dụng phân tích AST và so sánh cấu trúc
"""

import ast
import difflib
from collections import defaultdict
from typing import Dict, List, Tuple, Set
import hashlib


class PlagiarismDetector:
    """Lớp phát hiện đạo văn giữa các file code"""
    
    def __init__(self, similarity_threshold: float = 0.8):
        """
        Khởi tạo plagiarism detector
        
        Args:
            similarity_threshold: Ngưỡng tương đồng (0-1)
        """
        self.similarity_threshold = similarity_threshold
        
    def normalize_code(self, code: str) -> str:
        """
        Chuẩn hóa code bằng cách loại bỏ comments, docstrings
        
        Args:
            code: Mã nguồn gốc
            
        Returns:
            Mã nguồn đã chuẩn hóa
        """
        try:
            tree = ast.parse(code)
            
            # Loại bỏ docstrings
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    if (node.body and isinstance(node.body[0], ast.Expr) 
                        and isinstance(node.body[0].value, (ast.Str, ast.Constant))):
                        node.body = node.body[1:]
            
            return ast.unparse(tree)
        except:
            # Nếu parse thất bại, trả về code gốc
            return code
    
    def normalize_ast(self, code: str) -> str:
        """
        Chuẩn hóa AST bằng cách thay thế tên biến
        
        Args:
            code: Mã nguồn
            
        Returns:
            Mã nguồn đã chuẩn hóa AST
        """
        try:
            tree = ast.parse(code)
        except:
            return ""
        
        class Normalizer(ast.NodeTransformer):
            def __init__(self):
                self.var_counter = 0
                self.var_map = {}
                self.func_counter = 0
                self.func_map = {}
            
            def visit_Name(self, node):
                if node.id not in self.var_map:
                    self.var_map[node.id] = f"var_{self.var_counter}"
                    self.var_counter += 1
                node.id = self.var_map[node.id]
                return node
            
            def visit_FunctionDef(self, node):
                # Chuẩn hóa tên hàm
                if node.name not in self.func_map:
                    self.func_map[node.name] = f"func_{self.func_counter}"
                    self.func_counter += 1
                node.name = self.func_map[node.name]
                
                # Loại bỏ docstring
                if (node.body and isinstance(node.body[0], ast.Expr) 
                    and isinstance(node.body[0].value, (ast.Str, ast.Constant))):
                    node.body = node.body[1:]
                
                self.generic_visit(node)
                return node
            
            def visit_ClassDef(self, node):
                node.name = "Class"
                self.generic_visit(node)
                return node
        
        normalizer = Normalizer()
        normalized = normalizer.visit(tree)
        
        try:
            return ast.unparse(normalized)
        except:
            return ""
    
    def calculate_text_similarity(self, code1: str, code2: str) -> float:
        """
        Tính độ tương đồng văn bản đơn giản
        
        Args:
            code1: Mã nguồn 1
            code2: Mã nguồn 2
            
        Returns:
            Độ tương đồng (0-1)
        """
        norm1 = self.normalize_code(code1)
        norm2 = self.normalize_code(code2)
        
        matcher = difflib.SequenceMatcher(None, norm1, norm2)
        return matcher.ratio()
    
    def calculate_ast_similarity(self, code1: str, code2: str) -> float:
        """
        Tính độ tương đồng cấu trúc AST
        
        Args:
            code1: Mã nguồn 1
            code2: Mã nguồn 2
            
        Returns:
            Độ tương đồng (0-1)
        """
        norm1 = self.normalize_ast(code1)
        norm2 = self.normalize_ast(code2)
        
        if not norm1 or not norm2:
            return 0.0
        
        matcher = difflib.SequenceMatcher(None, norm1, norm2)
        return matcher.ratio()
    
    def get_code_fingerprint(self, code: str) -> Set[str]:
        """
        Tạo fingerprint từ code (n-grams của AST nodes)
        
        Args:
            code: Mã nguồn
            
        Returns:
            Set các fingerprint
        """
        try:
            tree = ast.parse(code)
        except:
            return set()
        
        fingerprints = set()
        
        # Tạo n-grams từ chuỗi các node types
        node_sequence = []
        for node in ast.walk(tree):
            node_sequence.append(type(node).__name__)
        
        # 3-grams
        for i in range(len(node_sequence) - 2):
            trigram = tuple(node_sequence[i:i+3])
            fingerprints.add(trigram)
        
        return fingerprints
    
    def calculate_fingerprint_similarity(self, code1: str, code2: str) -> float:
        """
        Tính độ tương đồng dựa trên fingerprints
        
        Args:
            code1: Mã nguồn 1
            code2: Mã nguồn 2
            
        Returns:
            Độ tương đồng (0-1)
        """
        fp1 = self.get_code_fingerprint(code1)
        fp2 = self.get_code_fingerprint(code2)
        
        if not fp1 or not fp2:
            return 0.0
        
        intersection = len(fp1 & fp2)
        union = len(fp1 | fp2)
        
        return intersection / union if union > 0 else 0.0
    
    def calculate_structure_hash(self, code: str) -> str:
        """
        Tạo hash từ cấu trúc code
        
        Args:
            code: Mã nguồn
            
        Returns:
            Hash string
        """
        normalized = self.normalize_ast(code)
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def compare_pair(self, file1: str, code1: str, 
                    file2: str, code2: str) -> Dict:
        """
        So sánh một cặp file
        
        Args:
            file1: Tên file 1
            code1: Mã nguồn 1
            file2: Tên file 2
            code2: Mã nguồn 2
            
        Returns:
            Dictionary chứa kết quả so sánh
        """
        text_sim = self.calculate_text_similarity(code1, code2)
        ast_sim = self.calculate_ast_similarity(code1, code2)
        fp_sim = self.calculate_fingerprint_similarity(code1, code2)
        
        # Tính similarity trung bình có trọng số
        weighted_sim = (text_sim * 0.3 + ast_sim * 0.4 + fp_sim * 0.3)
        
        status = "SUSPICIOUS" if weighted_sim >= self.similarity_threshold else "OK"
        
        return {
            'file1': file1,
            'file2': file2,
            'text_similarity': text_sim,
            'ast_similarity': ast_sim,
            'fingerprint_similarity': fp_sim,
            'overall_similarity': weighted_sim,
            'status': status
        }
    
    def detect_in_submissions(self, submissions: Dict[str, str]) -> List[Dict]:
        """
        Phát hiện đạo văn trong nhiều bài nộp
        
        Args:
            submissions: Dictionary {filename: code}
            
        Returns:
            Danh sách các cặp nghi ngờ
        """
        results = []
        filenames = list(submissions.keys())
        
        # So sánh từng cặp
        for i in range(len(filenames)):
            for j in range(i + 1, len(filenames)):
                file1 = filenames[i]
                file2 = filenames[j]
                
                comparison = self.compare_pair(
                    file1, submissions[file1],
                    file2, submissions[file2]
                )
                
                results.append(comparison)
        
        # Sắp xếp theo độ tương đồng giảm dần
        results.sort(key=lambda x: x['overall_similarity'], reverse=True)
        
        return results
    
    def detect_exact_matches(self, submissions: Dict[str, str]) -> List[Tuple]:
        """
        Phát hiện các bài nộp giống hệt nhau (sau khi chuẩn hóa)
        
        Args:
            submissions: Dictionary {filename: code}
            
        Returns:
            Danh sách các nhóm file giống nhau
        """
        hash_groups = defaultdict(list)
        
        for filename, code in submissions.items():
            code_hash = self.calculate_structure_hash(code)
            hash_groups[code_hash].append(filename)
        
        # Chỉ giữ các nhóm có > 1 file
        exact_matches = [
            files for files in hash_groups.values() 
            if len(files) > 1
        ]
        
        return exact_matches
    
    def generate_report(self, results: List[Dict], 
                       show_all: bool = False) -> str:
        """
        Tạo báo cáo phát hiện đạo văn
        
        Args:
            results: Kết quả từ detect_in_submissions()
            show_all: Hiện tất cả hoặc chỉ các trường hợp nghi ngờ
            
        Returns:
            Chuỗi báo cáo
        """
        report = []
        report.append("=" * 80)
        report.append("PLAGIARISM DETECTION REPORT")
        report.append("=" * 80)
        report.append(f"Threshold: {self.similarity_threshold:.1%}")
        report.append("")
        
        suspicious = [r for r in results if r['status'] == 'SUSPICIOUS']
        
        report.append(f"Total comparisons: {len(results)}")
        report.append(f"Suspicious pairs: {len(suspicious)}")
        report.append("")
        
        if show_all:
            display_results = results
        else:
            display_results = suspicious
        
        for i, result in enumerate(display_results, 1):
            report.append(f"Pair #{i}: {result['status']}")
            report.append(f"  File 1: {result['file1']}")
            report.append(f"  File 2: {result['file2']}")
            report.append(f"  Overall Similarity: {result['overall_similarity']:.1%}")
            report.append(f"    - Text Similarity: {result['text_similarity']:.1%}")
            report.append(f"    - AST Similarity: {result['ast_similarity']:.1%}")
            report.append(f"    - Fingerprint Similarity: {result['fingerprint_similarity']:.1%}")
            report.append("")
        
        return "\n".join(report)


### Thử nghiệm
##if __name__ == "__main__":
##    detector = PlagiarismDetector(similarity_threshold=0.8)
##    
##    # Đọc các bài nộp
##    submissions = {}
##    for i in range(1, 4):
##        filename = f"student_{i}.py"
##        try:
##            with open(filename, 'r', encoding='utf-8') as f:
##                submissions[filename] = f.read()
##        except:
##            print(f"Cannot read {filename}")
##    
##    # Phát hiện đạo văn
##    if submissions:
##        # Kiểm tra giống hệt
##        exact_matches = detector.detect_exact_matches(submissions)
##        if exact_matches:
##            print("EXACT MATCHES FOUND:")
##            for group in exact_matches:
##                print(f"  Group: {', '.join(group)}")
##            print()
##        
##        # Kiểm tra tương đồng
##        results = detector.detect_in_submissions(submissions)
##        print(detector.generate_report(results, show_all=False))
##
