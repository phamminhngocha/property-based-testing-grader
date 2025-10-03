# MANIFEST.in - Manifest file configuration
# Chức năng: Chỉ định các file non-Python cần được include khi đóng gói
# Được sử dụng bởi setuptools khi build distribution

# Include documentation files
include README.md
include LICENSE
include CHANGELOG.md
include CONTRIBUTING.md

# Include requirements files
include requirements.txt
include requirements-dev.txt
include requirements-prod.txt

# Include configuration files
recursive-include src/config *.json *.yaml *.yml

# Include templates
recursive-include src/templates *.html *.txt

# Include examples
recursive-include examples *.py *.md

# Include tests
recursive-include tests *.py

# Exclude compiled Python files
global-exclude *.pyc
global-exclude __pycache__
global-exclude *.pyo
global-exclude *.pyd
global-exclude .DS_Store

# Exclude development files
exclude .gitignore
exclude .gitattributes
exclude pytest.ini
exclude .coveragerc
