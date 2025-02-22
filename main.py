import pygame
import sys
from Button import ImageButton
import cv2
from Game import Game
from Settings import Settings

pygame.init()
pygame.font.init()
info = pygame.display.Info()

# Сначала инициализируем cap, чтобы он был доступен
video_path = "Assets/Background/lvl1.mp4"
cap = cv2.VideoCapture(video_path)

# Теперь инициализируем settings с cap
settings = Settings(info.current_w, info.current_h, cap)  # Инициализируем настройки с текущим разрешением монитора

# Инициализируем экран в зависимости от полноэкранного режима
if settings.fullscreen:
    screen = pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((settings.width, settings.height), pygame.RESIZABLE)

my_font = pygame.font.SysFont('Comic Sans MS', 30)
font = pygame.font.SysFont('Comic Sans MS', 72)

pygame.display.set_caption("Duck Hunt")

# Инициализация кнопок с учетом текущего разрешения
start_button = ImageButton((settings.width - 252) / 2, settings.height * 0.35, 252, 74, "", "Assets/Buttons/new_game_button.png",
                          "Assets/Buttons/new_game_button_hover.png", "Assets/Sounds/click.mp3", settings)
settings_button = ImageButton((settings.width - 252) / 2, settings.height * 0.45, 252, 74, "", "Assets/Buttons/settings_button.png",
                             "Assets/Buttons/settings_button_hover.png", "Assets/Sounds/click.mp3", settings)
exit_button = ImageButton((settings.width - 252) / 2, settings.height * 0.55, 252, 74, "", "Assets/Buttons/exit_button.png",
                         "Assets/Buttons/exit_button_hover.png", "Assets/Sounds/click.mp3", settings)

def draw_text_with_outline(text, font, text_color, outline_color, x, y):
    text_surface = font.render(text, True, text_color)
    text_outline = font.render(text, True, outline_color)

    text_rect = text_surface.get_rect(center=(x, y))

    screen.blit(text_outline, text_rect.move(2, 2))
    screen.blit(text_outline, text_rect.move(-2, -2))
    screen.blit(text_outline, text_rect.move(2, -2))
    screen.blit(text_outline, text_rect.move(-2, 2))

    screen.blit(text_surface, text_rect)

def main_menu():
    global screen, cap, start_button, settings_button, exit_button
    running = True
    while running:
        try:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            # Масштабируем видео под текущее разрешение
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (settings.width, settings.height), interpolation=cv2.INTER_AREA)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame_surface, (0, 0))
        except Exception as e:
            print(f"Ошибка при обработке видео в главном меню: {e}")
            screen.fill((0, 0, 0))

        draw_text_with_outline("Duck Hunt", font, (255, 255, 255), (0, 0, 0), settings.width / 2, settings.height * 0.2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
            if event.type == pygame.USEREVENT:
                if event.button == start_button:
                    select_level()
                elif event.button == settings_button:
                    screen = settings.settings_menu(screen, font, draw_text_with_outline, main_menu)
                    if screen:
                        settings.width, settings.height = screen.get_width(), screen.get_height()
                        # Позиционируем кнопки пропорционально новому размеру
                        start_button = ImageButton((settings.width - 252) / 2, settings.height * 0.35, 252, 74, "", "Assets/Buttons/new_game_button.png",
                                                  "Assets/Buttons/new_game_button_hover.png", "Assets/Sounds/click.mp3", settings)
                        settings_button = ImageButton((settings.width - 252) / 2, settings.height * 0.45, 252, 74, "", "Assets/Buttons/settings_button.png",
                                                     "Assets/Buttons/settings_button_hover.png", "Assets/Sounds/click.mp3", settings)
                        exit_button = ImageButton((settings.width - 252) / 2, settings.height * 0.55, 252, 74, "", "Assets/Buttons/exit_button.png",
                                                 "Assets/Buttons/exit_button_hover.png", "Assets/Sounds/click.mp3", settings)
                elif event.button == exit_button:
                    running = False
                    break

            for btn in [start_button, settings_button, exit_button]:
                btn.handle_event(event)

        for btn in [start_button, settings_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

    cap.release()
    pygame.quit()
    sys.exit()

def select_level():
    global screen, cap
    running = True
    while running:
        try:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            # Масштабируем видео под текущее разрешение
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (settings.width, settings.height), interpolation=cv2.INTER_AREA)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame_surface, (0, 0))
        except Exception as e:
            print(f"Ошибка при обработке видео в выборе уровня: {e}")
            screen.fill((0, 0, 0))

        draw_text_with_outline("Select level", font, (255, 255, 255), (0, 0, 0), settings.width / 2, settings.height * 0.2)

        # Инициализация кнопок с учетом текущего разрешения
        Lbutton1 = ImageButton((settings.width - 80) / 2 - 140, settings.height * 0.35, 80, 74, "", "Assets/Buttons/level_but_1.png",
                               "Assets/Buttons/level_but_hover_1.png", "Assets/Sounds/click.mp3", settings)
        Lbutton2 = ImageButton((settings.width - 80) / 2 - (70 / 2), settings.height * 0.35, 80, 74, "", "Assets/Buttons/level_but_2.png",
                               "Assets/Buttons/level_but_hover_2.png", "Assets/Sounds/click.mp3", settings)
        Lbutton3 = ImageButton((settings.width - 80) / 2 + 70, settings.height * 0.35, 80, 74, "", "Assets/Buttons/level_but_3.png",
                               "Assets/Buttons/level_but_hover_3.png", "Assets/Sounds/click.mp3", settings)
        Lbutton4 = ImageButton((settings.width - 80) / 2 - 140, settings.height * 0.45, 80, 74, "", "Assets/Buttons/level_but_4.png",
                               "Assets/Buttons/level_but_hover_4.png", "Assets/Sounds/click.mp3", settings)
        Lbutton5 = ImageButton((settings.width - 80) / 2 - (70 / 2), settings.height * 0.45, 80, 74, "", "Assets/Buttons/level_but_5.png",
                               "Assets/Buttons/level_but_hover_5.png", "Assets/Sounds/click.mp3", settings)
        Lbutton6 = ImageButton((settings.width - 80) / 2 + 70, settings.height * 0.45, 80, 74, "", "Assets/Buttons/level_but_6.png",
                               "Assets/Buttons/level_but_hover_6.png", "Assets/Sounds/click.mp3", settings)
        Lbutton7 = ImageButton((settings.width - 80) / 2 - 140, settings.height * 0.55, 80, 74, "", "Assets/Buttons/level_but_7.png",
                               "Assets/Buttons/level_but_hover_7.png", "Assets/Sounds/click.mp3", settings)
        Lbutton8 = ImageButton((settings.width - 80) / 2 - (70 / 2), settings.height * 0.55, 80, 74, "", "Assets/Buttons/level_but_8.png",
                               "Assets/Buttons/level_but_hover_8.png", "Assets/Sounds/click.mp3", settings)
        Lbutton9 = ImageButton((settings.width - 80) / 2 + 70, settings.height * 0.55, 80, 74, "", "Assets/Buttons/level_but_9.png",
                               "Assets/Buttons/level_but_hover_9.png", "Assets/Sounds/click.mp3", settings)
        back_button = ImageButton((settings.width - 252) / 2, settings.height * 0.65, 252, 74, "", "Assets/Buttons/back_button.png",
                                  "Assets/Buttons/back_button_hover.png", "Assets/Sounds/click.mp3", settings)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                cap.release()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
            if event.type == pygame.USEREVENT:
                if event.button == Lbutton1:
                    levelone = Game()
                    levelone.start_level()
                elif event.button == back_button:
                    running = False
                    break

            for btn in [Lbutton1, Lbutton2, Lbutton3, Lbutton4, Lbutton5, Lbutton6, Lbutton7, Lbutton8, Lbutton9, back_button]:
                btn.handle_event(event)

        for btn in [Lbutton1, Lbutton2, Lbutton3, Lbutton4, Lbutton5, Lbutton6, Lbutton7, Lbutton8, Lbutton9, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

def main():
    main_menu()

if __name__ == "__main__":
    main()