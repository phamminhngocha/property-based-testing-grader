"""
setup.py - Package setup configuration
Chức năng: Cấu hình để đóng gói và cài đặt project như một Python package
Cho phép cài đặt bằng: pip install .
"""

from setuptools import setup, find_packages
import os

# Đọc README.md để làm long description
def read_file(filename):
    """Đọc nội dung file"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# Đọc requirements
def read_requirements(filename):
    """Đọc danh sách dependencies từ requirements.txt"""
    requirements = []
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
    return requirements

setup(
    # Thông tin cơ bản về package
    name='python-auto-grader-pbt',
    version='1.0.0',
    author='Pham Minh Ngoc Ha',
    author_email='phammingngocha@hvtc.edu.vn',
    description='Automated grading system for Python assignments using Property-Based Testing',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/[username]/python-auto-grader-pbt',
    
    # Phân loại package
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Topic :: Education :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    
    # Keywords để tìm kiếm trên PyPI
    keywords='grading education testing property-based hypothesis python',
    
    # Tìm tất cả packages trong project
    packages=find_packages(exclude=['tests', 'docs', 'examples']),
    
    # Python version yêu cầu
    python_requires='>=3.8',
    
    # Dependencies
    install_requires=read_requirements('requirements.txt'),
    
    # Optional dependencies cho development
    extras_require={
        'dev': read_requirements('requirements-dev.txt'),
        'test': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
        ],
        'docs': [
            'sphinx>=7.2.0',
            'sphinx-rtd-theme>=2.0.0',
        ],
    },
    
    # Entry points - command line scripts
    entry_points={
        'console_scripts': [
            'pbt-grader=src.cli:main',  # Command: pbt-grader
        ],
    },
    
    # Include non-Python files
    include_package_data=True,
    
    # Thư mục data files
    package_data={
        'src': ['config/*.json', 'templates/*.html'],
    },
    
    # Zip safe
    zip_safe=False,
)
