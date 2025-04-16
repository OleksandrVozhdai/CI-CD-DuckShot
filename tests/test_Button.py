import pytest
import pygame
from unittest.mock import Mock, patch
from Button import ImageButton

def test_draw_button(button, screen):
    button.draw(screen)


@pytest.mark.parametrize("mouse_pos, expected", [
    ((110, 110), True),
    ((50, 50), False),
])
def test_check_hover(button, mouse_pos, expected):
    button.check_hover(mouse_pos)
    assert button.is_hovered == expected


@pytest.mark.parametrize("volume", [0, 0.3, 1])
def test_handle_event_with_sound(button, volume):
    fake_sound = Mock()
    button.sound = fake_sound
    button.settings.get_volume.return_value = volume
    button.is_hovered = True

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
    button.handle_event(event)

    if volume > 0:
        fake_sound.play.assert_called_once()
    else:
        fake_sound.play.assert_not_called()
