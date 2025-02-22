import os
import json
import pygame
import cv2
import sys
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
        self.fullscreen = False  # По умолчанию начинаем в оконном режиме
        self.cap = cap
        self.sound_enabled = True

        # Зменьшуємо довжину полоски гучності та коригуємо положення повзунка
        self.slider_width = self.width // 3  # Нова ширина полоски (коротша)
        self.slider_x_start = (self.width - self.slider_width) // 2  # Центруємо полоску
        self.slider_x = self.slider_x_start + int(self.volume * self.slider_width)
        self.slider_dragging = False

        # Завантажуємо налаштування гучності та роздільної здатності з файлу
        self.load_settings()

        # Оновлення положення повзунка після завантаження гучності
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
        """Зберігає поточні налаштування гучності, роздільної здатності та режиму у файл"""
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
        """Завантажує налаштування з файлу, якщо він існує. Якщо ні – створює новий файл"""
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r") as file:
                    data = json.load(file)
                    self.volume = data.get("volume", 0.5)
                    self.width = data.get("width", pygame.display.Info().current_w)
                    self.height = data.get("height", pygame.display.Info().current_h)
                    self.fullscreen = data.get("fullscreen", False)  # Убедимся, что по умолчанию False для оконного режима
                    print(f"🔄 Завантажено гучність: {self.volume * 100}%, роздільна здатність: {self.width}x{self.height}, Fullscreen: {self.fullscreen}")
            except json.JSONDecodeError:
                print("⚠️ Помилка завантаження налаштувань! Використовуються значення за замовчуванням.")
        else:
            print("⚠️ Файл налаштувань відсутній. Створюємо новий...")
            self.save_settings()  # Якщо файл відсутній, створюємо його

    def update_slider_position(self):
        """Оновлює положення повзунка відповідно до поточної гучності"""
        self.slider_width = self.width // 3
        self.slider_x_start = (self.width - self.slider_width) // 2
        self.slider_x = self.slider_x_start + int(self.volume * self.slider_width)

    def increase_volume(self):
        """Збільшує гучність, зберігає зміни та оновлює звук"""
        self.volume = min(1.0, self.volume + 0.1)
        self.update_slider_position()
        self.save_settings()  # Зберігаємо зміни
        if self.sound_loaded:
            pygame.mixer.music.set_volume(self.volume)

    def decrease_volume(self):
        """Зменьшує гучність, зберігає зміни та оновлює звук"""
        self.volume = max(0.0, self.volume - 0.1)
        self.update_slider_position()
        self.save_settings()  # Зберігаємо зміни
        if self.sound_loaded:
            pygame.mixer.music.set_volume(self.volume)

    def get_volume(self):
        """Повертає поточний рівень гучності"""
        return self.volume

    def settings_menu(self, screen, font, draw_text_with_outline, main_menu):
        # Ініціалізація кнопок для меню налаштувань, центрирование относительно текущего разрешения
        audio_button = ImageButton((self.width - 252) / 2, self.height * 0.35, 252, 74, "", "Assets/Buttons/audio_button.png",
                                   "Assets/Buttons/audio_button_hover.png", "")
        video_button = ImageButton((self.width - 252) / 2, self.height * 0.45, 252, 74, "", "Assets/Buttons/video_button.png",
                                   "Assets/Buttons/video_button_hover.png", "")
        back_button = ImageButton((self.width - 252) / 2, self.height * 0.55, 252, 74, "", "Assets/Buttons/exit_button.png",
                                  "Assets/Buttons/exit_button_hover.png", "")

        running = True
        while running:
            try:
                if self.cap:
                    ret, frame = self.cap.read()
                    if not ret:
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    # Масштабируем видео под текущее разрешение
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_AREA)
                    frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                    screen.blit(frame_surface, (0, 0))
            except Exception as e:
                print(f"Ошибка при обработке видео: {e}")
                screen.fill((0, 0, 0))

            draw_text_with_outline("Settings", font, (255, 255, 255), (0, 0, 0), self.width / 2, self.height * 0.2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        return screen
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if audio_button.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        screen = self.audio_settings(screen, font, draw_text_with_outline, main_menu)
                        # Обновляем размер экрана после возврата из подменю
                        if screen:
                            self.width, self.height = screen.get_width(), screen.get_height()
                            # Переинициализируем кнопки с учетом нового разрешения
                            audio_button = ImageButton((self.width - 252) / 2, self.height * 0.35, 252, 74, "", "Assets/Buttons/audio_button.png",
                                                       "Assets/Buttons/audio_button_hover.png", "")
                            video_button = ImageButton((self.width - 252) / 2, self.height * 0.45, 252, 74, "", "Assets/Buttons/video_button.png",
                                                       "Assets/Buttons/video_button_hover.png", "")
                            back_button = ImageButton((self.width - 252) / 2, self.height * 0.55, 252, 74, "", "Assets/Buttons/exit_button.png",
                                                      "Assets/Buttons/exit_button_hover.png", "")
                    elif video_button.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        screen = self.video_settings(screen, font, draw_text_with_outline, main_menu)
                        if screen:
                            self.width, self.height = screen.get_width(), screen.get_height()
                            # Переинициализируем кнопки с учетом нового разрешения
                            audio_button = ImageButton((self.width - 252) / 2, self.height * 0.35, 252, 74, "", "Assets/Buttons/audio_button.png",
                                                       "Assets/Buttons/audio_button_hover.png", "")
                            video_button = ImageButton((self.width - 252) / 2, self.height * 0.45, 252, 74, "", "Assets/Buttons/video_button.png",
                                                       "Assets/Buttons/video_button_hover.png", "")
                            back_button = ImageButton((self.width - 252) / 2, self.height * 0.55, 252, 74, "", "Assets/Buttons/exit_button.png",
                                                      "Assets/Buttons/exit_button_hover.png", "")
                    elif back_button.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        running = False
                        return screen

                for btn in [audio_button, video_button, back_button]:
                    btn.handle_event(event)
                    if event.type == pygame.MOUSEBUTTONDOWN and btn.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()

            # Центрируем кнопки по ширине и масштабируем по высоте
            audio_button.rect.topleft = ((self.width - 252) / 2, self.height * 0.35)
            video_button.rect.topleft = ((self.width - 252) / 2, self.height * 0.45)
            back_button.rect.topleft = ((self.width - 252) / 2, self.height * 0.55)

            for btn in [audio_button, video_button, back_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

            pygame.display.flip()

        return screen

    def audio_settings(self, screen, font, draw_text_with_outline, main_menu):
        # Оставляем порядок кнопок: Mute, Save, Back
        mute_button = ImageButton((self.width - 252) / 2, self.height * 0.35, 252, 74, "", "Assets/Buttons/mute_button.png",
                                  "Assets/Buttons/mute_button_hover.png", "")
        save_button = ImageButton((self.width - 252) / 2, self.height * 0.45, 252, 74, "", "Assets/Buttons/save_button.png",
                                  "Assets/Buttons/save_button_hover.png", "")
        back_button = ImageButton((self.width - 252) / 2, self.height * 0.55, 252, 74, "", "Assets/Buttons/back_button.png",
                                  "Assets/Buttons/back_button_hover.png", "")

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
                    # Масштабируем видео под текущее разрешение
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_AREA)
                    frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                    screen.blit(frame_surface, (0, 0))
            except Exception as e:
                print(f"Ошибка при обработке видео: {e}")
                screen.fill((0, 0, 0))

            # Устанавливаем новые позиции для 10% от верха и 10% от кнопок
            draw_text_with_outline("Audio Settings", font, (255, 255, 255), (0, 0, 0), self.width / 2, self.height * 0.1)
            pygame.draw.rect(screen, (255, 255, 255), (self.slider_x_start, self.height * 0.15, self.slider_width, 8))  # Подняли ползунок выше
            pygame.draw.rect(screen, (0, 255, 0), (self.slider_x_start, self.height * 0.15, int(self.volume * self.slider_width), 8))
            pygame.draw.circle(screen, (255, 255, 255), (self.slider_x, int(self.height * 0.15 + 4)), 10)
            draw_text_with_outline(f"Volume: {int(self.volume * 100)}%", font, (255, 255, 255), (0, 0, 0),
                                   self.width / 2, self.height * 0.2)  # Подняли текст выше
            if self.settings_saved and not settings_changed:
                draw_text_with_outline("Налаштування збережено!", font, (0, 255, 0), (0, 0, 0), self.width / 2, self.height * 0.7)
            elif settings_changed:
                draw_text_with_outline("Налаштування не збережено!", font, (255, 0, 0), (0, 0, 0), self.width / 2, self.height * 0.7)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if settings_changed and not self.settings_saved:
                            self.volume = previous_volume
                            self.update_slider_position()
                            if self.sound_loaded:
                                pygame.mixer.music.set_volume(self.volume)
                        running = False
                        return screen
                    elif event.key == pygame.K_m:
                        if self.volume > 0.0:
                            self.sound_enabled = False
                            self.volume = 0.0
                            self.slider_x = self.slider_x_start
                            if self.sound_loaded:
                                pygame.mixer.music.set_volume(0.0)
                            settings_changed = True
                            self.settings_saved = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if abs(event.pos[0] - self.slider_x) <= 10 and (self.height * 0.15 - 4) <= event.pos[1] <= (self.height * 0.15 + 12):  # Обновили высоту для ползунка
                        self.slider_dragging = True
                    elif mute_button.rect.collidepoint(event.pos):
                        if self.volume > 0.0:
                            self.sound_enabled = False
                            self.volume = 0.0
                            self.slider_x = self.slider_x_start
                            if self.sound_loaded:
                                pygame.mixer.music.set_volume(0.0)
                            settings_changed = True
                            self.settings_saved = False
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                    elif save_button.rect.collidepoint(event.pos):
                        self.save_settings()
                        previous_volume = self.volume
                        settings_changed = False
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        print("✅ Налаштування збережено!")
                    elif back_button.rect.collidepoint(event.pos):
                        if settings_changed and not self.settings_saved:
                            self.volume = previous_volume
                            self.update_slider_position()
                            if self.sound_loaded:
                                pygame.mixer.music.set_volume(self.volume)
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        running = False
                        return screen

                if event.type == pygame.MOUSEBUTTONUP:
                    self.slider_dragging = False

                if event.type == pygame.MOUSEMOTION and self.slider_dragging:
                    self.slider_x = max(self.slider_x_start, min(event.pos[0], self.slider_x_start + self.slider_width))
                    self.volume = (self.slider_x - self.slider_x_start) / self.slider_width
                    if self.sound_loaded:
                        pygame.mixer.music.set_volume(self.volume)
                    settings_changed = True
                    self.settings_saved = False

                if event.type == pygame.VIDEORESIZE:
                    if not self.fullscreen:  # Разрешить изменение размера только в оконном режиме
                        self.width, self.height = event.w, event.h
                        self.slider_width = self.width // 3
                        self.slider_x_start = (self.width - self.slider_width) // 2
                        self.update_slider_position()
                        screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                        # Переинициализация кнопок после изменения размера
                        mute_button = ImageButton((self.width - 252) / 2, self.height * 0.35, 252, 74, "", "Assets/Buttons/mute_button.png",
                                                  "Assets/Buttons/mute_button_hover.png", "")
                        save_button = ImageButton((self.width - 252) / 2, self.height * 0.45, 252, 74, "", "Assets/Buttons/save_button.png",
                                                  "Assets/Buttons/save_button_hover.png", "")
                        back_button = ImageButton((self.width - 252) / 2, self.height * 0.55, 252, 74, "", "Assets/Buttons/back_button.png",
                                                  "Assets/Buttons/back_button_hover.png", "")

                mute_button.handle_event(event)
                save_button.handle_event(event)
                back_button.handle_event(event)

            mute_button.check_hover(pygame.mouse.get_pos())
            mute_button.draw(screen)
            save_button.check_hover(pygame.mouse.get_pos())
            save_button.draw(screen)
            back_button.check_hover(pygame.mouse.get_pos())
            back_button.draw(screen)

            pygame.display.flip()

        return screen

    def video_settings(self, screen, font, draw_text_with_outline, main_menu):
        """Налаштування відео: изменение порядка кнопок и корректное масштабирование с кнопкой "Сохранить" """
        fullscreen_button = ImageButton((self.width - 252) / 2, self.height * 0.35, 252, 74, "",
                                        "Assets/Buttons/fullscreen_button.png",
                                        "Assets/Buttons/fullscreen_button_hover.png", "")  # Первая кнопка - Fullscreen
        resolution_button = ImageButton((self.width - 252) / 2, self.height * 0.45, 252, 74, "",
                                        "Assets/Buttons/resolution_button.png",
                                        "Assets/Buttons/resolution_button_hover.png", "")  # Вторая кнопка - Resolution
        save_button = ImageButton((self.width - 252) / 2, self.height * 0.55, 252, 74, "", "Assets/Buttons/save_button.png",
                                  "Assets/Buttons/save_button_hover.png", "")  # Третья кнопка - Save
        back_button = ImageButton((self.width - 252) / 2, self.height * 0.65, 252, 74, "", "Assets/Buttons/back_button.png",
                                  "Assets/Buttons/back_button_hover.png", "")  # Четвертая кнопка - Back

        running = True
        while running:
            try:
                if self.cap:
                    ret, frame = self.cap.read()
                    if not ret:
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    # Масштабируем видео под текущее разрешение
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_AREA)
                    frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                    screen.blit(frame_surface, (0, 0))
            except Exception as e:
                print(f"Ошибка при обработке видео: {e}")
                screen.fill((0, 0, 0))

            # Выравниваем текст с одинаковым шрифтом и позицией
            draw_text_with_outline("Video Settings", font, (255, 255, 255), (0, 0, 0), self.width / 2, self.height * 0.1)
            draw_text_with_outline(f"Resolution: {self.width}x{self.height}", font, (255, 255, 255), (0, 0, 0), self.width / 2, self.height * 0.2)
            fullscreen_text = "Fullscreen: ON" if self.fullscreen else "Fullscreen: OFF"
            draw_text_with_outline(fullscreen_text, font, (255, 255, 255), (0, 0, 0), self.width / 2, self.height * 0.3)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        return screen
                    elif event.key == pygame.K_F11:  # Горячая клавиша для переключения в полноэкранный режим
                        screen = self.toggle_fullscreen(screen)
                        if screen:
                            self.width, self.height = screen.get_width(), screen.get_height()
                            # Переинициализация кнопок после изменения режима
                            fullscreen_button = ImageButton((self.width - 252) / 2, self.height * 0.35, 252, 74, "",
                                                            "Assets/Buttons/fullscreen_button.png",
                                                            "Assets/Buttons/fullscreen_button_hover.png", "")
                            resolution_button = ImageButton((self.width - 252) / 2, self.height * 0.45, 252, 74, "",
                                                            "Assets/Buttons/resolution_button.png",
                                                            "Assets/Buttons/resolution_button_hover.png", "")
                            save_button = ImageButton((self.width - 252) / 2, self.height * 0.55, 252, 74, "",
                                                      "Assets/Buttons/save_button.png",
                                                      "Assets/Buttons/save_button_hover.png", "")
                            back_button = ImageButton((self.width - 252) / 2, self.height * 0.65, 252, 74, "",
                                                      "Assets/Buttons/back_button.png",
                                                      "Assets/Buttons/back_button_hover.png", "")
                if event.type == pygame.VIDEORESIZE:
                    if not self.fullscreen:  # Разрешить изменение размера только в оконном режиме
                        self.width, self.height = event.w, event.h
                        self.slider_width = self.width // 3
                        self.slider_x_start = (self.width - self.slider_width) // 2
                        self.update_slider_position()
                        screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                        # Переинициализация кнопок после изменения размера
                        fullscreen_button = ImageButton((self.width - 252) / 2, self.height * 0.35, 252, 74, "",
                                                        "Assets/Buttons/fullscreen_button.png",
                                                        "Assets/Buttons/fullscreen_button_hover.png", "")
                        resolution_button = ImageButton((self.width - 252) / 2, self.height * 0.45, 252, 74, "",
                                                        "Assets/Buttons/resolution_button.png",
                                                        "Assets/Buttons/resolution_button_hover.png", "")
                        save_button = ImageButton((self.width - 252) / 2, self.height * 0.55, 252, 74, "",
                                                  "Assets/Buttons/save_button.png",
                                                  "Assets/Buttons/save_button_hover.png", "")
                        back_button = ImageButton((self.width - 252) / 2, self.height * 0.65, 252, 74, "",
                                                  "Assets/Buttons/back_button.png",
                                                  "Assets/Buttons/back_button_hover.png", "")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resolution_button.rect.collidepoint(event.pos):  # Разрешение можно менять в обоих режимах
                        screen = self.change_resolution(screen)
                        if screen:
                            self.width, self.height = screen.get_width(), screen.get_height()
                            # Переинициализация кнопок после изменения разрешения
                            fullscreen_button = ImageButton((self.width - 252) / 2, self.height * 0.35, 252, 74, "",
                                                            "Assets/Buttons/fullscreen_button.png",
                                                            "Assets/Buttons/fullscreen_button_hover.png", "")
                            resolution_button = ImageButton((self.width - 252) / 2, self.height * 0.45, 252, 74, "",
                                                            "Assets/Buttons/resolution_button.png",
                                                            "Assets/Buttons/resolution_button_hover.png", "")
                            save_button = ImageButton((self.width - 252) / 2, self.height * 0.55, 252, 74, "",
                                                      "Assets/Buttons/save_button.png",
                                                      "Assets/Buttons/save_button_hover.png", "")
                            back_button = ImageButton((self.width - 252) / 2, self.height * 0.65, 252, 74, "",
                                                      "Assets/Buttons/back_button.png",
                                                      "Assets/Buttons/back_button_hover.png", "")
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                    elif fullscreen_button.rect.collidepoint(event.pos):
                        screen = self.toggle_fullscreen(screen)
                        if screen:
                            self.width, self.height = screen.get_width(), screen.get_height()
                            # Переинициализация кнопок после изменения режима
                            fullscreen_button = ImageButton((self.width - 252) / 2, self.height * 0.35, 252, 74, "",
                                                            "Assets/Buttons/fullscreen_button.png",
                                                            "Assets/Buttons/fullscreen_button_hover.png", "")
                            resolution_button = ImageButton((self.width - 252) / 2, self.height * 0.45, 252, 74, "",
                                                            "Assets/Buttons/resolution_button.png",
                                                            "Assets/Buttons/resolution_button_hover.png", "")
                            save_button = ImageButton((self.width - 252) / 2, self.height * 0.55, 252, 74, "",
                                                      "Assets/Buttons/save_button.png",
                                                      "Assets/Buttons/save_button_hover.png", "")
                            back_button = ImageButton((self.width - 252) / 2, self.height * 0.65, 252, 74, "",
                                                      "Assets/Buttons/back_button.png",
                                                      "Assets/Buttons/back_button_hover.png", "")
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                    elif save_button.rect.collidepoint(event.pos):
                        self.save_settings()
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        print("✅ Налаштування відео збережено!")
                    elif back_button.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        running = False
                        return screen

                for btn in [fullscreen_button, resolution_button, save_button, back_button]:
                    btn.handle_event(event)

            # Центрируем кнопки по ширине и масштабируем по высоте
            fullscreen_button.rect.topleft = ((self.width - 252) / 2, self.height * 0.35)
            resolution_button.rect.topleft = ((self.width - 252) / 2, self.height * 0.45)
            save_button.rect.topleft = ((self.width - 252) / 2, self.height * 0.55)
            back_button.rect.topleft = ((self.width - 252) / 2, self.height * 0.65)

            for btn in [fullscreen_button, resolution_button, save_button, back_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

            pygame.display.flip()

        return screen

    def toggle_fullscreen(self, screen):
        """Переключаємо між звичайним і повноэкранным режимом, изменяя разрешение монитора только в полноэкранном режиме"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            # В полноэкранном режиме устанавливаем указанное разрешение, изменяя разрешение монитора
            resolutions = [(3440, 1440), (2752, 1152), (1920, 1080), (1280, 720), (1024, 768)]
            if (self.width, self.height) in resolutions:
                screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            else:
                # Если указанное разрешение не в списке, используем максимальное разрешение монитора
                info = pygame.display.Info()
                self.width, self.height = info.current_w, info.current_h
                screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            # В оконном режиме устанавливаем указанное разрешение как размер окна, не меняя разрешение монитора
            screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            # Убедимся, что окно не превышает размер монитора
            info = pygame.display.Info()
            if self.width > info.current_w or self.height > info.current_h:
                self.width, self.height = min(self.width, info.current_w), min(self.height, info.current_h)
                screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.slider_width = self.width // 3
        self.slider_x_start = (self.width - self.slider_width) // 2
        self.update_slider_position()
        self.save_settings()  # Сохраняем изменения полноэкранного режима
        return screen

    def change_resolution(self, screen):
        """Змінюємо роздільну здатность в обоих режимах, изменяя разрешение монитора только в полноэкранном режиме"""
        resolutions = [(3440, 1440), (2752, 1152), (1920, 1080), (1280, 720), (1024, 768)]
        current_resolution = (self.width, self.height)
        index = resolutions.index(current_resolution) if current_resolution in resolutions else 0
        new_resolution = resolutions[(index + 1) % len(resolutions)]
        self.width, self.height = new_resolution
        self.slider_width = self.width // 3
        self.slider_x_start = (self.width - self.slider_width) // 2
        self.update_slider_position()
        if self.fullscreen:
            # В полноэкранном режиме устанавливаем указанное разрешение, изменяя разрешение монитора
            screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            # В оконном режиме устанавливаем указанное разрешение как размер окна, не меняя разрешение монитора
            screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            # Убедимся, что окно не превышает размер монитора
            info = pygame.display.Info()
            if self.width > info.current_w or self.height > info.current_h:
                self.width, self.height = min(self.width, info.current_w), min(self.height, info.current_h)
                screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.save_settings()  # Сохраняем новое разрешение
        print(f"🔄 Змінено роздільну здатність на: {new_resolution[0]}x{new_resolution[1]}")
        return screen