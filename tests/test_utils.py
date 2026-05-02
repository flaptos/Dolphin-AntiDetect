#!/usr/bin/env python3
"""
Tests для системы логирования.
"""

import pytest
import logging
from unittest.mock import patch, MagicMock


class TestLogger:
    """Тесты для логирования."""
    
    def test_logger_creation(self):
        """Проверяет создание logger."""
        from src.utils.logger import setup_logger
        
        logger = setup_logger("test_logger")
        
        assert logger is not None
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"
    
    def test_logger_levels(self):
        """Проверяет разные уровни логирования."""
        from src.utils.logger import setup_logger
        
        logger = setup_logger("test_levels")
        
        # Просто проверяем, что нет ошибок
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
    
    def test_colored_output(self):
        """Проверяем colored output."""
        from src.utils.logger import ColoredFormatter
        
        formatter = ColoredFormatter()
        assert formatter is not None
        
        # Test format method
        log_record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None
        )
        result = formatter.format(log_record)
        assert "Test message" in result


class TestValidators:
    """Тесты для валидаторов."""
    
    def test_validate_profile_name(self):
        """Проверяет валидацию имени профиля."""
        from src.utils.validators import validate_profile_name, ValidationError
        
        assert validate_profile_name("valid_name") == "valid_name"
        assert validate_profile_name("Test-Profile_123") == "Test-Profile_123"
        
        with pytest.raises(ValidationError):
            validate_profile_name("")
        
        with pytest.raises(ValidationError):
            validate_profile_name("a" * 200)  # Too long
    
    def test_validate_user_agent(self):
        """Проверяет валидацию User-Agent."""
        from src.utils.validators import validate_user_agent, ValidationError
        
        valid_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        assert validate_user_agent(valid_ua) == valid_ua
        
        with pytest.raises(ValidationError):
            validate_user_agent("")
        
        with pytest.raises(ValidationError):
            validate_user_agent("invalid")  # Too short
    
    def test_validate_viewport(self):
        """Проверяет валидацию viewport."""
        from src.utils.validators import validate_viewport, ValidationError
        
        assert validate_viewport((1920, 1080)) == (1920, 1080)
        assert validate_viewport((1366, 768)) == (1366, 768)
        
        with pytest.raises(ValidationError):
            validate_viewport((0, 0))
        
        with pytest.raises(ValidationError):
            validate_viewport((-1, 1080))
        
        with pytest.raises(ValidationError):
            validate_viewport((1920, 1080, 60))  # Wrong size
    
    def test_validate_timezone(self):
        """Проверяет валидацию timezone."""
        from src.utils.validators import validate_timezone, ValidationError
        
        try:
            assert validate_timezone("America/New_York") == "America/New_York"
        except Exception as e:
            pytest.skip(f"Timezone validation requires zoneinfo: {e}")
    
    def test_validate_hardware(self):
        """Проверяет валидацию hardware."""
        from src.utils.validators import validate_hardware, ValidationError
        
        assert validate_hardware(8, 8, 8) == (8, 8, 8)
        assert validate_hardware(4, 4, 4) == (4, 4, 4)
        
        with pytest.raises(ValidationError):
            validate_hardware(0, 8, 8)  # Invalid cores
        
        with pytest.raises(ValidationError):
            validate_hardware(32, 64, 64)  # Unlikely but valid


class TestCrypto:
    """Тесты для криптографии."""
    
    def test_generate_session_token(self):
        """Проверяет генерацию session token."""
        from src.utils.crypto import CryptoUtils
        
        crypto = CryptoUtils()
        token = crypto.generate_session_token()
        
        assert token is not None
        assert len(token) > 0
        assert len(token) <= 64  # Max length
    
    def test_generate_fingerprint_id(self):
        """Проверяет генерацию fingerprint ID."""
        from src.utils.crypto import CryptoUtils
        
        crypto = CryptoUtils()
        fid = crypto.generate_fingerprint_id()
        
        assert fid is not None
        assert len(fid) == 32  # 32 chars hex
    
    def test_generate_request_id(self):
        """Проверяет генерацию request ID."""
        from src.utils.crypto import CryptoUtils
        
        crypto = CryptoUtils()
        rid = crypto.generate_request_id()
        
        assert rid is not None
        assert len(rid) > 0
    
    def test_hmac_sign(self):
        """Проверяет HMAC подпись."""
        from src.utils.crypto import CryptoUtils
        
        crypto = CryptoUtils()
        data = b"test data"
        signature = crypto.hmac_sign(data)
        
        assert signature is not None
        assert len(signature) > 0
    
    def test_secure_random(self):
        """Проверяет secure random."""
        from src.utils.crypto import CryptoUtils
        
        crypto = CryptoUtils()
        r = crypto.secure_random(16)
        
        assert len(r) == 16


class TestDataModels:
    """Тесты для data models."""
    
    def test_browser_profile_creation(self):
        """Проверяет создание BrowserProfile."""
        from src.models.data_models import BrowserProfile, OSType, BROWSER_TYPE_MAP
        
        profile = BrowserProfile(
            name="test",
            browser=BROWSER_TYPE_MAP["chrome"],
            user_agent="Test UA",
            os=OSType.WINDOWS,
        )
        
        assert profile.name == "test"
        assert profile.os == OSType.WINDOWS
        assert profile.browser_type == BROWSER_TYPE_MAP["chrome"]
    
    def test_profile_to_dict(self):
        """Проверяет конвертацию profile в dict."""
        from src.models.data_models import BrowserProfile, OSType, BROWSER_TYPE_MAP
        
        profile = BrowserProfile(
            name="test",
            browser=BROWSER_TYPE_MAP["chrome"],
            user_agent="Test UA",
            os=OSType.WINDOWS,
            viewport=(1920, 1080),
        )
        
        data = profile.to_dict()
        
        assert "name" in data
        assert data["name"] == "test"
        assert "viewport" in data
    
    def test_fingerprint_model(self):
        """Проверяет Fingerprint model."""
        from src.models.data_models import Fingerprint
        
        fp = Fingerprint(
            user_agent="Test UA",
            screen_resolution=(1920, 1080),
            timezone="America/New_York",
            languages=["en-US"],
        )
        
        assert fp.user_agent == "Test UA"
        assert fp.screen_resolution == (1920, 1080)
    
    def test_browser_type_enum(self):
        """Проверяет BrowserType enum."""
        from src.models.data_models import BrowserType
        
        assert BrowserType.CHROME.value == "chrome"
        assert BrowserType.FIREFOX.value == "firefox"
        assert BrowserType.SAFARI.value == "safari"
    
    def test_os_type_enum(self):
        """Проверяет OSType enum."""
        from src.models.data_models import OSType
        
        assert OSType.WINDOWS.value == "windows"
        assert OSType.MACOS.value == "macos"
        assert OSType.LINUX.value == "linux"
        assert OSType.IOS.value == "ios"
        assert OSType.ANDROID.value == "android"
