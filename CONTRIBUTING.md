# Contributing to Dolphin-AntiDetect

Thank you for your interest in contributing to Dolphin-AntiDetect! This document provides guidelines and instructions for contributing.

## 🌟 How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected vs actual behavior**
- **Environment details** (Python version, OS, browser version)
- **Stack traces** if applicable
- **Minimal code examples** if applicable

Example bug report template:
```markdown
## Bug Description
[Description]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior
[Description]

##Actual Behavior
[Description]

## Environment
- Python: 3.11.x
- Browser: Chrome 120.0.0.0
- OS: Ubuntu 22.04
```

### Suggesting Features

Feature suggestions are welcome! Please include:

- **Use case** - Why is this feature needed?
- **Proposed solution** - How should it work?
- **Alternatives considered** - Other approaches
- **Additional context** - Screenshots, examples

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the code style
3. **Add tests** for new functionality
4. **Update documentation** if needed
5. **Ensure CI passes** (tests, linting, type checking)
6. **Write clear commit messages**
7. **Create pull request**

## 📐 Code Style

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Indentation**: 4 spaces (no tabs)
- **Line length**: 120 characters maximum
- **Imports**: Grouped and sorted (standard, third-party, local)
- **Naming**: 
  - Variables/functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`
  - Private: `_leading_underscore`

### Example Code

```python
#!/usr/bin/env python3
"""Module docstring."""

from typing import Optional, Dict, Any
import logging


class BrowserProfile:
    """Browser profile management."""
    
    def __init__(self, name: str, os_type: str):
        """Initialize profile.
        
        Args:
            name: Profile name
            os_type: Operating system type
        """
        self.name = name
        self.os_type = os_type
        self._logger = logging.getLogger(__name__)
    
    def get_info(self) -> Dict[str, Any]:
        """Get profile information."""
        return {
            "name": self.name,
            "os": self.os_type,
        }
```

### Type Hints

**Required for all functions:**
```python
def process_data(
    data: Dict[str, Any],
    options: Optional[Dict] = None
) -> Dict[str, Any]:
    """Process the data."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def calculate_fingerprint(profile: BrowserProfile) -> str:
    """Generate fingerprint for profile.
    
    Args:
        profile: BrowserProfile instance
        
    Returns:
        Hex string fingerprint
        
    Raises:
        ValueError: If profile is invalid
        
    Example:
        >>> fp = calculate_fingerprint(profile)
        >>> len(fp)
        64
    """
```

## 🧪 Testing

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_profiler.py -v

# With coverage
pytest tests/ --cov=src --cov-report=term-missing

# Specific test
pytest tests/test_utils.py::TestValidators::test_validate_profile_name -v
```

### Writing Tests

**Structure:**
```python
import pytest
from src.profiler import BrowserProfiler


class TestBrowserProfiler:
    """Profiler tests."""
    
    def test_profile_creation(self):
        """Test profile creation."""
        profiler = BrowserProfiler()
        profile = profiler.create_profile(name="test")
        
        assert profile is not None
        assert profile.name == "test"
    
    @pytest.mark.slow
    def test_batch_profile_creation(self):
        """Test batch creation (slow)."""
        pass
```

**Best Practices:**
- Test one thing per test function
- Use descriptive test names
- Include edge cases
- Use fixtures for setup/teardown
- Mock external dependencies

### Test Coverage

Aim for **80%+ coverage**:
```bash
# Check coverage
pytest tests/ --cov=src --cov-report=html

# View in browser
open htmlcov/index.html
```

## 📝 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

**Examples:**
```bash
feat(browser): add stealth script injection

Injected 6 anti-detect scripts for browser automation.
- webdriver property override
- plugins length check
- chrome object check

Closes #123
```

```bash
fix(profiler): correct hardware weighting for macos

Adjusted RAM and CPU core defaults for macOS profiles.
- RAM: 8GB → 16GB (default macOS)
- CPU cores: 4 → 8 (default macOS)
```

### Git Hooks

Set up pre-commit hooks:
```bash
pip install pre-commit
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## 🔄 Pull Request Process

### PR Template

```markdown
## Description
[What does this PR do?]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Coverage maintained

## Checklist
- [ ] Code follows style guidelines
- [ ] Docstrings added
- [ ] Self-review completed
- [ ] No new warnings
```

### Review Process

1. **Automated checks** - CI must pass
2. **Code review** - At least 1 approver
3. **Tests** - All tests must pass
4. **Documentation** - Updated if needed
5. **Merge** - Squash and merge to main

## 🎯 Areas for Contribution

### High Priority
1. **Browser support** - Firefox, Safari
2. **Playwright integration**
3. **Headless detection** improvements
4. **Machine learning** for anti-detection
5. **API server** mode

### Medium Priority
1. **GUI interface**
2. **Cloud deployment** templates
3. **Real-time** fingerprint analysis
4. **Multi-browser** sessions
5. **Performance** optimizations

### Low Priority
1. **Documentation** improvements
2. **Examples** and tutorials
3. **Internationalization**
4. **Theme** customization
5. **UI** enhancements

## 📋 Coding Standards Checklist

Before submitting PR:
- [ ] Code follows PEP 8
- [ ] Type hints for all functions
- [ ] Docstrings for all public functions
- [ ] Tests for new functionality
- [ ] No linting errors
- [ ] No type checking errors
- [ ] Updated documentation
- [ ] Clear commit messages
- [ ] Tested manually
- [ ] No debug code

## 🐛 Debugging Tips

### Common Issues

**ChromeDriver issues:**
```bash
# Update ChromeDriver
webdriver-manager

# Or manually
chromedriver --version
```

**Import errors:**
```bash
# Install package in editable mode
pip install -e .

# Or add to path
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
```

**Test failures:**
```bash
# Run with verbose output
pytest -v -s

# Run specific test
pytest tests/test_file.py::test_function -v -s
```

## 🤝 Getting Help

- **Documentation**: See [README.md](README.md)
- **Issues**: https://github.com/flaptos/Dolphin-AntiDetect/issues
- **Discussions**: https://github.com/flaptos/Dolphin-AntiDetect/discussions
- **Email**: flaptos@github.com

## 📜 Code of Conduct

Be respectful and inclusive:
- Use welcoming and inclusive language
- Be respectful of different viewpoints
- Gracefully accept constructive criticism
- Focus on what's best for the community

## 🎓 Learning Resources

- [Selenium Documentation](https://selenium.dev/documentation/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2/)

---

Thank you for contributing to Dolphin-AntiDetect! 🐬
