#file for fixtures

import pygame
import pytest

@pytest.fixture
def dummy_sprite_sheet():
    pygame.init()
    surface = pygame.Surface((128, 128))
    return surface
