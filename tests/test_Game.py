import pytest
from unittest.mock import patch
from Game import Game

# Комбіноване мокування: init і Sound
@pytest.mark.basic
@patch("pygame.mixer.init", return_value=None)
@patch("pygame.mixer.Sound", return_value=None)
def test_initial_score_zero(mock_sound, mock_mixer_init, game_instance):
    assert game_instance.score == 0

@pytest.mark.basic
@patch("pygame.mixer.init", return_value=None)
@patch("pygame.mixer.Sound", return_value=None)
@pytest.mark.parametrize("expected_ammo", [4])
def test_initial_ammo(mock_sound, mock_mixer_init, game_instance, expected_ammo):
    assert game_instance.ammo == expected_ammo
    assert game_instance.magazine == expected_ammo

@pytest.mark.init
@patch("pygame.mixer.init", return_value=None)
@patch("pygame.mixer.Sound", return_value=None)
def test_screen_is_initialized(mock_sound, mock_mixer_init, game_instance):
    assert game_instance.screen is not None

@pytest.mark.init
@patch("pygame.mixer.init", return_value=None)
@patch("pygame.mixer.Sound", return_value=None)
def test_birds_list_is_empty_on_start(mock_sound, mock_mixer_init, game_instance):
    assert isinstance(game_instance.birds, list)
    assert len(game_instance.birds) == 0

@pytest.mark.spawn
@patch("pygame.mixer.init", return_value=None)
@patch("pygame.mixer.Sound", return_value=None)
def test_bird_spawn_decreases_level_count(mock_sound, mock_mixer_init, game_instance):
    initial_count = game_instance.birdLevelCount
    game_instance.spawn_bird()
    assert len(game_instance.birds) == 1
    assert game_instance.birdLevelCount == initial_count - 1
