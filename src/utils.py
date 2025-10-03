"""
Utility Functions - Các hàm tiện ích chung
"""

import os
import sys
import subprocess
import tempfile
import shutil
from typing import Dict, Any, Optional
import json


def safe_import_module(file_path: str, module_name: str = "student_module"):
    """
    Import module một cách an toàn
    
    Args:
        file_path: Đường dẫn đến file Python
        module_name: Tên module
        
    Returns:
        Module object hoặc None nếu thất bại
    """
    import importlib.util
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error importing {file_path}: {e}")
        return None


def check_syntax(file_path: str) -> Dict[str, Any]:
    """
    Kiểm tra cú pháp Python
    
    Args:
        file_path: Đường dẫn đến file
        
    Returns:
        Dictionary chứa kết quả kiểm tra
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        compile(code, file_path, 'exec')
        
        return {
            'valid': True,
            'error': None
        }
    except SyntaxError as e:
        return {
            'valid': False,
            'error': str(e),
            'line': e.lineno,
            'offset': e.offset
        }
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }


def run_python_file(file_path: str, input_data: str = "", 
                   timeout: int = 5) -> Dict[str, Any]:
    """
    Chạy file Python với input
    
    Args:
        file_path: Đường dẫn đến file
        input_data: Dữ liệu đầu vào
        timeout: Thời gian timeout (giây)
        
    Returns:
        Dictionary chứa kết quả
    """
    try:
        result = subprocess.run(
            [sys.executable, file_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Timeout',
            'stdout': '',
            'stderr': 'Process exceeded timeout limit'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'stdout': '',
            'stderr': str(e)
        }


def create_sandbox_environment():
    """
    Tạo môi trường sandbox để chạy code an toàn
    
    Returns:
        Đường dẫn đến thư mục sandbox
    """
    sandbox_dir = tempfile.mkdtemp(prefix="grader_sandbox_")
    return sandbox_dir


def cleanup_sandbox(sandbox_dir: str):
    """
    Dọn dẹp môi trường sandbox
    
    Args:
        sandbox_dir: Đường dẫn thư mục sandbox
    """
    try:
        shutil.rmtree(sandbox_dir)
    except Exception as e:
        print(f"Error cleaning up sandbox: {e}")


def format_time(seconds: float) -> str:
    """
    Format thời gian theo dạng dễ đọc
    
    Args:
        seconds: Số giây
        
    Returns:
        Chuỗi thời gian đã format
    """
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f}μs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        remaining = seconds % 60
        return f"{minutes}m {remaining:.2f}s"


def format_bytes(bytes_size: int) -> str:
    """
    Format kích thước bytes theo dạng dễ đọc
    
    Args:
        bytes_size: Kích thước bytes
        
    Returns:
        Chuỗi kích thước đã format
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def load_config(config_file: str) -> Optional[Dict]:
    """
    Load cấu hình từ file JSON
    
    Args:
        config_file: Đường dẫn file config
        
    Returns:
        Dictionary config hoặc None
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None


def save_config(config: Dict, config_file: str):
    """
    Lưu cấu hình ra file JSON
    
    Args:
        config: Dictionary config
        config_file: Đường dẫn file output
    """
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving config: {e}")


def colorize_output(text: str, color: str) -> str:
    """
    Thêm màu cho text output (terminal)
    
    Args:
        text: Text cần tô màu
        color: Màu ('red', 'green', 'yellow', 'blue')
        
    Returns:
        Text đã có mã màu
    """
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'reset': '\033[0m'
    }
    
    color_code = colors.get(color, colors['reset'])
    return f"{color_code}{text}{colors['reset']}"


def print_progress_bar(iteration: int, total: int, prefix: str = '',
                      suffix: str = '', length: int = 50):
    """
    In progress bar
    
    Args:
        iteration: Iteration hiện tại
        total: Tổng số iteration
        prefix: Prefix string
        suffix: Suffix string
        length: Độ dài progress bar
    """
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='')
    
    if iteration == total:
        print()


# Constants
DEFAULT_TIMEOUT = 30
MAX_FILE_SIZE = 1024 * 1024  # 1MB
ALLOWED_EXTENSIONS = ['.py']
