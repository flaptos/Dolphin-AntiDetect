#!/usr/bin/env python3
"""
Tests для fingerprint модуля.
"""

import pytest
from unittest.mock import Mock, patch


class TestFingerprintManager:
    """Тесты для FingerprintManager."""
    
    @pytest.fixture
    def fingerprint_manager(self):
        """Создает FingerprintManager instance."""
        from src.fingerprint import FingerprintManager
        return FingerprintManager()
    
    @pytest.fixture
    def mock_profile(self):
        """Создает mock BrowserProfile."""
        profile = Mock()
        profile.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        profile.viewport = (1920, 1080)
        profile.device_pixel_ratio = 1.0
        profile.color_depth = 24
        profile.timezone = "America/New_York"
        profile.language = "en-US"
        profile.country = "US"
        profile.platform = "Win32"
        profile.vendor = "Google Inc."
        return profile
    
    def test_fingerprint_manager_initialization(self, fingerprint_manager):
        """Проверяет инициализацию FingerprintManager."""
        assert fingerprint_manager is not None
    
    def test_generate_canvas_fingerprint(self, fingerprint_manager, mock_profile):
        """Проверяет генерацию Canvas fingerprint."""
        with patch.object(fingerprint_manager, '_get_canvas_data') as mock_canvas:
            mock_canvas.return_value = b"test_canvas_data"
            
            result = fingerprint_manager.generate_canvas_fingerprint(
                mock_profile,
                width=1920,
                height=1080
            )
            
            assert result is not None
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_generate_webgl_fingerprint(self, fingerprint_manager, mock_profile):
        """Проверяет генерацию WebGL fingerprint."""
        with patch.object(fingerprint_manager, '_get_webgl_data') as mock_webgl:
            mock_webgl.return_value = vendor="test_vendor", renderer="test_renderer"
            
            result = fingerprint_manager.generate_webgl_fingerprint(mock_profile)
            
            assert result is not None
            assert isinstance(result, str)
    
    def test_generate_audio_fingerprint(self, fingerprint_manager, mock_profile):
        """Проверяет генерацию Audio fingerprint."""
        with patch.object(fingerprint_manager, '_get_audio_data') as mock_audio:
            mock_audio.return_value = b"test_audio_data"
            
            result = fingerprint_manager.generate_audio_fingerprint(mock_profile)
            
            assert result is not None
            assert isinstance(result, str)
    
    def test_generate_font_fingerprint(self, fingerprint_manager, mock_profile):
        """Проверяет генерацию Font fingerprint."""
        # Mock available fonts
        fonts = [
            "Arial",
            "Times New Roman",
            "Courier New",
            "Georgia",
            "Verdana",
        ]
        
        result = fingerprint_manager._get_font_fingerprint(mock_profile, fonts)
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_generate_full_fingerprint(self, fingerprint_manager, mock_profile):
        """Проверяет полную генерацию fingerprint."""
        with (
            patch.object(fingerprint_manager, 'generate_canvas_fingerprint') as mock_canvas,
            patch.object(fingerprint_manager, 'generate_webgl_fingerprint') as mock_webgl,
            patch.object(fingerprint_manager, 'generate_audio_fingerprint') as mock_audio,
        ):
            mock_canvas.return_value = "canvas_hash"
            mock_webgl.return_value = "webgl_hash"
            mock_audio.return_value = "audio_hash"
            
            result = fingerprint_manager.generate_full_fingerprint(mock_profile)
            
            assert result is not None
            assert "canvas" in result
            assert "webgl" in result
            assert "audio" in result
            assert "user_agent" in result
            assert "screen_resolution" in result
    
    def test_canvas_noise_generation(self, fingerprint_manager):
        """Проверяет генерацию noise для canvas."""
        noise = fingerprint_manager._generate_canvas_noise(width=1920, height=1080)
        
        assert noise is not None
        assert len(noise) > 0
    
    def test_webgl_vendor_overrides(self, fingerprint_manager):
        """Проверяет кастомные WebGL Overrides."""
        vendor = fingerprint_manager.get_webgl_vendor("Windows", "chrome")
        assert vendor is not None


class TestFingerprintComponents:
    """Тесты для компонентов fingerprint."""
    
    @pytest.fixture
    def fingerprint_manager(self):
        from src.fingerprint import FingerprintManager
        return FingerprintManager()
    
    def test_timezone_fingerprint(self, fingerprint_manager):
        """Проверяет timezone fingerprint."""
        result = fingerprint_manager._get_timezone_fingerprint("America/New_York")
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_language_fingerprint(self, fingerprint_manager):
        """Проверяет language fingerprint."""
        result = fingerprint_manager._get_language_fingerprint(["en-US", "en"])
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_device_pixel_ratio_fingerprint(self, fingerprint_manager):
        """Проверяет pixel ratio fingerprint."""
        result = fingerprint_manager._get_pixel_ratio_fingerprint(1.0)
        
        assert result is not None
    
    def test_color_depth_fingerprint(self, fingerprint_manager):
        """Проверяет color depth fingerprint."""
        result = fingerprint_manager._get_color_depth_fingerprint(24)
        
        assert result is not None


class TestFingerprintEdgeCases:
    """Тесты для edge cases fingerprint."""
    
    @pytest.fixture
    def fingerprint_manager(self):
        from src.fingerprint import FingerprintManager
        return FingerprintManager()
    
    def test_empty_profile(self, fingerprint_manager):
        """Проверяет empty profile."""
        profile = Mock()
        profile.user_agent = ""
        profile.viewport = (0, 0)
        profile.device_pixel_ratio = 0
        
        result = fingerprint_manager.generate_full_fingerprint(profile)
        
        assert result is not None
    
    def test_none_profile(self, fingerprint_manager):
        """Проверяет None profile."""
        with pytest.raises(Exception):
            fingerprint_manager.generate_full_fingerprint(None)
    
    def test_special_characters_in_fingerprint(self, fingerprint_manager, mock_profile):
        """Проверяет специальные символы в fingerprint."""
        mock_profile.user_agent = "Mozilla/5.0 (Test\nSpecial\rCharacters)"
        
        result = fingerprint_manager.generate_full_fingerprint(mock_profile)
        
        assert result is not None
        assert "user_agent" in result
