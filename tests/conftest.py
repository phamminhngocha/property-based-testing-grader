"""
tests/conftest.py - Pytest configuration and shared fixtures
Chức năng: Định nghĩa fixtures dùng chung cho tất cả tests
Pytest tự động load file này
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path

# ============================================================================
# Directory Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def fixtures_dir():
    """
    Fixture: Path to fixtures directory.
    Scope: session (created once per test session)
    """
    return Path(__file__).parent / "fixtures"

@pytest.fixture
def temp_dir():
    """
    Fixture: Temporary directory for test files.
    Scope: function (created for each test)
    Automatically cleaned up after test.
    """
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

# ============================================================================
# File Fixtures
# ============================================================================

@pytest.fixture
def sample_student_code(temp_dir):
    """
    Fixture: Create a sample student code file.
    Returns path to file.
    """
    code = '''
def add(a, b):
    """Add two numbers."""
    return a + b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def sort_list(lst):
    """Sort a list."""
    return sorted(lst)
'''
    
    filepath = os.path.join(temp_dir, "student_code.py")
    with open(filepath, 'w') as f:
        f.write(code)
    
    return filepath

@pytest.fixture
def sample_buggy_code(temp_dir):
    """
    Fixture: Create a buggy student code file.
    """
    code = '''
def add(a, b):
    """Add two numbers - but has a bug."""
    return a - b  # BUG: Should be a + b

def divide(a, b):
    """Divide without checking zero."""
    return a / b  # BUG: No zero check
'''
    
    filepath = os.path.join(temp_dir, "buggy_code.py")
    with open(filepath, 'w') as f:
        f.write(code)
    
    return filepath

@pytest.fixture
def sample_io_program(temp_dir):
    """
    Fixture: Create a sample IO program.
    """
    code = '''
# Simple addition program
a = int(input())
b = int(input())
print(a + b)
'''
    
    filepath = os.path.join(temp_dir, "io_program.py")
    with open(filepath, 'w') as f:
        f.write(code)
    
    return filepath

@pytest.fixture
def sample_complex_code(temp_dir):
    """
    Fixture: Create complex code for AST analysis.
    """
    code = '''
"""Module with complex code for testing."""

class Calculator:
    """A simple calculator class."""
    
    def __init__(self):
        """Initialize calculator."""
        self.result = 0
    
    def add(self, x, y):
        """Add two numbers."""
        if x is None or y is None:
            raise ValueError("Arguments cannot be None")
        self.result = x + y
        return self.result
    
    def complex_function(self, a, b, c):
        """Function with high complexity."""
        if a > 0:
            if b > 0:
                if c > 0:
                    return a + b + c
                else:
                    return a + b
            else:
                return a
        else:
            return 0

def helper_function(x):
    """Helper function."""
    return x * 2
'''
    
    filepath = os.path.join(temp_dir, "complex_code.py")
    with open(filepath, 'w') as f:
        f.write(code)
    
    return filepath

# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def basic_test_cases():
    """
    Fixture: Basic test cases for grading.
    """
    return [
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
        },
        {
            'function': 'multiply',
            'inputs': [3, 4],
            'expected': 12
        }
    ]

@pytest.fixture
def io_test_cases():
    """
    Fixture: IO test cases.
    """
    return [
        {
            'input': '5\n3\n',
            'expected': '8\n'
        },
        {
            'input': '10\n-2\n',
            'expected': '8\n'
        },
        {
            'input': '0\n0\n',
            'expected': '0\n'
        }
    ]

@pytest.fixture
def structure_requirements():
    """
    Fixture: Structure requirements for AST grading.
    """
    return {
        'functions': 2,
        'classes': 0,
        'loops': 0
    }

# ============================================================================
# Mock Fixtures
# ============================================================================

@pytest.fixture
def mock_reference_function():
    """
    Fixture: Mock reference function for testing.
    """
    def reference_sort(lst):
        return sorted(lst)
    
    return reference_sort

@pytest.fixture
def mock_performance_test_inputs():
    """
    Fixture: Mock test inputs for performance testing.
    """
    return [
        ([list(range(10))],),
        ([list(range(50))],),
        ([list(range(100))],),
    ]

# ============================================================================
# Configuration Fixtures
# ============================================================================

@pytest.fixture
def default_grader_config():
    """
    Fixture: Default grader configuration.
    """
    return {
        'weights': {
            'functionality': 0.40,
            'code_quality': 0.20,
            'performance': 0.20,
            'documentation': 0.10,
            'style': 0.10
        },
        'enable_pbt': True,
        'enable_performance': True,
        'enable_ast_analysis': True,
        'max_complexity': 10,
        'timeout': 30
    }

# ============================================================================
# Cleanup Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_after_test():
    """
    Fixture: Automatic cleanup after each test.
    autouse=True means it runs for every test automatically.
    """
    # Setup (before test)
    yield
    
    # Teardown (after test)
    import gc
    gc.collect()

# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    """
    Pytest hook: Configure test session.
    Register custom markers.
    """
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )

def pytest_collection_modifyitems(config, items):
    """
    Pytest hook: Modify collected test items.
    Add markers to tests based on patterns.
    """
    for item in items:
        # Auto-mark integration tests
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Auto-mark unit tests
        if "test_" in item.nodeid and "integration" not in item.nodeid:
            item.add_marker(pytest.mark.unit)
