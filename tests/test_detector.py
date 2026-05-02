#!/usr/bin/env python3
"""
Tests для detector модуля.
"""

import pytest
from typing import Dict, Any


class TestDetector:
    """Тесты для Detector."""
    
    @pytest.fixture
    def detector(self):
        """Создает Detector instance."""
        from src.detector import Detector
        return Detector()
    
    @pytest.fixture
    def sample_fingerprint(self) -> Dict[str, Any]:
        """Возвращает sample fingerprint для тестов."""
        return {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "screen_resolution": (1920, 1080),
            "window_inner_size": (1920, 1014),
            "window_outer_size": (1920, 1080),
            "timezone": "America/New_York",
            "languages": ["en-US", "en"],
            "color_depth": 24,
            "pixel_ratio": 1.0,
            "hardware_concurrency": 8,
            "logical_cores": 4,
            "ram": 8192,
            "device_memory": 8,
            "platform": "Win32",
            "vendor": "Google Inc.",
            "browser_platform": "Win32",
            "vendor_brand": "Google",
            "video_adapters": ["NVIDIA Corporation", "Intel Corporation"],
            "do_not_track": "1",
            "language": "en-US",
        }
    
    def test_detector_initialization(self, detector):
        """Проверяет инициализацию Detector."""
        assert detector is not None
    
    def test_detect_bot_not_detected(self, detector, sample_fingerprint):
        """Проверяет детекцию когда не бот."""
        # Убираем webdriver property
        clean_fingerprint = {k: v for k, v in sample_fingerprint.items() if k != "webdriver"}
        
        report = detector.detect(clean_fingerprint)
        
        assert report is not None
        assert report.is_detected is False
    
    def test_detect_webdriver_flag(self, detector, sample_fingerprint):
        """Проверяет детекцию webdriver flag."""
        # Добавляем webdriver flag
        fingerprint_with_webdriver = sample_fingerprint.copy()
        fingerprint_with_webdriver["webdriver"] = True
        
        report = detector.detect(fingerprint_with_webdriver)
        
        assert report is not None
        # Должно обнаружить webdriver
        assert report.score > 0
    
    def test_detection_scoring(self, detector, sample_fingerprint):
        """Проверяет систему скоринга."""
        report = detector.detect(sample_fingerprint)
        
        assert report.score >= 0
        assert report.risk_level is not None
    
    def test_risk_levels(self, detector, sample_fingerprint):
        """Проверяет уровни риска."""
        report = detector.detect(sample_fingerprint)
        
        assert report.risk_level in ["low", "medium", "high", "critical"]
    
    def test_detection_patterns(self, detector, sample_fingerprint):
        """Проверяет паттерны детекции."""
        report = detector.detect(sample_fingerprint)
        
        if report.patterns:
            for pattern in report.patterns:
                assert "name" in pattern
                assert "score" in pattern
                assert "description" in pattern
    
    def test_detection_report_json(self, detector, sample_fingerprint):
        """Проверяет JSON отчет."""
        report = detector.detect(sample_fingerprint)
        
        report_dict = report.to_dict()
        
        assert isinstance(report_dict, dict)
        assert "is_detected" in report_dict
        assert "risk_level" in report_dict
        assert "score" in report_dict
    
    def test_detection_multiple_sequential(self, detector, sample_fingerprint):
        """Проверяет несколько последовательных детекций."""
        # Несколько детекций
        for i in range(3):
            report = detector.detect(sample_fingerprint)
            assert report is not None


class TestDetectionRules:
    """Тесты для правил детекции."""
    
    @pytest.fixture
    def detector(self):
        from src.detector import Detector
        return Detector()
    
    def test_canvass_detection(self, detector):
        """Проверяет Canvas детекцию."""
        fingerprint = {
            "canvas_fingerprint": None,  # No canvas fingerprint
        }
        report = detector.detect(fingerprint)
        assert report is not None
    
    def test_webgl_detection(self, detector):
        """Проверяет WebGL детекцию."""
        fingerprint = {
            "webgl_fingerprint": None,  # No WebGL fingerprint
        }
        report = detector.detect(fingerprint)
        assert report is not None
    
    def test_audio_detection(self, detector):
        """Проверяет AudioContext детекцию."""
        fingerprint = {
            "audio_fingerprint": None,  # No audio fingerprint
        }
        report = detector.detect(fingerprint)
        assert report is not None
    
    def test_font_detection(self, detector):
        """Проверяет Font детекцию."""
        fingerprint = {
            "font_fingerprints": [],  # No fonts
        }
        report = detector.detect(fingerprint)
        assert report is not None
    
    def test_plugins_detection(self, detector):
        """Проверяет Plugins детекцию."""
        fingerprint = {
            "plugins": [],  # Empty plugins
        }
        report = detector.detect(fingerprint)
        assert report is not None
    
    def test_timezone_detection(self, detector):
        """Проверяет Timezone детекцию."""
        # Test missing timezone
        fingerprint = {}
        report = detector.detect(fingerprint)
        assert report is not None


class TestDetectionEdgeCases:
    """Тесты для edge cases."""
    
    @pytest.fixture
    def detector(self):
        from src.detector import Detector
        return Detector()
    
    def test_empty_fingerprint(self, detector):
        """Проверяет обработку пустого fingerprint."""
        report = detector.detect({})
        
        assert report is not None
    
    def test_none_values(self, detector):
        """Проверяет обработку None значений."""
        fingerprint = {
            "user_agent": None,
            "screen_resolution": None,
        }
        report = detector.detect(fingerprint)
        
        assert report is not None
    
    def test_malformed_values(self, detector):
        """Проверяет обработку malformed значений."""
        fingerprint = {
            "screen_resolution": "not_a_tuple",
            "timezone": 12345,
        }
        report = detector.detect(fingerprint)
        
        assert report is not None
    
    def test_very_large_values(self, detector):
        """Проверяет обработку очень больших значений."""
        fingerprint = {
            "screen_resolution": (99999, 99999),
            "ram": 999999999,
        }
        report = detector.detect(fingerprint)
        
        assert report is not None
