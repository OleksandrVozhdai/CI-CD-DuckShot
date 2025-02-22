import pygame
import sys
from Button import ImageButton
import cv2
from Game import Game
from Settings import Settings

pygame.init()
pygame.font.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h  # Автоматически подстраиваемся под точное разрешение монитора
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Запускаем в полноэкранном режиме

my_font = pygame.font.SysFont('Comic Sans MS', 30)
font = pygame.font.SysFont('Comic Sans MS', 72)

pygame.display.set_caption("Duck Hunt")

video_path = "Assets/Background/lvl1.mp4"
cap = cv2.VideoCapture(video_path)

settings = Settings(WIDTH, HEIGHT, cap)

# Ініціалізація кнопок
start_button = ImageButton(WIDTH / 2 - (252 / 2), HEIGHT * 0.35, 252, 74, "", "Assets/Buttons/new_game_button.png",
                          "Assets/Buttons/new_game_button_hover.png", "Assets/Sounds/click.mp3", settings)  # Подняты на 20% вверх (0.55 -> 0.35)
settings_button = ImageButton(WIDTH / 2 - (252 / 2), HEIGHT * 0.45, 252, 74, "", "Assets/Buttons/settings_button.png",
                             "Assets/Buttons/settings_button_hover.png", "Assets/Sounds/click.mp3", settings)  # Подняты на 20% вверх (0.65 -> 0.45)
exit_button = ImageButton(WIDTH / 2 - (252 / 2), HEIGHT * 0.55, 252, 74, "", "Assets/Buttons/exit_button.png",
                         "Assets/Buttons/exit_button_hover.png", "Assets/Sounds/click.mp3", settings)  # Подняты на 20% вверх (0.75 -> 0.55)

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
    global screen, cap, WIDTH, HEIGHT, start_button, settings_button, exit_button
    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        # Масштабируем видео, чтобы оно соответствовало размеру окна без чёрных полос
        aspect_ratio = frame.shape[1] / frame.shape[0]
        window_aspect = WIDTH / HEIGHT
        if aspect_ratio > window_aspect:
            new_width = WIDTH
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = HEIGHT
            new_width = int(new_height * aspect_ratio)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)  # Изменяем размер на точное разрешение окна
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))  # Заполняем весь экран без центрирования

        draw_text_with_outline("Duck Hunt", font, (255, 255, 255), (0, 0, 0), WIDTH / 2, HEIGHT * 0.2)  # Подняты на 20% вверх (0.4 -> 0.2)

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
                        WIDTH, HEIGHT = screen.get_width(), screen.get_height()
                        # Позиционируем кнопки пропорционально новому размеру
                        start_button = ImageButton(WIDTH / 2 - (252 / 2), HEIGHT * 0.35, 252, 74, "", "Assets/Buttons/new_game_button.png",
                                                  "Assets/Buttons/new_game_button_hover.png", "Assets/Sounds/click.mp3", settings)
                        settings_button = ImageButton(WIDTH / 2 - (252 / 2), HEIGHT * 0.45, 252, 74, "", "Assets/Buttons/settings_button.png",
                                                     "Assets/Buttons/settings_button_hover.png", "Assets/Sounds/click.mp3", settings)
                        exit_button = ImageButton(WIDTH / 2 - (252 / 2), HEIGHT * 0.55, 252, 74, "", "Assets/Buttons/exit_button.png",
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
    global screen, cap, WIDTH, HEIGHT
    Lbutton1 = ImageButton(WIDTH / 2 - 140, HEIGHT * 0.35, 80, 74, "", "Assets/Buttons/level_but_1.png",
                           "Assets/Buttons/level_but_hover_1.png", "Assets/Sounds/click.mp3", settings)  # Подняты на 20% вверх (0.55 -> 0.35)
    Lbutton2 = ImageButton(WIDTH / 2 - (70 / 2), HEIGHT * 0.35, 80, 74, "", "Assets/Buttons/level_but_2.png",
                           "Assets/Buttons/level_but_hover_2.png", "Assets/Sounds/click.mp3", settings)  # Подняты на 20% вверх (0.55 -> 0.35)
    Lbutton3 = ImageButton(WIDTH / 2 + 70, HEIGHT * 0.35, 80, 74, "", "Assets/Buttons/level_but_3.png",
                           "Assets/Buttons/level_but_hover_3.png", "Assets/Sounds/click.mp3", settings)  # Подняты на 20% вверх (0.55 -> 0.35)
    Lbutton4 = ImageButton(WIDTH / 2 - 140, HEIGHT * 0.45, 80, 74, "", "Assets/Buttons/level_but_4.png",
                           "Assets/Buttons/level_but_hover_4.png", "Assets/Sounds/click.mp3", settings)  # Подняты на 20% вверх (0.65 -> 0.45)
    Lbutton5 = ImageButton(WIDTH / 2 - (70 / 2), HEIGHT * 0.45, 80, 74, "", "Assets/Buttons/level_but_5.png",
                           "Assets/Buttons/level_but_hover_5.png", "Assets/Sounds/click.mp3", settings)  # Подняты на 20% вверх (0.65 -> 0.45)
    Lbutton6 = ImageButton(WIDTH / 2 + 70, HEIGHT * 0.45, 80, 74, "", "Assets/Buttons/level_but_6.png",
                           "Assets/Buttons/level_but_hover_6.png", "Assets/Sounds/click.mp3", settings)  # Подняты на 20% вверх (0.65 -> 0.45)
    Lbutton7 = ImageButton(WIDTH / 2 - 140, HEIGHT * 0.55, 80, 74, "", "Assets/Buttons/level_but_7.png",
                           "Assets/Buttons/level_but_hover_7.png", "Assets/Sounds/click.mp3", settings)  # Подняты на 20% вверх (0.75 -> 0.55)
    Lbutton8 = ImageButton(WIDTH / 2 - (70 / 2), HEIGHT * 0.55, 80, 74, "", "Assets/Buttons/level_but_8.png",
                           "Assets/Buttons/level_but_hover_8.png", "Assets/Sounds/click.mp3", settings)  # Подняты на 20% вверх (0.75 -> 0.55)
    Lbutton9 = ImageButton(WIDTH / 2 + 70, HEIGHT * 0.55, 80, 74, "", "Assets/Buttons/level_but_9.png",
                           "Assets/Buttons/level_but_hover_9.png", "Assets/Sounds/click.mp3", settings)  # Подняты на 20% вверх (0.75 -> 0.55)
    back_button = ImageButton(WIDTH / 2 - (243 / 2), HEIGHT * 0.65, 252, 74, "", "Assets/Buttons/back_button.png",
                              "Assets/Buttons/back_button_hover.png", "Assets/Sounds/click.mp3", settings)  # Подняты на 20% вверх (0.85 -> 0.65)

    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Масштабируем видео, чтобы оно соответствовало размеру окна без чёрных полос
        aspect_ratio = frame.shape[1] / frame.shape[0]
        window_aspect = WIDTH / HEIGHT
        if aspect_ratio > window_aspect:
            new_width = WIDTH
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = HEIGHT
            new_width = int(new_height * aspect_ratio)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)  # Изменяем размер на точное разрешение окна
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))  # Заполняем весь экран без центрирования

        draw_text_with_outline("Select level", font, (255, 255, 255), (0, 0, 0), WIDTH / 2, HEIGHT * 0.2)  # Подняты на 20% вверх (0.4 -> 0.2)

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