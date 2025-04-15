import pytest
import pygame
import sys
from unittest.mock import patch, MagicMock
from Game import Game
import time
import numpy as np
@pytest.fixture
def game_instance():
    """
    Фікстура для створення екземпляра гри.
    """
    pygame.init()
    game = Game()
    game.levelType = 1
    game.bird_speed = 5
    game.birdLevelCount = 10
    game.total_shots = 10
    game.total_hits = 7
    game.death_times = {1: 1000, 2: 1500}
    game.score = 500
    game.running = True
    game.show_controls = False
    game.paused = False
    game.exit_to_menu = False
    return game

@pytest.mark.game
def test_draw_pause_screen_runs(game_instance):
    try:
        game_instance.draw_pause_screen()
    except Exception as e:
        pytest.fail(f"draw_pause_screen() викликав помилку: {e}")


def test_show_statistics_runs(game_instance):
    try:
        game_instance.show_statistics()
    except Exception as e:
        pytest.fail(f"show_statistics() викликав помилку: {e}")


def test_quit_event(game_instance):
    with patch('pygame.event.get', return_value=[pygame.event.Event(pygame.QUIT)]):
        with pytest.raises(SystemExit):
            game_instance.handle_events()
        assert not game_instance.running


@pytest.mark.parametrize("key, attr", [
    (pygame.K_h, 'show_controls'),
    (pygame.K_p, 'paused')
])
def test_toggle_boolean_flags(game_instance, key, attr):
    event = pygame.event.Event(pygame.KEYDOWN, key=key)
    with patch('pygame.event.get', return_value=[event]):
        initial_value = getattr(game_instance, attr)
        game_instance.handle_events()
        assert getattr(game_instance, attr) == (not initial_value)


def test_escape_key_quits_game(game_instance):
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    with patch('pygame.event.get', return_value=[event]):
        with pytest.raises(SystemExit):
            game_instance.handle_events()
        assert not game_instance.running


def test_pause_unpause_game(game_instance):
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p)
    with patch('pygame.event.get', return_value=[event]):
        assert not game_instance.paused
        game_instance.handle_events()
        assert game_instance.paused
        game_instance.handle_events()
        assert not game_instance.paused


def test_exit_to_menu(game_instance):
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m)
    with patch('pygame.event.get', return_value=[event]):
        game_instance.handle_events()
        assert not game_instance.running
        assert game_instance.exit_to_menu


def test_mouse_click_event(game_instance):
    mouse_pos = (100, 200)
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
    with patch('pygame.event.get', return_value=[event]):
        with patch.object(game_instance, 'handle_mouse_click') as mock_handle:
            with patch('pygame.mouse.get_pos', return_value=mouse_pos):
                game_instance.handle_events()
                mock_handle.assert_called_once_with(mouse_pos)


# ДОДАТКОВІ ТЕСТИ ДЛЯ handle_mouse_click

@pytest.fixture
def setup_clickable_game(game_instance):
    bird = MagicMock()
    bird.check_collision.return_value = True
    bird.hp = 1
    bird.birdSpeed = 5
    bird.frame_delay = 10
    bird.value = 100
    bird.id = 3
    bird.kill = MagicMock()

    game_instance.birds = [bird]
    game_instance.ammo = 3
    game_instance.last_shot_time = 0
    game_instance.shootDelay = 500
    game_instance.total_shots = 0
    game_instance.total_hits = 0
    game_instance.birdLevelCount = 0
    game_instance.score = 0
    game_instance.death_times = {}

    return game_instance, bird


@patch('pygame.time.get_ticks', return_value=1000)
def test_handle_mouse_click_kills_bird(mock_ticks, setup_clickable_game):
    game, bird = setup_clickable_game
    game.handle_mouse_click((50, 50))

    assert game.ammo == 2
    assert game.total_shots == 1
    assert game.total_hits == 1
    assert game.birdLevelCount == 1
    assert game.score == 100
    assert bird.birdSpeed == 7
    assert bird.frame_delay == 8
    bird.kill.assert_called_once()
    assert game.death_times[bird.id] == 1000


@patch('pygame.time.get_ticks', return_value=1000)
def test_handle_mouse_click_does_not_kill_bird(mock_ticks, setup_clickable_game):
    game, bird = setup_clickable_game
    bird.hp = 2

    game.handle_mouse_click((50, 50))

    assert bird.hp == 1
    bird.kill.assert_not_called()
    assert game.total_hits == 0
    assert game.birdLevelCount == 0
    assert game.score == 0


@patch('pygame.time.get_ticks', return_value=400)
def test_handle_mouse_click_too_soon(mock_ticks, setup_clickable_game):
    game, bird = setup_clickable_game
    game.last_shot_time = 300  # лише 100мс пройшло

    game.handle_mouse_click((50, 50))

    assert game.total_shots == 0
    assert game.ammo == 3
    bird.kill.assert_not_called()


@patch('pygame.time.get_ticks', return_value=1000)
def test_handle_mouse_click_no_ammo(mock_ticks, setup_clickable_game):
    game, bird = setup_clickable_game
    game.ammo = 0

    game.handle_mouse_click((50, 50))

    assert game.total_shots == 0
    bird.kill.assert_not_called()

@pytest.mark.game
@patch('time.time', return_value=100)
def test_game_paused_no_update(mock_time, game_instance):
    game_instance.paused = True
    game_instance.running = True
    game_instance.update_game_state()
    assert game_instance.running  # нічого не змінилось


@pytest.mark.game
@patch('time.time', return_value=100)
@patch('pygame.mouse.set_visible')
def test_game_ends_after_40_seconds(mock_mouse, mock_time, game_instance):
    game_instance.start_time = 50
    game_instance.total_paused_time = 5
    game_instance.running = True
    game_instance.paused = False

    game_instance.update_game_state()

    assert not game_instance.running
    mock_mouse.assert_called_once_with(True)


@pytest.mark.game
@patch('pygame.time.get_ticks', return_value=10000)
def test_remove_dead_birds(mock_ticks, game_instance):
    bird = MagicMock()
    game_instance.birds = [bird]
    game_instance.death_times = {bird: 4000}  # пройшло 6000 мс

    game_instance.paused = False
    game_instance.start_time = 0
    game_instance.total_paused_time = 0

    with patch('time.time', return_value=10):
        game_instance.update_game_state()

    assert bird not in game_instance.birds
    assert bird not in game_instance.death_times


@pytest.mark.game
@patch('random.randint', return_value=0)
def test_spawn_bird_called(mock_randint, game_instance):
    game_instance.spawn_bird = MagicMock()
    game_instance.birds = []
    game_instance.death_times = {}
    game_instance.paused = False
    game_instance.start_time = 0
    game_instance.total_paused_time = 0

    with patch('time.time', return_value=1), patch('pygame.time.get_ticks', return_value=1000):
        game_instance.update_game_state()

    game_instance.spawn_bird.assert_called_once()


@pytest.mark.game
@pytest.mark.parametrize("tick_time", [1000, 5000, 9999])
def test_birds_are_updated(game_instance, tick_time):
    bird = MagicMock()
    game_instance.birds = [bird]
    game_instance.death_times = {}
    game_instance.paused = False
    game_instance.start_time = 0
    game_instance.total_paused_time = 0

    with patch('time.time', return_value=1), patch('pygame.time.get_ticks', return_value=tick_time):
        game_instance.update_game_state()

    bird.update.assert_called_once()


@pytest.mark.game
@patch('pygame.time.get_ticks', return_value=10000)
@pytest.mark.parametrize("last_shot,expected_ammo", [(6000, 8), (9000, 0), (8000, 0)])
def test_reload_ammo_timing(mock_ticks, game_instance, last_shot, expected_ammo):
    game_instance.ammo = 0
    game_instance.last_shot_time = last_shot
    game_instance.paused = False
    game_instance.start_time = 0
    game_instance.total_paused_time = 0

    with patch('time.time', return_value=1):
        game_instance.update_game_state()

    assert game_instance.ammo == expected_ammo

@pytest.fixture
def game_instance_with_assets():
    game = Game()
    game.birdLevelCount = 5
    game.spawn_point = [[100, 200], [150, 250]]
    game.ground_spawn_point = [300, 400]
    game.birds = []

    # Мокування спрайтів
    game.sprite_sheet_blue = MagicMock()
    game.sprite_sheet_red = MagicMock()
    game.sprite_sheet_yellow = MagicMock()
    game.sprite_sheet_BlackFatty = MagicMock()
    game.sprite_sheet_Diagonally = MagicMock()

    game.SpritePerRow = 5
    game.SpriteWidth_Blue = 64
    game.SpriteHeight_Blue = 64
    game.SpriteWidth_Red = 64
    game.SpriteHeight_Red = 64
    game.SpriteWidth_Yellow = 64
    game.SpriteHeight_Yellow = 64
    game.SpriteWidth_BlackFatty = 64
    game.SpriteHeight_BlackFatty = 64
    game.SpriteWidth_Diagonally = 64
    game.SpriteHeight_Diagonally = 64

    return game

@pytest.mark.parametrize("bird_type", [
    "blue",
    "red",
    "yellow",
    "black-fatty",
    "diagonally"
])
@pytest.mark.game
def test_spawn_specific_bird(game_instance_with_assets, bird_type):
    """
    Перевіряє, чи створюється птах відповідного типу та додається до списку birds.
    """
    game = game_instance_with_assets

    with patch('random.choice') as mock_choice, patch('random.choices', return_value=[bird_type]):
        mock_choice.side_effect = lambda x: x[0]  # завжди вибирає перший елемент
        game.spawn_bird()

    assert len(game.birds) == 1
    bird = game.birds[0]
    assert isinstance(bird, object)
    assert game.birdLevelCount == 4  # зменшився на 1

@pytest.mark.game
def test_no_spawn_when_bird_count_zero(game_instance_with_assets):
    """
    Перевіряє, що птах не спавниться, коли birdLevelCount == 0
    """
    game = game_instance_with_assets
    game.birdLevelCount = 0

    with patch('random.choices') as mock_random:
        game.spawn_bird()
        mock_random.assert_not_called()  # random.choices не викликається
        assert len(game.birds) == 0

