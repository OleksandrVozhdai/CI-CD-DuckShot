import os
import json
import pygame
import cv2
from Button import ImageButton

# Ініціалізація мікшера Pygame
pygame.mixer.init()

class Settings:
    def __init__(self, width, height, cap):
        self.SETTINGS_FILE = "settings.json"  # Файл для збереження налаштувань

        self.volume = 0.5  # Значення гучності за замовчуванням
        self.crosshair_size = 20
        self.difficulty = "Medium"
        self.brightness = 0.8
        self.width = width
        self.height = height
        self.fullscreen = False
        self.cap = cap
        self.sound_enabled = True

        # Зменшуємо довжину полоски гучності та коригуємо положення повзунка
        self.slider_width = self.width // 3  # Нова ширина полоски (коротша)
        self.slider_x_start = (self.width - self.slider_width) // 2  # Центруємо полоску
        self.slider_x = self.slider_x_start + int(self.volume * self.slider_width)
        self.slider_dragging = False

        # Завантажуємо налаштування гучності з файлу
        self.load_settings()

        # **Оновлення положення повзунка після завантаження гучності**
        self.update_slider_position()

        # Завантажуємо звук кнопок
        self.sound_path = "Assets/Sounds/click.mp3"
        self.sound_loaded = os.path.exists(self.sound_path)
        if self.sound_loaded:
            pygame.mixer.music.load(self.sound_path)
            pygame.mixer.music.set_volume(self.volume)  # Встановлюємо поточну гучність
        else:
            print(f"⚠️ Файл {self.sound_path} не знайдено! Звук кнопок вимкнено.")

        # Плашка з повідомленнями
        self.settings_saved = False  # Показує, чи були збережені налаштування

    def save_settings(self):
        """Зберігає поточні налаштування гучності у файл"""
        try:
            with open(self.SETTINGS_FILE, "w") as file:
                json.dump({"volume": self.volume}, file)
            self.settings_saved = True
            print(f"✅ Налаштування збережено у {self.SETTINGS_FILE}")
        except Exception as e:
            print(f"❌ Помилка збереження налаштувань: {e}")

    def load_settings(self):
        """Завантажує налаштування з файлу, якщо він існує. Якщо ні – створює новий файл"""
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r") as file:
                    data = json.load(file)
                    self.volume = data.get("volume", 0.5)  # Якщо файлу немає, використовуємо 50%
                    print(f"🔄 Завантажено гучність: {self.volume * 100}%")
            except json.JSONDecodeError:
                print("⚠️ Помилка завантаження налаштувань! Використовуються значення за замовчуванням.")
        else:
            print("⚠️ Файл налаштувань відсутній. Створюємо новий...")
            self.save_settings()  # Якщо файл відсутній, створюємо його

    def update_slider_position(self):
        """Оновлює положення повзунка відповідно до поточної гучності"""
        self.slider_x = self.slider_x_start + int(self.volume * self.slider_width)

    def increase_volume(self):
        """Збільшує гучність, зберігає зміни та оновлює звук"""
        self.volume = min(1.0, self.volume + 0.1)
        self.update_slider_position()
        self.save_settings()  # Зберігаємо зміни
        if self.sound_loaded:
            pygame.mixer.music.set_volume(self.volume)

    def decrease_volume(self):
        """Зменшує гучність, зберігає зміни та оновлює звук"""
        self.volume = max(0.0, self.volume - 0.1)
        self.update_slider_position()
        self.save_settings()  # Зберігаємо зміни
        if self.sound_loaded:
            pygame.mixer.music.set_volume(self.volume)

    def get_volume(self):
        """Повертає поточний рівень гучності"""
        return self.volume

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

    def settings_menu(self, screen, font, draw_text_with_outline, main_menu):
        # Ініціалізація кнопок для меню налаштувань
        audio_button = ImageButton(self.width / 2 - (252 / 2), 400, 252, 74, "", "Assets/Buttons/audio_button.png",
                                   "Assets/Buttons/audio_button_hover.png", "")
        video_button = ImageButton(self.width / 2 - (252 / 2), 500, 252, 74, "", "Assets/Buttons/video_button.png",
                                   "Assets/Buttons/video_button_hover.png", "")
        back_button = ImageButton(self.width / 2 - (252 / 2), 600, 252, 74, "", "Assets/Buttons/exit_button.png",
                                  "Assets/Buttons/exit_button_hover.png", "")

        running = True
        while running:
            # Відтворення фонового відео, якщо є
            if self.cap:
                ret, frame = self.cap.read()
                if not ret:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.width, self.height))
                frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                screen.blit(frame_surface, (0, 0))

            # Відображення заголовку "Settings" з обведенням
            draw_text_with_outline("Settings", font, (255, 255, 255), (0, 0, 0), self.width / 2, 330)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Перехід до меню аудіо налаштувань
                    if audio_button.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        self.audio_settings(screen, font, draw_text_with_outline, main_menu)
                    # Вихід з меню налаштувань
                    if back_button.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        running = False
                        return

                # Обробка подій для кожної кнопки
                for btn in [audio_button, video_button, back_button]:
                    btn.handle_event(event)
                    if event.type == pygame.MOUSEBUTTONDOWN and btn.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()  # Відтворюємо звук при натисканні

            # Перевірка наведення миші та відображення кнопок
            for btn in [audio_button, video_button, back_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

            pygame.display.flip()

    def settings_menu(self, screen, font, draw_text_with_outline, main_menu):
        # Ініціалізація кнопок для меню налаштувань
        audio_button = ImageButton(self.width / 2 - (252 / 2), 400, 252, 74, "", "Assets/Buttons/audio_button.png",
                                   "Assets/Buttons/audio_button_hover.png", "")
        video_button = ImageButton(self.width / 2 - (252 / 2), 500, 252, 74, "", "Assets/Buttons/video_button.png",
                                   "Assets/Buttons/video_button_hover.png", "")
        back_button = ImageButton(self.width / 2 - (252 / 2), 600, 252, 74, "", "Assets/Buttons/exit_button.png",
                                  "Assets/Buttons/exit_button_hover.png", "")

        running = True
        while running:
            # Відтворення фонового відео, якщо є
            if self.cap:
                ret, frame = self.cap.read()
                if not ret:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.width, self.height))
                frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                screen.blit(frame_surface, (0, 0))

            # Відображення заголовку "Settings" з обведенням
            draw_text_with_outline("Settings", font, (255, 255, 255), (0, 0, 0), self.width / 2, 330)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Перехід до меню аудіо налаштувань
                    if audio_button.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        self.audio_settings(screen, font, draw_text_with_outline, main_menu)
                    # Вихід з меню налаштувань
                    if back_button.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        running = False
                        return

                # Обробка подій для кожної кнопки
                for btn in [audio_button, video_button, back_button]:
                    btn.handle_event(event)
                    if event.type == pygame.MOUSEBUTTONDOWN and btn.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()  # Відтворюємо звук при натисканні

            # Перевірка наведення миші та відображення кнопок
            for btn in [audio_button, video_button, back_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

            pygame.display.flip()

    def audio_settings(self, screen, font, draw_text_with_outline, main_menu):
        # Ініціалізація кнопок для меню аудіо налаштувань
        back_button = ImageButton(self.width / 2 - (252 / 2), 600, 252, 74, "", "Assets/Buttons/back_button.png",
                                  "Assets/Buttons/back_button_hover.png", "")
        mute_button = ImageButton(self.width / 2 - (252 / 2), 500, 252, 74, "", "Assets/Buttons/mute_button.png",
                                  "Assets/Buttons/mute_button_hover.png", "")
        save_button = ImageButton(self.width / 2 - (252 / 2), 400, 252, 74, "", "Assets/Buttons/save_button.png",
                                  "Assets/Buttons/save_button_hover.png", "")

        running = True
        settings_changed = False  # Прапорець для відстеження змін у налаштуваннях
        previous_volume = self.volume  # Зберігаємо попереднє значення гучності перед редагуванням
        self.settings_saved = False  # Скидаємо статус збереження при вході в меню

        while running:
            # Відтворення фонового відео, якщо є
            if self.cap:
                ret, frame = self.cap.read()
                if not ret:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.width, self.height))
                frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                screen.blit(frame_surface, (0, 0))
            else:
                screen.fill((0, 0, 0))

            # Відображення заголовку "Audio Settings" з обведенням
            draw_text_with_outline("Audio Settings", font, (255, 255, 255), (0, 0, 0), self.width / 2, 180)

            # Відображення смуги гучності
            pygame.draw.rect(screen, (255, 255, 255), (self.slider_x_start, 270, self.slider_width, 8))
            pygame.draw.rect(screen, (0, 255, 0), (self.slider_x_start, 270, int(self.volume * self.slider_width), 8))
            pygame.draw.circle(screen, (255, 255, 255), (self.slider_x, 274), 10)

            # Відображення поточного рівня гучності у відсотках
            draw_text_with_outline(f"Volume: {int(self.volume * 100)}%", font, (255, 255, 255), (0, 0, 0),
                                   self.width / 2, 330)

            # Плашка для відображення статусу збереження налаштувань
            if self.settings_saved and not settings_changed:
                draw_text_with_outline("Налаштування збережено!", font, (0, 255, 0), (0, 0, 0), self.width / 2, 730)
            elif settings_changed:
                draw_text_with_outline("Налаштування не збережено!", font, (255, 0, 0), (0, 0, 0), self.width / 2, 730)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Якщо виходимо без збереження, повертаємо попереднє значення гучності
                        if settings_changed and not self.settings_saved:
                            self.volume = previous_volume
                            self.update_slider_position()
                            if self.sound_loaded:
                                pygame.mixer.music.set_volume(self.volume)
                        running = False
                        return
                    elif event.key == pygame.K_m:  # Перемикання звуку клавішею M
                        if self.volume > 0.0:
                            self.sound_enabled = False
                            self.volume = 0.0
                            self.slider_x = self.slider_x_start
                            if self.sound_loaded:
                                pygame.mixer.music.set_volume(0.0)
                            settings_changed = True  # Позначаємо, що налаштування змінилися
                            self.settings_saved = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Початок перетягування повзунка
                    if abs(event.pos[0] - self.slider_x) <= 10 and 265 <= event.pos[1] <= 285:
                        self.slider_dragging = True
                    # Клік по кнопці "Mute"
                    elif mute_button.rect.collidepoint(event.pos):
                        if self.volume > 0.0:
                            self.sound_enabled = False
                            self.volume = 0.0
                            self.slider_x = self.slider_x_start
                            if self.sound_loaded:
                                pygame.mixer.music.set_volume(0.0)
                            settings_changed = True  # Позначаємо зміну
                            self.settings_saved = False
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                    # Клік по кнопці "Back"
                    elif back_button.rect.collidepoint(event.pos):
                        # Якщо виходимо без збереження, повертаємо попереднє значення гучності
                        if settings_changed and not self.settings_saved:
                            self.volume = previous_volume
                            self.update_slider_position()
                            if self.sound_loaded:
                                pygame.mixer.music.set_volume(self.volume)
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        running = False
                        return
                    # Клік по кнопці "Save"
                    elif save_button.rect.collidepoint(event.pos):
                        self.save_settings()
                        previous_volume = self.volume  # Оновлюємо попереднє значення після збереження
                        settings_changed = False  # Скидаємо прапорець змін після збереження
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        print("✅ Налаштування збережено!")

                # Кінець перетягування повзунка
                if event.type == pygame.MOUSEBUTTONUP:
                    self.slider_dragging = False

                # Оновлення позиції повзунка при перетягуванні
                if event.type == pygame.MOUSEMOTION and self.slider_dragging:
                    self.slider_x = max(self.slider_x_start, min(event.pos[0], self.slider_x_start + self.slider_width))
                    self.volume = (self.slider_x - self.slider_x_start) / self.slider_width
                    if self.sound_loaded:
                        pygame.mixer.music.set_volume(self.volume)
                    settings_changed = True  # Позначаємо зміну при русі повзунка
                    self.settings_saved = False

                # Обробка подій для кнопок
                back_button.handle_event(event)
                mute_button.handle_event(event)
                save_button.handle_event(event)

            # Перевірка наведення миші та відображення кнопок
            back_button.check_hover(pygame.mouse.get_pos())
            back_button.draw(screen)
            mute_button.check_hover(pygame.mouse.get_pos())
            mute_button.draw(screen)
            save_button.check_hover(pygame.mouse.get_pos())
            save_button.draw(screen)

            pygame.display.flip()
