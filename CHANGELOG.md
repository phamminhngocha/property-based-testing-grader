# Changelog

<!--
CHANGELOG.md - Project changelog
Chức năng: Ghi lại lịch sử các thay đổi, cập nhật của project
Tuân thủ chuẩn Keep a Changelog (https://keepachangelog.com/)
Format: Markdown
-->

Tất cả các thay đổi đáng chú ý của project sẽ được ghi lại trong file này.

Format dựa trên [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
và project tuân thủ [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Planned
- Integration with Learning Management Systems (LMS)
- Web-based dashboard for batch grading
- Support for Jupyter notebook grading
- AI-powered feedback generation

## [1.0.0] - 2025-10-03

### Added
- **BasicGrader**: Unit test-based grading system
- **IOGrader**: Input/Output comparison grading
- **WeightedGrader**: Weighted test group grading
- **ASTGrader**: Code quality analysis using AST
  - Cyclomatic complexity checking
  - Code structure validation
  - Naming convention checking (PEP 8)
  - Documentation coverage analysis
- **PropertyBasedGrader**: Property-based testing with Hypothesis
  - Commutativity testing
  - Associativity testing
  - Identity element testing
  - Monotonicity testing
  - Idempotence testing
  - Oracle-based testing
  - Custom invariant checking
- **PlagiarismDetector**: Code similarity detection
  - Text-based similarity
  - AST-based similarity
  - Fingerprint-based detection
  - Exact match detection
- **PerformanceGrader**: Performance evaluation
  - Execution time measurement
  - Memory usage profiling
  - Comparison with reference implementation
- **AdvancedGrader**: Integrated comprehensive grading
  - Multi-method grading
  - Weighted scoring
  - Detailed reporting
  - JSON/HTML export
- **BatchGrader**: Batch processing for multiple submissions
  - Directory-based grading
  - Plagiarism detection across submissions
  - Statistical analysis
  - CSV export
- Utility functions for safe code execution
- Comprehensive test suite
- Documentation and examples

### Changed
- N/A (Initial release)

### Deprecated
- N/A (Initial release)

### Removed
- N/A (Initial release)

### Fixed
- N/A (Initial release)

### Security
- Sandboxed code execution environment
- Timeout protection against infinite loops
- Resource usage limits

## [0.1.0] - 2025-09-15

### Added
- Initial project structure
- Basic proof of concept
- Core grading algorithms research

---

## Version History Format

### Version Number: [MAJOR.MINOR.PATCH]
- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality additions
- **PATCH**: Backward-compatible bug fixes

### Change Categories:
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes
