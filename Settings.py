import pygame
import cv2
from Button import ImageButton

class Settings:
    def __init__(self, width, height):
        self.volume = 0.5
        self.crosshair_size = 20
        self.difficulty = "Medium"
        self.brightness = 0.8
        self.width = width
        self.height = height
        self.fullscreen = False

    def increase_volume(self):
        self.volume = min(1.0, self.volume + 0.1)

    def decrease_volume(self):
        self.volume = max(0.0, self.volume - 0.1)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

    def increase_crosshair_size(self):
        self.crosshair_size = min(50, self.crosshair_size + 5)

    def decrease_crosshair_size(self):
        self.crosshair_size = max(10, self.crosshair_size - 5)

    def set_difficulty(self, level):
        if level in ["Easy", "Medium", "Hard"]:
            self.difficulty = level

    def increase_brightness(self):
        self.brightness = min(1.0, self.brightness + 0.1)

    def decrease_brightness(self):
        self.brightness = max(0.0, self.brightness - 0.1)

    def reset_settings(self):
        self.volume = 0.5
        self.crosshair_size = 20
        self.difficulty = "Medium"
        self.brightness = 0.8

    def settings_menu(self, screen, font, cap, draw_text_with_outline, main_menu):
        audio_button = ImageButton(self.width / 2 - (252 / 2), 400, 252, 74, "", "Assets/Buttons/audio_button.png",
                                   "Assets/Buttons/audio_button_hover.png", "Assets/Sounds/click.mp3")
        video_button = ImageButton(self.width / 2 - (252 / 2), 500, 252, 74, "", "Assets/Buttons/video_button.png",
                                   "Assets/Buttons/video_button_hover.png", "Assets/Sounds/click.mp3")
        back_button = ImageButton(self.width / 2 - (252 / 2), 600, 252, 74, "", "Assets/Buttons/exit_button.png",
                                  "Assets/Buttons/exit_button_hover.png", "Assets/Sounds/click.mp3")

        running = True
        while running:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
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
                        return main_menu()

                if event.type == pygame.USEREVENT and event.button == back_button:
                    return main_menu()

                for btn in [audio_button, video_button, back_button]:
                    btn.handle_event(event)

            for btn in [audio_button, video_button, back_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

            pygame.display.flip()

        cap.release()
        pygame.quit()