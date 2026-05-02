#!/usr/bin/env python3
"""
pytest configuration file.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


# Fixtures
import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_profile():
    """Create a mock BrowserProfile."""
    from src.models.data_models import BrowserProfile, OSType, BROWSER_TYPE_MAP
    
    return BrowserProfile(
        name="test_profile",
        browser=BROWSER_TYPE_MAP["chrome"],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        os=OSType.WINDOWS,
        viewport=(1920, 1080),
        device_pixel_ratio=1.0,
        color_depth=24,
        timezone="America/New_York",
        language="en-US",
        country="US",
        hardware_concurrency=8,
        cpu_cores=4,
        ram_in_gb=8,
        platform="Win32",
        vendor="Google Inc.",
    )


@pytest.fixture
def mock_detector():
    """Create a mock Detector."""
    mock = Mock()
    mock.detect.return_value = Mock(
        is_detected=False,
        score=10,
        risk_level="low",
        to_dict=lambda: {"is_detected": False, "score": 10}
    )
    return mock


@pytest.fixture
def mock_browser():
    """Create a mock AntiDetectBrowser."""
    mock = Mock()
    mock.is_running = True
    mock._driver = Mock()
    mock._started_at = None
    mock._request_id = "testRequestId"
    mock.profile = Mock()
    mock.profile.name = "test"
    mock.start = Mock()
    mock.close = Mock()
    mock.get_fingerprint = Mock(return_value={})
    mock.is_detected = Mock(return_value=False)
    return mock
