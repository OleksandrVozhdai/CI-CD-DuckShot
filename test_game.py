import pytest
import pygame
import sys
from unittest.mock import patch, MagicMock
from Game import Game


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


def test_toggle_show_controls(game_instance):
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_h)
    with patch('pygame.event.get', return_value=[event]):
        initial_state = game_instance.show_controls
        game_instance.handle_events()
        assert game_instance.show_controls == (not initial_state)


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
