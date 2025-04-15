import sys
import os.path
# Додаємо корінь проєкту до sys.path перед імпортами
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pygame
import cv2
from Settings import Settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        # Ініціалізація Pygame та його модулів перед кожним тестом
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        # Отримуємо інформацію про екран
        self.info = pygame.display.Info()
        # Завантажуємо відео для фону з абсолютним шляхом
        video_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "Assets", "Background", "lvl1.mp4"
        )
        # Дебагінг: перевіряємо, чи файл існує
        if not os.path.exists(video_path):
            self.fail(f"Файл {video_path} не існує")
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            self.fail(f"Не вдалося відкрити відео {video_path}")
        # Створюємо об’єкт Settings з поточною роздільною здатністю та відео
        self.settings = Settings(
            self.info.current_w, self.info.current_h, self.cap
        )
        # Ініціалізуємо екран у змінному розмірі
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height), pygame.RESIZABLE
        )

    def tearDown(self):
        # Звільняємо ресурси після кожного тесту
        self.cap.release()
        pygame.quit()

    def test_resolution_change(self):
        # Зберігаємо оригінальну роздільну здатність
        original_width = self.settings.width
        original_height = self.settings.height
        # Змінюємо роздільну здатність на 1280x720
        self.settings.width, self.settings.height = 1280, 720
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height), pygame.RESIZABLE
        )
        # Отримуємо нову роздільну здатність екрана
        new_width = self.screen.get_width()
        new_height = self.screen.get_height()
        # Перевіряємо, чи роздільна здатність змінилася коректно
        self.assertEqual(new_width, 1280)
        self.assertEqual(new_height, 720)
        # Відновлюємо оригінальну роздільну здатність
        self.settings.width = original_width
        self.settings.height = original_height
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height), pygame.RESIZABLE
        )

    def test_fullscreen_toggle(self):
        # Увімкнення повноекранного режиму
        self.settings.fullscreen = True
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height), pygame.FULLSCREEN
        )
        # Отримуємо поточні флаги екрана
        flags = pygame.display.get_surface().get_flags()
        # Перевіряємо, чи повноекранний режим увімкнено
        self.assertTrue(flags & pygame.FULLSCREEN)
        # Вимикаємо повноекранний режим
        self.settings.fullscreen = False
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height), pygame.RESIZABLE
        )
        # Перевіряємо, чи повноекранний режим вимкнено
        flags = pygame.display.get_surface().get_flags()
        self.assertFalse(flags & pygame.FULLSCREEN)

    def test_volume_change(self):
        # Завантажуємо музику для тестування гучності з абсолютним шляхом
        music_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "Assets", "Sounds", "level_music.mp3"
        )
        if not os.path.exists(music_path):
            self.fail(f"Не вдалося знайти музику {music_path}")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        # Встановлюємо гучність на 0.3
        self.settings.volume = 0.3
        pygame.mixer.music.set_volume(self.settings.volume)
        # Перевіряємо, чи гучність встановлена коректно
        self.assertAlmostEqual(
            pygame.mixer.music.get_volume(), 0.3, delta=0.01
        )
        # Змінюємо гучність на 0.7
        self.settings.volume = 0.7
        pygame.mixer.music.set_volume(self.settings.volume)
        # Перевіряємо, чи нова гучність застосована коректно
        self.assertAlmostEqual(
            pygame.mixer.music.get_volume(), 0.7, delta=0.01
        )
        # Зупиняємо музику після тесту
        pygame.mixer.music.stop()


if __name__ == '__main__':
    unittest.main()