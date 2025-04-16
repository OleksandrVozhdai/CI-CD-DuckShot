# file for fixtures

import pygame
import pytest
import sys
import os
from unittest.mock import Mock
from Game import Game

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))
from Button import ImageButton

#Bird fixtures

@pytest.fixture
def dummy_sprite_sheet():
    pygame.init()
    surface = pygame.Surface((128, 128))
    return surface

#Button fixtures

@pytest.fixture
def button_setup():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((800, 600))
    return screen


@pytest.fixture
def dummy_button_settings():
    mock_settings = Mock()
    mock_settings.get_volume.return_value = 0.5
    return mock_settings


@pytest.fixture
def button(button_setup, dummy_button_settings):
    return ImageButton(
        x=100, y=100,
        width=200, height=100,
        text="Click Me",
        image_path="tests/assets/button.png",
        hover_image_path="tests/assets/button_hover.png",
        sound_path="tests/assets/click.mp3",
        settings=dummy_button_settings
    )

@pytest.fixture(scope="session", autouse=True)
def set_cwd_to_project_root():
    os.chdir(os.path.dirname(os.path.dirname(__file__)))

@pytest.fixture
def dummy_screen():
    pygame.init()
    return pygame.display.set_mode((800, 600))

@pytest.fixture
def game_instance(dummy_screen):
    return Game(
        fullscreen=False,
        screen=dummy_screen,
        bird_speed=0,
        birdLevelCount=5,
        levelType=1,
        ammoLevel=0
    )