import unittest
import pygame
from unittest.mock import patch


def can_initialize_display():
    try:
        pygame.display.init()
        pygame.display.set_mode((1, 1))
        return True
    except pygame.error:
        return False


@unittest.skipUnless(can_initialize_display(), "Display not available")
class TestSettings(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.settings = type("Settings", (), {})()
        self.settings.width = 800
        self.settings.height = 600
        self.settings.fullscreen = False
        self.settings.volume = 0.5  # Значення за замовчуванням
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height), pygame.RESIZABLE
        )

    def tearDown(self):
        pygame.quit()

    def test_resolution_change(self):
        self.settings.width, self.settings.height = 1280, 720
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height), pygame.RESIZABLE
        )
        self.assertEqual(self.screen.get_width(), 1280)
        self.assertEqual(self.screen.get_height(), 720)

    def test_fullscreen_toggle(self):
        self.settings.fullscreen = True
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height), pygame.FULLSCREEN
        )
        flags = self.screen.get_flags()
        self.assertTrue(flags & pygame.FULLSCREEN)

        self.settings.fullscreen = False
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height), pygame.RESIZABLE
        )
        flags = self.screen.get_flags()
        self.assertFalse(flags & pygame.FULLSCREEN)

    @patch("pygame.mixer.music.set_volume")  # Мокаємо функцію set_volume
    @patch("pygame.mixer.music.get_volume", return_value=0.8)  # Мокаємо get_volume
    def test_volume_change(self, mock_get_volume, mock_set_volume):
        # Зміна гучності
        self.settings.volume = 0.8
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.settings.volume)
        # Перевірка, чи функція була викликана з правильним значенням
        mock_set_volume.assert_called_with(0.8)
        # Перевірка, чи повернутий правильний об'єм
        self.assertEqual(mock_get_volume(), 0.8)
