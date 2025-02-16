import os
import pygame
import cv2
from Button import ImageButton

# Инициализация микшера Pygame
pygame.mixer.init()

class Settings:
    def __init__(self, width, height, cap):
        self.volume = 0.5
        self.crosshair_size = 20
        self.difficulty = "Medium"
        self.brightness = 0.8
        self.width = width
        self.height = height
        self.fullscreen = False
        self.cap = cap
        self.sound_enabled = True

        # Укорачиваем полосу громкости и корректируем ползунок
        self.slider_width = self.width // 3  # Новая ширина полоски (короче)
        self.slider_x_start = (self.width - self.slider_width) // 2  # Центрирование полоски
        self.slider_x = self.slider_x_start + int(self.volume * self.slider_width)
        self.slider_dragging = False

        # Загружаем MP3 вместо WAV
        self.sound_path = "Assets/Sounds/click.mp3"
        self.sound_loaded = os.path.exists(self.sound_path)
        if self.sound_loaded:
            pygame.mixer.music.load(self.sound_path)
            pygame.mixer.music.set_volume(self.volume)  # Устанавливаем громкость
        else:
            print(f"⚠️ Файл {self.sound_path} не найден! Звук кнопок отключен.")

    def increase_volume(self):
        self.volume = min(1.0, self.volume + 0.1)
        self.slider_x = self.slider_x_start + int(self.volume * self.slider_width)
        if self.sound_loaded:
            pygame.mixer.music.set_volume(self.volume)  # Обновляем громкость кнопок

    def decrease_volume(self):
        self.volume = max(0.0, self.volume - 0.1)
        self.slider_x = self.slider_x_start + int(self.volume * self.slider_width)
        if self.sound_loaded:
            pygame.mixer.music.set_volume(self.volume)  # Обновляем громкость кнопок

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

    def settings_menu(self, screen, font, draw_text_with_outline, main_menu):
        audio_button = ImageButton(self.width / 2 - (252 / 2), 400, 252, 74, "", "Assets/Buttons/audio_button.png",
                                   "Assets/Buttons/audio_button_hover.png", "")
        video_button = ImageButton(self.width / 2 - (252 / 2), 500, 252, 74, "", "Assets/Buttons/video_button.png",
                                   "Assets/Buttons/video_button_hover.png", "")
        back_button = ImageButton(self.width / 2 - (252 / 2), 600, 252, 74, "", "Assets/Buttons/exit_button.png",
                                  "Assets/Buttons/exit_button_hover.png", "")

        running = True
        while running:
            if self.cap:
                ret, frame = self.cap.read()
                if not ret:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.width, self.height))
                frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                screen.blit(frame_surface, (0, 0))

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
                    if audio_button.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        self.audio_settings(screen, font, draw_text_with_outline, main_menu)
                    if back_button.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        running = False
                        return

                for btn in [audio_button, video_button, back_button]:
                    btn.handle_event(event)
                    if event.type == pygame.MOUSEBUTTONDOWN and btn.rect.collidepoint(event.pos):
                        if self.sound_loaded:
                            pygame.mixer.music.play()  # Воспроизводим звук при клике

            for btn in [audio_button, video_button, back_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

            pygame.display.flip()

    def audio_settings(self, screen, font, draw_text_with_outline, main_menu):
        back_button = ImageButton(self.width / 2 - (252 / 2), 600, 252, 74, "", "Assets/Buttons/back_button.png",
                                  "Assets/Buttons/back_button_hover.png", "")
        mute_button = ImageButton(self.width / 2 - (252 / 2), 500, 252, 74, "", "Assets/Buttons/mute_button.png",
                                  "Assets/Buttons/mute_button_hover.png", "")
        running = True

        while running:
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

            draw_text_with_outline("Audio Settings", font, (255, 255, 255), (0, 0, 0), self.width / 2, 180)

            # Отрисовка полосы громкости с новыми границами
            pygame.draw.rect(screen, (255, 255, 255), (self.slider_x_start, 270, self.slider_width, 8))
            pygame.draw.rect(screen, (0, 255, 0), (self.slider_x_start, 270, int(self.volume * self.slider_width), 8))
            pygame.draw.circle(screen, (255, 255, 255), (self.slider_x, 274), 10)

            draw_text_with_outline(f"Volume: {int(self.volume * 100)}%", font, (255, 255, 255), (0, 0, 0),
                                   self.width / 2, 350)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        return
                    elif event.key == pygame.K_m:  # Переключение звука клавишей M
                        if self.volume > 0.0:
                            self.sound_enabled = False
                            self.volume = 0.0
                            self.slider_x = self.slider_x_start  # Переносим ползунок в 0%
                            if self.sound_loaded:
                                pygame.mixer.music.set_volume(0.0)  # Полное отключение звука кнопок

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if abs(event.pos[0] - self.slider_x) <= 10 and 265 <= event.pos[1] <= 285:
                        self.slider_dragging = True
                    elif mute_button.rect.collidepoint(event.pos):  # Клик по кнопке "Mute"
                        if self.volume > 0.0:  # Если звук есть, то выключаем
                            self.sound_enabled = False
                            self.volume = 0.0
                            self.slider_x = self.slider_x_start  # Переносим ползунок в 0%
                            if self.sound_loaded:
                                pygame.mixer.music.set_volume(0.0)  # Полное отключение звука кнопок
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                    elif back_button.rect.collidepoint(event.pos):  # Клик по кнопке "Back"
                        if self.sound_loaded:
                            pygame.mixer.music.play()
                        running = False
                        return

                if event.type == pygame.MOUSEBUTTONUP:
                    self.slider_dragging = False

                if event.type == pygame.MOUSEMOTION and self.slider_dragging:
                    self.slider_x = max(self.slider_x_start, min(event.pos[0], self.slider_x_start + self.slider_width))
                    self.volume = (self.slider_x - self.slider_x_start) / self.slider_width
                    if self.sound_loaded:
                        pygame.mixer.music.set_volume(self.volume)  # Обновляем громкость звука кнопок

                back_button.handle_event(event)
                mute_button.handle_event(event)

            back_button.check_hover(pygame.mouse.get_pos())
            back_button.draw(screen)
            mute_button.check_hover(pygame.mouse.get_pos())
            mute_button.draw(screen)

            pygame.display.flip()
