import pygame
import sys
import cv2
from Button import ImageButton
from Game import Game

pygame.init()
pygame.font.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))

my_font = pygame.font.SysFont('Comic Sans MS', 30)
font = pygame.font.SysFont('Comic Sans MS', 72)

pygame.display.set_caption("Duck Hunt")

video_path = "Assets/Background/lvl1.mp4"
cap = cv2.VideoCapture(video_path)

# Кнопки головного меню
start_button = ImageButton(WIDTH / 2 - 126, 400, 252, 74, "",
                           "Assets/Buttons/new_game_button.png",
                           "Assets/Buttons/new_game_button_hover.png",
                           "Assets/Sounds/click.mp3")

settings_button = ImageButton(WIDTH / 2 - 126, 500, 252, 74, "",
                              "Assets/Buttons/settings_button.png",
                              "Assets/Buttons/settings_button_hover.png",
                              "Assets/Sounds/click.mp3")

exit_button = ImageButton(WIDTH / 2 - 126, 600, 252, 74, "",
                          "Assets/Buttons/exit_button.png",
                          "Assets/Buttons/exit_button_hover.png",
                          "Assets/Sounds/click.mp3")

def draw_text_with_outline(text, font, text_color, outline_color, x, y):
    text_surface = font.render(text, True, text_color)
    text_outline = font.render(text, True, outline_color)
    text_rect = text_surface.get_rect(center=(x, y))

    for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
        screen.blit(text_outline, text_rect.move(*offset))

    screen.blit(text_surface, text_rect)

def fade_screen():
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 256, 10):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)

def main_menu():
    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

        draw_text_with_outline("Duck Hunt", font, (255, 255, 255), (0, 0, 0), WIDTH / 2, 330)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.button == start_button:
                    fade_screen()
                    select_level()
                if event.button == settings_button:
                    fade_screen()
                    settings_menu()
                if event.button == exit_button:
                    running = False
                    pygame.quit()
                    sys.exit()

            for btn in [start_button, settings_button, exit_button]:
                btn.handle_event(event)

        for btn in [start_button, settings_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

    cap.release()
    pygame.quit()

def select_level():
    level_buttons = []
    positions = [(WIDTH / 2 - 140, 400), (WIDTH / 2 - 35, 400), (WIDTH / 2 + 70, 400),
                 (WIDTH / 2 - 140, 500), (WIDTH / 2 - 35, 500), (WIDTH / 2 + 70, 500),
                 (WIDTH / 2 - 140, 600), (WIDTH / 2 - 35, 600), (WIDTH / 2 + 70, 600)]

    for i, (x, y) in enumerate(positions):
        level_buttons.append(
            ImageButton(x, y, 80, 74, "",
                        f"Assets/Buttons/level_but_{i+1}.png",
                        f"Assets/Buttons/level_but_hover_{i+1}.png",
                        "Assets/Sounds/click.mp3")
        )

    back_button = ImageButton(WIDTH / 2 - 126, 700, 252, 74, "",
                              "Assets/Buttons/back_button.png",
                              "Assets/Buttons/back_button_hover.png",
                              "Assets/Sounds/click.mp3")

    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

        draw_text_with_outline("Select Level", font, (255, 255, 255), (0, 0, 0), WIDTH / 2, 330)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                fade_screen()
                main_menu()
            if event.type == pygame.USEREVENT:
                if event.button == back_button:
                    fade_screen()
                    main_menu()

                # Додаємо обробку кнопки першого рівня
                if event.button == level_buttons[0]:  # Перевіряємо, чи натиснута кнопка першого рівня
                    fade_screen()
                    levelone = Game()
                    levelone.start_level()

            for btn in level_buttons + [back_button]:
                btn.handle_event(event)

        for btn in level_buttons + [back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

    cap.release()
    pygame.quit()

def settings_menu():
    #buttons init
    audio_button = ImageButton(WIDTH / 2 - (252 / 2), 400, 252, 74, "", "Assets/Buttons/audio_button.png","Assets/Buttons/audio_button_hover.png", "Assets/Sounds/click.mp3")
    video_button = ImageButton(WIDTH / 2 - (252 / 2), 500, 252, 74, "","Assets/Buttons/video_button.png", "Assets/Buttons/video_button_hover.png","Assets/Sounds/click.mp3")
    back_button = ImageButton(WIDTH / 2 - (252 / 2), 600, 252, 74, "", "Assets/Buttons/exit_button.png","Assets/Buttons/exit_button_hover.png", "Assets/Sounds/click.mp3")

    running = True
    while running:

        # video bg will be swapped later
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1920, 1080))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface,  (0, 0))

        #Duck hunt menu banner
        draw_text_with_outline("Settings", font, (255, 255, 255), (0, 0, 0), WIDTH / 2, 330)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            #exit by ESC in menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            #back button to main menu
            if event.type == pygame.USEREVENT and event.button == back_button:
                main_menu()

            #click handler
            for btn in [audio_button, video_button, back_button]:
                btn.handle_event(event)

        #draw and check hover for buttons
        for btn in [audio_button, video_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

    #release video data
    cap.release()
    pygame.quit()

def main():
    main_menu()

if __name__ == "__main__":
    main()
