# tests/test_settings.py
import pygame
import pytest
import os
import json
from unittest.mock import Mock, patch
from Settings import Settings

pygame.init()

# Фікстура для створення об'єкта Settings
@pytest.fixture
def settings(tmp_path):
    cap = Mock()
    settings_file = tmp_path / "settings.json"
    settings = Settings(width=1920, height=1080, cap=cap)
    settings.SETTINGS_FILE = str(settings_file)
    return settings

# Параметризований тест для перевірки ініціалізації гучності
@pytest.mark.parametrize("volume, expected_volume", [
    (0.5, 0.5),
    (0.0, 0.0),
    (1.0, 1.0),
])
def test_settings_initialization(settings, volume, expected_volume):
    with open(settings.SETTINGS_FILE, "w") as f:
        json.dump({"volume": volume}, f)
    settings.load_settings()
    assert settings.volume == expected_volume

# Тест із мокуванням для перевірки збереження налаштувань
@patch("os.path.exists", return_value=True)
@patch("json.dump")
def test_save_settings_mocked(mock_json_dump, mock_exists, settings):
    settings.save_settings()
    mock_json_dump.assert_called_once()
    assert settings.settings_saved is True

# Тест для перевірки збільшення гучності
def test_increase_volume(settings):
    initial_volume = settings.volume
    settings.increase_volume()
    assert settings.volume == min(1.0, initial_volume + 0.1)
    expected_slider_x = settings.slider_x_start + int(settings.volume * settings.slider_width)
    assert settings.slider_x == expected_slider_x

# Тест для перевірки зменшення гучності
def test_decrease_volume(settings):
    initial_volume = settings.volume
    settings.decrease_volume()
    assert settings.volume == max(0.0, initial_volume - 0.1)
    expected_slider_x = settings.slider_x_start + int(settings.volume * settings.slider_width)
    assert settings.slider_x == expected_slider_x

# Тест із мокуванням для звуку
@patch("pygame.mixer.Sound")
def test_volume_update_sound_mocked(mock_sound, settings):
    settings.sound_loaded = True
    settings.sound = mock_sound
    initial_volume = settings.volume
    settings.increase_volume()
    mock_sound.set_volume.assert_called_with(settings.volume)

# Тест для перевірки перемикання повноекранного режиму
@patch("pygame.display.set_mode")
@patch("pygame.display.Info")
def test_toggle_fullscreen(mock_info, mock_set_mode, settings):
    mock_info.return_value.current_w = 1920
    mock_info.return_value.current_h = 1080
    mock_screen = Mock()
    mock_screen.get_width.return_value = 1920
    mock_screen.get_height.return_value = 1080
    mock_set_mode.return_value = mock_screen

    settings.fullscreen = False
    settings.toggle_fullscreen(Mock())
    assert settings.fullscreen is True
    assert settings.width == 1920
    assert settings.height == 1080

# Тест для перевірки зміни роздільної здатності
@patch("pygame.display.set_mode")
def test_change_resolution(mock_set_mode, settings):
    mock_screen = Mock()
    mock_screen.get_width.return_value = 1280
    mock_screen.get_height.return_value = 720
    mock_set_mode.return_value = mock_screen

    settings.width = 1920
    settings.height = 1080
    settings.change_resolution(Mock())
    assert settings.width == 1280
    assert settings.height == 720

# Тест із маркером
@pytest.mark.skip(reason="Демонстрація маркерів")
def test_settings_skipped():
    assert False