"""
tests/__init__.py - Test package initialization
Chức năng: Khởi tạo test package, định nghĩa test utilities chung
"""

import os
import sys

# Add src to path for imports
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

# Test constants
FIXTURES_DIR = os.path.join(TEST_DIR, 'fixtures')
TIMEOUT = 30  # Default timeout for tests

# Test helper functions
def get_fixture_path(filename):
    """
    Get full path to a fixture file.
    
    Args:
        filename: Name of fixture file
        
    Returns:
        Full path to fixture
    """
    return os.path.join(FIXTURES_DIR, filename)

def create_temp_file(content, suffix='.py'):
    """
    Create a temporary file with given content.
    
    Args:
        content: File content
        suffix: File suffix
        
    Returns:
        Path to temporary file
    """
    import tempfile
    
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, 'w') as f:
        f.write(content)
    
    return path

def cleanup_temp_file(path):
    """
    Remove temporary file.
    
    Args:
        path: Path to file
    """
    try:
        os.remove(path)
    except:
        pass
