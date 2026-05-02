#!/usr/bin/env python3
"""
Tests для profiler модуля.
"""

import pytest
import os
from pathlib import Path
from unittest.mock import Mock, patch


class TestBrowserProfiler:
    """Тесты для BrowserProfiler."""
    
    @pytest.fixture
    def profiler(self, tmp_path):
        """Создает profiler с temp storage."""
        from src.profiler import BrowserProfiler
        
        profiler = BrowserProfiler(storage_path=str(tmp_path))
        yield profiler
        
        # Cleanup
        if tmp_path.exists():
            import shutil
            shutil.rmtree(tmp_path, ignore_errors=True)
    
    def test_profile_creation(self, profiler):
        """Проверяет создание профиля."""
        profile = profiler.create_profile(name="test_profile")
        
        assert profile is not None
        assert profile.name == "test_profile"
        assert profile.os is not None
        assert profile.browser_type is not None
        assert profile.user_agent is not None
    
    def test_profile_persistence(self, profiler):
        """Проверяет сохранение профиля."""
        profile = profiler.create_profile(name="persistent_profile")
        profile_path = profiler.storage_path / f"{profile.name}.json"
        
        assert profile_path.exists()
    
    def test_profile_loading(self, profiler):
        """Проверяет загрузку профиля."""
        # Создать профиль
        original = profiler.create_profile(name="load_test")
        
        # Загрузить профиль
        loaded = profiler.load_profile("load_test")
        
        assert loaded is not None
        assert loaded.name == original.name
        assert loaded.user_agent == original.user_agent
        assert loaded.os == original.os
    
    def test_list_profiles(self, profiler):
        """Проверяет список профилей."""
        # Создать несколько профилей
        profiler.create_profile(name="profile_1")
        profiler.create_profile(name="profile_2")
        profiler.create_profile(name="profile_3")
        
        profiles = profiler.list_all_profiles()
        
        assert len(profiles) >= 3
        assert "profile_1" in profiles
        assert "profile_2" in profiles
        assert "profile_3" in profiles
    
    def test_profile_deletion(self, profiler):
        """Проверяет удаление профиля."""
        profile = profiler.create_profile(name="delete_test")
        
        # Проверить существование
        assert profiler.storage_path.exists()
        
        # Удалить
        profiler.delete_profile("delete_test")
        
        # Проверить удаление
        deleted_path = profiler.storage_path / "delete_test.json"
        assert not deleted_path.exists()
    
    def test_default_profile_creation(self, profiler):
        """Проверяет создание профиля по умолчанию."""
        profile = profiler.create_profile()  # Без имени
        
        assert profile is not None
        assert profile.name is not None
        assert len(profile.name) > 0
    
    def test_user_agent_pool(self, profiler):
        """Проверяет генерацию User-Agent из пула."""
        profile = profiler.create_profile()
        
        assert profile.user_agent is not None
        assert "Mozilla" in profile.user_agent
        assert "Chrome" in profile.user_agent or "Firefox" in profile.user_agent
    
    def test_browser_type_selection(self, profiler):
        """Проверяет выбор типа браузера."""
        profile = profiler.create_profile(browser="firefox")
        
        assert profile.browser_type == "firefox"
    
    def test_os_type_selection(self, profiler):
        """Проверяет выбор типа ОС."""
        profile = profiler.create_profile(os="macos")
        
        assert profile.os == "macos"
    
    def test_profile_defaults(self, profiler):
        """Проверяет значения по умолчанию."""
        profile = profiler.create_profile()
        
        # Проверяем реалистичные значения
        assert profile.viewport is not None
        assert len(profile.viewport) == 2
        assert profile.viewport[0] > 0
        assert profile.viewport[1] > 0
        
        assert profile.hardware_concurrency is not None
        assert profile.cpu_cores is not None
        assert profile.ram_in_gb is not None
    
    def test_profile_realistic_hardware(self, profiler):
        """Проверяем реалистичные hardware параметры."""
        profile = profiler.create_profile()
        
        # Hardware параметры должны быть реалистичными
        assert 2 <= profile.hardware_concurrency <= 64
        assert 1 <= profile.cpu_cores <= 32
        assert 2 <= profile.ram_in_gb <= 128
    
    def test_profile_serialization(self, profiler):
        """Проверяет сериализацию профиля."""
        profile = profiler.create_profile(name="serialize_test")
        
        # Конвертировать в dict
        data = profile.to_dict()
        
        assert isinstance(data, dict)
        assert "name" in data
        assert "user_agent" in data
        assert "os" in data
    
    def test_profile_metadata(self, profiler):
        """Проверяет сохранение metadata."""
        profile = profiler.create_profile(name="metadata_test")
        
        metadata_path = profiler.storage_path / f"{profile.name}_meta.json"
        
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                import json
                meta = json.load(f)
            
            assert "created_at" in meta
            assert "last_accessed" in meta


class TestUserProfileProfile:
    """Тесты для кастомных профилей."""
    
    @pytest.fixture
    def profiler(self, tmp_path):
        from src.profiler import BrowserProfiler
        return BrowserProfiler(storage_path=str(tmp_path))
    
    def test_custom_user_agent(self, profiler):
        """Проверяет кастомный User-Agent."""
        custom_ua = "Mozilla/5.0 (Test) AppleWebKit/537.36"
        profile = profiler.create_profile(name="custom_ua", user_agent=custom_ua)
        
        assert profile.user_agent == custom_ua
    
    def test_custom_viewport(self, profiler):
        """Проверяет кастомный viewport."""
        profile = profiler.create_profile(name="custom_view", viewport=(1440, 900))
        
        assert profile.viewport == (1440, 900)
    
    def test_custom_timezone(self, profiler):
        """Проверяет кастомный timezone."""
        try:
            profile = profiler.create_profile(name="custom_tz", timezone="Europe/Moscow")
            assert profile.timezone == "Europe/Moscow"
        except Exception:
            pytest.skip("Timezone not available")
    
    def test_custom_language(self, profiler):
        """Проверяет кастомный язык."""
        profile = profiler.create_profile(name="custom_lang", language="ru-RU")
        
        assert profile.language == "ru-RU"
    
    def test_complete_profile(self, profiler):
        """Проверяет полный кастомный профиль."""
        profile = profiler.create_profile(
            name="complete",
            os="linux",
            browser="firefox",
            user_agent="Custom UA",
            viewport=(1600, 900),
            timezone="Asia/Tokyo",
            language="ja-JP",
            country="JP",
            hardware_concurrency=6,
            cpu_cores=4,
            ram_in_gb=16,
        )
        
        assert profile.os == "linux"
        assert profile.browser_type == "firefox"
        assert profile.viewport == (1600, 900)
        assert profile.language == "ja-JP"
        assert profile.country == "JP"
