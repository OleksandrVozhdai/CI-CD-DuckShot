import os.path
import json
import pygame
import cv2
import sys
from Button import ImageButton

# Ініціалізація мікшера Pygame
pygame.mixer.init()


class Settings:
    def __init__(self, width, height, cap):
        """Ініціалізація налаштувань."""
        # Файл для збереження налаштувань
        self.SETTINGS_FILE = "settings.json"

        # Значення за замовчуванням
        self.volume = 0.5  # Гучність
        self.crosshair_size = 20  # Розмір прицілу
        self.difficulty = "Medium"  # Складність
        self.brightness = 0.8  # Яскравість
        self.width = width  # Ширина екрана
        self.height = height  # Висота екрана
        self.fullscreen = False  # Повноекранний режим (вимкнено)
        self.cap = cap  # Відеопотік
        self.sound_enabled = True  # Звук увімкнено

        # Налаштування слайдера гучності
        self.slider_width = self.width // 3  # Ширина слайдера
        self.slider_x_start = (self.width - self.slider_width) // 2
        self.slider_x = self.slider_x_start + int(
            self.volume * self.slider_width
        )
        self.slider_dragging = False  # Чи перетягується повзунок

        # Завантажуємо налаштування з файлу
        self.load_settings()

        # Оновлюємо позицію повзунка після завантаження гучності
        self.update_slider_position()

        # Завантажуємо звук кнопок з абсолютним шляхом
        self.sound_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "Assets", "Sounds", "click.mp3"
        )
        self.sound_loaded = os.path.exists(self.sound_path)
        if self.sound_loaded:
            self.sound = pygame.mixer.Sound(self.sound_path)
            self.sound.set_volume(self.volume)  # Встановлюємо гучність
        else:
            print(f"Попередження: Файл {self.sound_path} не знайдено.")
            print("Звук кнопок не завантажено.")
            self.sound = None

        # Прапорець для відображення повідомлення про збереження
        self.settings_saved = False

    def save_settings(self):
        """Зберігає поточні налаштування у файл."""
        try:
            settings_data = {
                "volume": self.volume,
                "width": self.width,
                "height": self.height,
                "fullscreen": self.fullscreen
            }
            with open(self.SETTINGS_FILE, "w") as file:
                json.dump(settings_data, file)
            self.settings_saved = True
            print(f"✅ Налаштування збережено у {self.SETTINGS_FILE}")
        except Exception as e:
            print(f"❌ Помилка збереження налаштувань: {e}")

    def load_settings(self):
        """Завантажує налаштування з файлу або створює новий."""
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r") as file:
                    data = json.load(file)
                    self.volume = data.get("volume", 0.5)
                    self.width = data.get(
                        "width", pygame.display.Info().current_w)
                    self.height = data.get(
                        "height", pygame.display.Info().current_h)
                    self.fullscreen = data.get("fullscreen", False)
                    print(
                        f"🔄 Завантажено гучність: {self.volume * 100}%, "
                        f"роздільна здатність: {self.width}x{self.height}, "
                        f"Повноекранний режим: {self.fullscreen}"
                    )
            except json.JSONDecodeError:
                print("⚠️ Помилка завантаження налаштувань! Використовуються "
                      "значення за замовчуванням.")
        else:
            print("⚠️ Файл налаштувань відсутній. Створюємо новий...")
            self.save_settings()

    def update_slider_position(self):
        """Оновлює позицію повзунка відповідно до гучності."""
        self.slider_width = self.width // 3
        self.slider_x_start = (self.width - self.slider_width) // 2
        self.slider_x = self.slider_x_start + int(
            self.volume * self.slider_width
        )

    def increase_volume(self):
        """Збільшує гучність, зберігає зміни та оновлює звук."""
        self.volume = min(1.0, self.volume + 0.1)
        self.update_slider_position()
        self.save_settings()
        if self.sound_loaded and self.sound:
            self.sound.set_volume(self.volume)

    def decrease_volume(self):
        """Зменшує гучність, зберігає зміни та оновлює звук."""
        self.volume = max(0.0, self.volume - 0.1)
        self.update_slider_position()
        self.save_settings()
        if self.sound_loaded and self.sound:
            self.sound.set_volume(self.volume)

    def get_volume(self):
        """Повертає поточний рівень гучності."""
        return self.volume

    def fade_screen(self, screen):
        """Створює чорний fade-перехід на екрані."""
        fade_surface = pygame.Surface((self.width, self.height))
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 256, 10):  # Плавне збільшення прозорості
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)

    def settings_menu(self, screen, font, draw_text_with_outline, main_menu):
        """Відображає меню налаштувань."""
        # Зупиняємо будь-яку фонову музику
        pygame.mixer.music.stop()

        # Ініціалізація кнопок для меню налаштувань
        button_width, button_height = 252, 74
        audio_button = ImageButton(
            (self.width - button_width) / 2,
            self.height * 0.35,
            button_width, button_height, "",
            "Assets/Buttons/audio_button.png",
            "Assets/Buttons/audio_button_hover.png", ""
        )
        video_button = ImageButton(
            (self.width - button_width) / 2,
            self.height * 0.45,
            button_width, button_height, "",
            "Assets/Buttons/video_button.png",
            "Assets/Buttons/video_button_hover.png", ""
        )
        back_button = ImageButton(
            (self.width - button_width) / 2,
            self.height * 0.55,
            button_width, button_height, "",
            "Assets/Buttons/exit_button.png",
            "Assets/Buttons/exit_button_hover.png", ""
        )

        running = True
        while running:
            try:
                if self.cap:
                    ret, frame = self.cap.read()
                    if not ret:
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(
                        frame, (self.width, self.height),
                        interpolation=cv2.INTER_AREA
                    )
                    frame_surface = pygame.surfarray.make_surface(
                        frame.swapaxes(0, 1))
                    screen.blit(frame_surface, (0, 0))
            except Exception as e:
                print(f"Помилка при обробці відео: {e}")
                screen.fill((0, 0, 0))

            # Відображення заголовка
            draw_text_with_outline(
                "Settings", font, (255, 255, 255), (0, 0, 0),
                self.width / 2, self.height * 0.2
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.fade_screen(screen)
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.fade_screen(screen)
                        running = False
                        return screen
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if audio_button.rect.collidepoint(event.pos):
                        if self.sound_loaded and self.sound:
                            self.sound.play()
                        self.fade_screen(screen)
                        screen = self.audio_settings(
                            screen, font, draw_text_with_outline, main_menu)
                        if screen:
                            self.width = screen.get_width()
                            self.height = screen.get_height()
                            # Оновлюємо кнопки після зміни розширення
                            audio_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.35,
                                button_width, button_height, "",
                                "Assets/Buttons/audio_button.png",
                                "Assets/Buttons/audio_button_hover.png", ""
                            )
                            video_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.45,
                                button_width, button_height, "",
                                "Assets/Buttons/video_button.png",
                                "Assets/Buttons/video_button_hover.png", ""
                            )
                            back_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.55,
                                button_width, button_height, "",
                                "Assets/Buttons/exit_button.png",
                                "Assets/Buttons/exit_button_hover.png", ""
                            )
                    elif video_button.rect.collidepoint(event.pos):
                        if self.sound_loaded and self.sound:
                            self.sound.play()
                        self.fade_screen(screen)
                        screen = self.video_settings(
                            screen, font, draw_text_with_outline, main_menu)
                        if screen:
                            self.width = screen.get_width()
                            self.height = screen.get_height()
                            # Оновлюємо кнопки після зміни розширення
                            audio_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.35,
                                button_width, button_height, "",
                                "Assets/Buttons/audio_button.png",
                                "Assets/Buttons/audio_button_hover.png", ""
                            )
                            video_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.45,
                                button_width, button_height, "",
                                "Assets/Buttons/video_button.png",
                                "Assets/Buttons/video_button_hover.png", ""
                            )
                            back_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.55,
                                button_width, button_height, "",
                                "Assets/Buttons/exit_button.png",
                                "Assets/Buttons/exit_button_hover.png", ""
                            )
                    elif back_button.rect.collidepoint(event.pos):
                        if self.sound_loaded and self.sound:
                            self.sound.play()
                        self.fade_screen(screen)
                        running = False
                        return screen

                buttons = [audio_button, video_button, back_button]
                for btn in buttons:
                    btn.handle_event(event)

            # Оновлюємо позиції кнопок
            audio_button.rect.topleft = (
                (self.width - button_width) / 2, self.height * 0.35)
            video_button.rect.topleft = (
                (self.width - button_width) / 2, self.height * 0.45)
            back_button.rect.topleft = (
                (self.width - button_width) / 2, self.height * 0.55)

            # Відображення кнопок
            buttons = [audio_button, video_button, back_button]
            for btn in buttons:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

            pygame.display.flip()

        return screen

    def audio_settings(self, screen, font, draw_text_with_outline, main_menu):
        """Відображає меню аудіо налаштувань."""
        button_width, button_height = 252, 74
        mute_button = ImageButton(
            (self.width - button_width) / 2,
            self.height * 0.35,
            button_width, button_height, "",
            "Assets/Buttons/mute_button.png",
            "Assets/Buttons/mute_button_hover.png", ""
        )
        save_button = ImageButton(
            (self.width - button_width) / 2,
            self.height * 0.45,
            button_width, button_height, "",
            "Assets/Buttons/save_button.png",
            "Assets/Buttons/save_button_hover.png", ""
        )
        back_button = ImageButton(
            (self.width - button_width) / 2,
            self.height * 0.55,
            button_width, button_height, "",
            "Assets/Buttons/back_button.png",
            "Assets/Buttons/back_button_hover.png", ""
        )

        running = True
        settings_changed = False
        previous_volume = self.volume
        self.settings_saved = False

        while running:
            try:
                if self.cap:
                    ret, frame = self.cap.read()
                    if not ret:
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(
                        frame, (self.width, self.height),
                        interpolation=cv2.INTER_AREA
                    )
                    frame_surface = pygame.surfarray.make_surface(
                        frame.swapaxes(0, 1))
                    screen.blit(frame_surface, (0, 0))
            except Exception as e:
                print(f"Помилка при обробці відео: {e}")
                screen.fill((0, 0, 0))

            # Відображення елементів аудіо налаштувань
            draw_text_with_outline(
                "Audio Settings", font, (255, 255, 255), (0, 0, 0),
                self.width / 2, self.height * 0.1
            )
            pygame.draw.rect(
                screen, (255, 255, 255),
                (self.slider_x_start, self.height * 0.15, self.slider_width, 8)
            )
            pygame.draw.rect(
                screen, (0, 255, 0),
                (self.slider_x_start, self.height * 0.15,
                 int(self.volume * self.slider_width), 8)
            )
            pygame.draw.circle(
                screen, (255, 255, 255),
                (self.slider_x, int(self.height * 0.15 + 4)), 10
            )
            draw_text_with_outline(
                f"Volume: {int(self.volume * 100)}%", font,
                (255, 255, 255), (0, 0, 0), self.width / 2, self.height * 0.2
            )
            if self.settings_saved and not settings_changed:
                draw_text_with_outline(
                    "Налаштування збережено!", font,
                    (0, 255, 0), (0, 0, 0), self.width / 2, self.height * 0.7
                )
            elif settings_changed:
                draw_text_with_outline(
                    "Налаштування не збережено!", font,
                    (255, 0, 0), (0, 0, 0), self.width / 2, self.height * 0.7
                )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.fade_screen(screen)
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if settings_changed and not self.settings_saved:
                            self.volume = previous_volume
                            self.update_slider_position()
                            if self.sound_loaded and self.sound:
                                self.sound.set_volume(self.volume)
                        self.fade_screen(screen)
                        running = False
                        return screen
                    elif event.key == pygame.K_m:
                        if self.volume > 0.0:
                            self.sound_enabled = False
                            self.volume = 0.0
                            self.slider_x = self.slider_x_start
                            if self.sound_loaded and self.sound:
                                self.sound.set_volume(0.0)
                            settings_changed = True
                            self.settings_saved = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (abs(event.pos[0] - self.slider_x) <= 10 and
                            (self.height * 0.15 - 4) <= event.pos[1] <=
                            (self.height * 0.15 + 12)):
                        self.slider_dragging = True
                    elif mute_button.rect.collidepoint(event.pos):
                        if self.volume > 0.0:
                            self.sound_enabled = False
                            self.volume = 0.0
                            self.slider_x = self.slider_x_start
                            if self.sound_loaded and self.sound:
                                self.sound.set_volume(0.0)
                            settings_changed = True
                            self.settings_saved = False
                        if self.sound_loaded and self.sound:
                            self.sound.play()
                        self.fade_screen(screen)
                    elif save_button.rect.collidepoint(event.pos):
                        self.save_settings()
                        previous_volume = self.volume
                        settings_changed = False
                        if self.sound_loaded and self.sound:
                            self.sound.play()
                        self.fade_screen(screen)
                        print("✅ Налаштування збережено!")
                    elif back_button.rect.collidepoint(event.pos):
                        if settings_changed and not self.settings_saved:
                            self.volume = previous_volume
                            self.update_slider_position()
                            if self.sound_loaded and self.sound:
                                self.sound.set_volume(self.volume)
                        if self.sound_loaded and self.sound:
                            self.sound.play()
                        self.fade_screen(screen)
                        running = False
                        return screen

                if event.type == pygame.MOUSEBUTTONUP:
                    self.slider_dragging = False

                if event.type == pygame.MOUSEMOTION and self.slider_dragging:
                    max_width = self.slider_x_start + self.slider_width
                    min_x = min(event.pos[0], max_width)
                    self.slider_x = max(self.slider_x_start, min_x)
                    delta_x = self.slider_x - self.slider_x_start
                    self.volume = delta_x / self.slider_width
                    if self.sound_loaded and self.sound:
                        self.sound.set_volume(self.volume)
                    settings_changed = True
                    self.settings_saved = False

                if event.type == pygame.VIDEORESIZE:
                    if not self.fullscreen:
                        self.width, self.height = event.w, event.h
                        self.slider_width = self.width // 3
                        width_diff = self.width - self.slider_width
                        slider_width_half = width_diff / 2
                        self.slider_x_start = slider_width_half
                        self.update_slider_position()
                        screen = pygame.display.set_mode(
                            (self.width, self.height), pygame.RESIZABLE
                        )
                        mute_button = ImageButton(
                            (self.width - button_width) / 2,
                            self.height * 0.35,
                            button_width, button_height, "",
                            "Assets/Buttons/mute_button.png",
                            "Assets/Buttons/mute_button_hover.png", ""
                        )
                        save_button = ImageButton(
                            (self.width - button_width) / 2,
                            self.height * 0.45,
                            button_width, button_height, "",
                            "Assets/Buttons/save_button.png",
                            "Assets/Buttons/save_button_hover.png", ""
                        )
                        back_button = ImageButton(
                            (self.width - button_width) / 2,
                            self.height * 0.55,
                            button_width, button_height, "",
                            "Assets/Buttons/back_button.png",
                            "Assets/Buttons/back_button_hover.png", ""
                        )

                mute_button.handle_event(event)
                save_button.handle_event(event)
                back_button.handle_event(event)

            # Відображення кнопок
            mute_button.check_hover(pygame.mouse.get_pos())
            mute_button.draw(screen)
            save_button.check_hover(pygame.mouse.get_pos())
            save_button.draw(screen)
            back_button.check_hover(pygame.mouse.get_pos())
            back_button.draw(screen)

            pygame.display.flip()

        return screen

    def video_settings(self, screen, font, draw_text_with_outline, main_menu):
        """Відображає меню відео налаштувань."""
        button_width, button_height = 252, 74
        fullscreen_button = ImageButton(
            (self.width - button_width) / 2,
            self.height * 0.35,
            button_width, button_height, "",
            "Assets/Buttons/fullscreen_button.png",
            "Assets/Buttons/fullscreen_button_hover.png", ""
        )
        resolution_button = ImageButton(
            (self.width - button_width) / 2,
            self.height * 0.45,
            button_width, button_height, "",
            "Assets/Buttons/resolution_button.png",
            "Assets/Buttons/resolution_button_hover.png", ""
        )
        save_button = ImageButton(
            (self.width - button_width) / 2,
            self.height * 0.55,
            button_width, button_height, "",
            "Assets/Buttons/save_button.png",
            "Assets/Buttons/save_button_hover.png", ""
        )
        back_button = ImageButton(
            (self.width - button_width) / 2,
            self.height * 0.65,
            button_width, button_height, "",
            "Assets/Buttons/back_button.png",
            "Assets/Buttons/back_button_hover.png", ""
        )

        running = True
        while running:
            try:
                if self.cap:
                    ret, frame = self.cap.read()
                    if not ret:
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(
                        frame, (self.width, self.height),
                        interpolation=cv2.INTER_AREA
                    )
                    frame_surface = pygame.surfarray.make_surface(
                        frame.swapaxes(0, 1))
                    screen.blit(frame_surface, (0, 0))
            except Exception as e:
                print(f"Помилка при обробці відео: {e}")
                screen.fill((0, 0, 0))

            # Відображення елементів відео налаштувань
            draw_text_with_outline(
                "Video Settings", font, (255, 255, 255), (0, 0, 0),
                self.width / 2, self.height * 0.1
            )
            draw_text_with_outline(
                f"Resolution: {self.width}x{self.height}", font,
                (255, 255, 255), (0, 0, 0), self.width / 2, self.height * 0.2
            )
            fullscreen_text = (
                "Fullscreen: ON" if self.fullscreen else "Fullscreen: OFF")
            draw_text_with_outline(
                fullscreen_text, font, (255, 255, 255), (0, 0, 0),
                self.width / 2, self.height * 0.3
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.fade_screen(screen)
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.fade_screen(screen)
                        running = False
                        return screen
                    elif event.key == pygame.K_F11:
                        screen = self.toggle_fullscreen(screen)
                        if screen:
                            self.width = screen.get_width()
                            self.height = screen.get_height()
                            self.fade_screen(screen)
                            fullscreen_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.35,
                                button_width, button_height, "",
                                "Assets/Buttons/fullscreen_button.png",
                                "Assets/Buttons/fullscreen_button_hover.png",
                                ""
                            )
                            resolution_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.45,
                                button_width, button_height, "",
                                "Assets/Buttons/resolution_button.png",
                                "Assets/Buttons/resolution_button_hover.png",
                                ""
                            )
                            save_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.55,
                                button_width, button_height, "",
                                "Assets/Buttons/save_button.png",
                                "Assets/Buttons/save_button_hover.png", ""
                            )
                            back_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.65,
                                button_width, button_height, "",
                                "Assets/Buttons/back_button.png",
                                "Assets/Buttons/back_button_hover.png", ""
                            )
                if event.type == pygame.VIDEORESIZE:
                    if not self.fullscreen:
                        self.width = screen.get_width()
                        self.height = screen.get_height()
                        self.slider_width = self.width // 3
                        width_diff = self.width - self.slider_width
                        self.slider_x_start = width_diff / 2
                        self.update_slider_position()
                        screen = pygame.display.set_mode(
                            (self.width, self.height), pygame.RESIZABLE
                        )
                        fullscreen_button = ImageButton(
                            (self.width - button_width) / 2,
                            self.height * 0.35,
                            button_width, button_height, "",
                            "Assets/Buttons/fullscreen_button.png",
                            "Assets/Buttons/fullscreen_button_hover.png", ""
                        )
                        resolution_button = ImageButton(
                            (self.width - button_width) / 2,
                            self.height * 0.45,
                            button_width, button_height, "",
                            "Assets/Buttons/resolution_button.png",
                            "Assets/Buttons/resolution_button_hover.png", ""
                        )
                        save_button = ImageButton(
                            (self.width - button_width) / 2,
                            self.height * 0.55,
                            button_width, button_height, "",
                            "Assets/Buttons/save_button.png",
                            "Assets/Buttons/save_button_hover.png", ""
                        )
                        back_button = ImageButton(
                            (self.width - button_width) / 2,
                            self.height * 0.65,
                            button_width, button_height, "",
                            "Assets/Buttons/back_button.png",
                            "Assets/Buttons/back_button_hover.png", ""
                        )
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resolution_button.rect.collidepoint(event.pos):
                        screen = self.change_resolution(screen)
                        if screen:
                            self.width = screen.get_width()
                            self.height = screen.get_height()
                            fullscreen_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.35,
                                button_width, button_height, "",
                                "Assets/Buttons/fullscreen_button.png",
                                "Assets/Buttons/fullscreen_button_hover.png",
                                ""
                            )
                            resolution_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.45,
                                button_width, button_height, "",
                                "Assets/Buttons/resolution_button.png",
                                "Assets/Buttons/resolution_button_hover.png",
                                ""
                            )
                            save_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.55,
                                button_width, button_height, "",
                                "Assets/Buttons/save_button.png",
                                "Assets/Buttons/save_button_hover.png", ""
                            )
                            back_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.65,
                                button_width, button_height, "",
                                "Assets/Buttons/back_button.png",
                                "Assets/Buttons/back_button_hover.png", ""
                            )
                        if self.sound_loaded and self.sound:
                            self.sound.play()
                    elif fullscreen_button.rect.collidepoint(event.pos):
                        screen = self.toggle_fullscreen(screen)
                        if screen:
                            self.width = screen.get_width()
                            self.height = screen.get_height()
                            fullscreen_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.35,
                                button_width, button_height, "",
                                "Assets/Buttons/fullscreen_button.png",
                                "Assets/Buttons/fullscreen_button_hover.png",
                                ""
                            )
                            resolution_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.45,
                                button_width, button_height, "",
                                "Assets/Buttons/resolution_button.png",
                                "Assets/Buttons/resolution_button_hover.png",
                                ""
                            )
                            save_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.55,
                                button_width, button_height, "",
                                "Assets/Buttons/save_button.png",
                                "Assets/Buttons/save_button_hover.png", ""
                            )
                            back_button = ImageButton(
                                (self.width - button_width) / 2,
                                self.height * 0.65,
                                button_width, button_height, "",
                                "Assets/Buttons/back_button.png",
                                "Assets/Buttons/back_button_hover.png", ""
                            )
                        if self.sound_loaded and self.sound:
                            self.sound.play()
                    elif save_button.rect.collidepoint(event.pos):
                        self.save_settings()
                        if self.sound_loaded and self.sound:
                            self.sound.play()
                        self.fade_screen(screen)
                        print("✅ Налаштування відео збережено!")
                    elif back_button.rect.collidepoint(event.pos):
                        if self.sound_loaded and self.sound:
                            self.sound.play()
                        self.fade_screen(screen)
                        running = False
                        return screen

                for btn in [
                    fullscreen_button,
                    resolution_button,
                    save_button,
                    back_button
                ]:
                    btn.handle_event(event)

            # Оновлюємо позиції кнопок
            fullscreen_button.rect.topleft = (
                (self.width - button_width) / 2, self.height * 0.35
            )
            resolution_button.rect.topleft = (
                (self.width - button_width) / 2, self.height * 0.45
            )
            save_button.rect.topleft = (
                (self.width - button_width) / 2, self.height * 0.55
            )
            back_button.rect.topleft = (
                (self.width - button_width) / 2, self.height * 0.65
            )

            # Відображення кнопок
            for btn in [
                fullscreen_button,
                resolution_button,
                save_button,
                back_button
            ]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

            pygame.display.flip()

        return screen

    def toggle_fullscreen(self, screen):
        """Перемикає між віконним і повноекранним режимами."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            resolutions = [(3440, 1440), (2752, 1152), (1920, 1080),
                           (1280, 720), (1024, 768)]
            if (self.width, self.height) in resolutions:
                screen = pygame.display.set_mode(
                    (self.width, self.height), pygame.FULLSCREEN)
            else:
                info = pygame.display.Info()
                self.width, self.height = info.current_w, info.current_h
                screen = pygame.display.set_mode(
                    (self.width, self.height), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE)
            info = pygame.display.Info()
            if self.width > info.current_w or self.height > info.current_h:
                self.width = min(self.width, info.current_w)
                self.height = min(self.height, info.current_h)
                screen = pygame.display.set_mode(
                    (self.width, self.height), pygame.RESIZABLE)
        self.slider_width = self.width // 3
        self.slider_x_start = (self.width - self.slider_width) / 2
        self.update_slider_position()
        self.save_settings()
        return screen

    def change_resolution(self, screen):
        """Змінює роздільну здатність."""
        resolutions = [(3440, 1440), (2752, 1152), (1920, 1080),
                       (1280, 720), (1024, 768)]
        current_resolution = (self.width, self.height)
        index = (resolutions.index(current_resolution)
                 if current_resolution in resolutions else 0)
        new_resolution = resolutions[(index + 1) % len(resolutions)]
        self.width, self.height = new_resolution
        self.slider_width = self.width // 3
        self.slider_x_start = (self.width - self.slider_width) / 2
        self.update_slider_position()
        if self.fullscreen:
            screen = pygame.display.set_mode(
                (self.width, self.height), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE)
            info = pygame.display.Info()
            if self.width > info.current_w or self.height > info.current_h:
                self.width = min(self.width, info.current_w)
                self.height = min(self.height, info.current_h)
                screen = pygame.display.set_mode(
                    (self.width, self.height), pygame.RESIZABLE)
        self.save_settings()
        print(
            f"🔄 Змінено роздільну здатність на: {new_resolution[0]}x"
            f"{new_resolution[1]}"
        )
        return screen
