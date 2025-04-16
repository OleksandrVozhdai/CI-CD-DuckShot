# file for fixtures

import pygame
import pytest
import sys
import os
from unittest.mock import Mock, patch
from unittest import mock


sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))
from Button import ImageButton
from Game import Game

#Bird fixtures

@pytest.fixture
def dummy_sprite_sheet():
    pygame.init()
    surface = pygame.Surface((128, 128))
    return surface

#Button fixtures

@pytest.fixture
def screen():
    return pygame.Surface((800, 600))  # Headless-compatible surface


@pytest.fixture
def mock_settings():
    settings = Mock()
    settings.get_volume.return_value = 0.5
    return settings


@pytest.fixture
def button(mock_settings):
    with patch("pygame.mixer.Sound", return_value=Mock()):
        return ImageButton(
            x=100, y=100,
            width=200, height=100,
            text="Click Me",
            image_path="tests/assets/button.png",
            hover_image_path="tests/assets/button_hover.png",
            sound_path="tests/assets/click.mp3",
            settings=mock_settings
        )


@pytest.fixture(scope="session", autouse=True)
def set_cwd_to_project_root():
    os.chdir(os.path.dirname(os.path.dirname(__file__)))

@pytest.fixture(autouse=True)
def mock_pygame_mixer_init():
    with patch("pygame.mixer.init"):
        yield

@pytest.fixture
def dummy_screen():
    pygame.init()
    return pygame.display.set_mode((800, 600))

@pytest.fixture
def game_instance(dummy_screen):
    with mock.patch("pygame.mixer.init"), mock.patch("pygame.mixer.Sound"):
        return Game(
            fullscreen=False,
            screen=dummy_screen,
            bird_speed=0,
            birdLevelCount=5,
            levelType=1,
            ammoLevel=0
        )