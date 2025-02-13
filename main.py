import pygame
import sys
from Button import ImageButton
import cv2
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

#buttons init
start_button = ImageButton(WIDTH / 2 - (252 / 2), 400, 252, 74, "", "Assets/Buttons/new_game_button.png","Assets/Buttons/new_game_button_hover.png", "Assets/Sounds/click.mp3")
settings_button = ImageButton(WIDTH / 2 - (252 / 2), 500, 252, 74, "", "Assets/Buttons/settings_button.png","Assets/Buttons/settings_button_hover.png", "Assets/Sounds/click.mp3")
exit_button = ImageButton(WIDTH / 2 - (252 / 2), 600, 252, 74, "", "Assets/Buttons/exit_button.png","Assets/Buttons/exit_button_hover.png", "Assets/Sounds/click.mp3")

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
    running = True
    while running:

        # video bg will be swapped later
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

        #Duck hunt menu banner
        draw_text_with_outline("Duck Hunt", font, (255, 255, 255), (0, 0, 0), WIDTH / 2, 330)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            #exit by ESC in menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()

            #start level button
            if event.type == pygame.USEREVENT and event.button == start_button:
                select_level()

            #settings button
            if event.type == pygame.USEREVENT and event.button == settings_button:
                settings_menu()

            #exit button
            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                pygame.quit()
                sys.exit()

            #button event handler, checking for click
            for btn in [start_button, settings_button, exit_button]:
                btn.handle_event(event)

        #checking for hover and drawing buttons
        for btn in [start_button, settings_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

    #release video data
    cap.release()
    pygame.quit()

def select_level():
    Lbutton1 = ImageButton(WIDTH / 2 - 140, 400, 80, 74, "", "Assets/Buttons/level_but_1.png",
                               "Assets/Buttons/level_but_hover_1.png", "Assets/Sounds/click.mp3")
    Lbutton2 = ImageButton(WIDTH / 2 - (70 / 2), 400, 80, 74, "", "Assets/Buttons/level_but_2.png",
                                  "Assets/Buttons/level_but_hover_2.png", "Assets/Sounds/click.mp3")
    Lbutton3 = ImageButton(WIDTH / 2 + 70, 400, 80, 74, "", "Assets/Buttons/level_but_3.png",
                              "Assets/Buttons/level_but_hover_3.png", "Assets/Sounds/click.mp3")
    Lbutton4 = ImageButton(WIDTH / 2 - 140, 500, 80, 74, "", "Assets/Buttons/level_but_4.png",
                          "Assets/Buttons/level_but_hover_4.png", "Assets/Sounds/click.mp3")
    Lbutton5 = ImageButton(WIDTH / 2 - (70 / 2), 500, 80, 74, "", "Assets/Buttons/level_but_5.png",
                          "Assets/Buttons/level_but_hover_5.png", "Assets/Sounds/click.mp3")
    Lbutton6 = ImageButton(WIDTH / 2 + 70, 500, 80, 74, "", "Assets/Buttons/level_but_6.png",
                          "Assets/Buttons/level_but_hover_6.png", "Assets/Sounds/click.mp3")
    Lbutton7 = ImageButton(WIDTH / 2 - 140, 600, 80, 74, "", "Assets/Buttons/level_but_7.png",
                          "Assets/Buttons/level_but_hover_7.png", "Assets/Sounds/click.mp3")
    Lbutton8 = ImageButton(WIDTH / 2 - (70 / 2), 600, 80, 74, "", "Assets/Buttons/level_but_8.png",
                          "Assets/Buttons/level_but_hover_8.png", "Assets/Sounds/click.mp3")
    Lbutton9 = ImageButton(WIDTH / 2 + 70, 600, 80, 74, "", "Assets/Buttons/level_but_9.png",
                          "Assets/Buttons/level_but_hover_9.png", "Assets/Sounds/click.mp3")

    back_button = ImageButton(WIDTH / 2 - (243 / 2), 700, 252, 74, "", "Assets/Buttons/back_button.png",
                              "Assets/Buttons/back_button_hover.png", "Assets/Sounds/click.mp3")

    running = True
    while running:

        # video bg will be swapped later
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

        #Duck hunt menu banner
        draw_text_with_outline("Select level", font, (255, 255, 255), (0, 0, 0), WIDTH / 2, 330)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            #exit by ESC in menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            #start level1 button
            if event.type == pygame.USEREVENT and event.button == Lbutton1:
                levelone = Game()
                levelone.start_level()

            #back button
            if event.type == pygame.USEREVENT and event.button == back_button:
                main_menu()

            #button event handler, checking for click
            for btn in [Lbutton1, Lbutton2, Lbutton3, Lbutton4, Lbutton5, Lbutton6, Lbutton7, Lbutton8, Lbutton9, back_button]:
                btn.handle_event(event)

        #checking for hover and drawing buttons
        for btn in [Lbutton1, Lbutton2, Lbutton3, Lbutton4, Lbutton5, Lbutton6, Lbutton7, Lbutton8, Lbutton9, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

    #release video data
    cap.release()
    pygame.quit()

def settings_menu():
    #buttons init
    audio_button = ImageButton(WIDTH / 2 - (252 / 2), 400, 252, 74, "", "Assets/Buttons/audio_button.png", "Assets/Buttons/audio_button_hover.png", "Assets/Sounds/click.mp3")
    video_button = ImageButton(WIDTH / 2 - (252 / 2), 500, 252, 74, "","Assets/Buttons/video_button.png", "Assets/Buttons/video_button_hover.png", "Assets/Sounds/click.mp3")
    back_button = ImageButton(WIDTH / 2 - (252 / 2), 600, 252, 74, "", "Assets/Buttons/exit_button.png", "Assets/Buttons/exit_button_hover.png", "Assets/Sounds/click.mp3")

    running = True
    while running:
        # video bg will be swapped later
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT)) # use dynamic screen resolution
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface,  (0, 0))

        # Duck hunt menu banner
        draw_text_with_outline("Settings", font, (255, 255, 255), (0, 0, 0), WIDTH / 2, 330)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # exit by ESC in menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            # back button to main menu
            if event.type == pygame.USEREVENT and event.button == back_button:
                main_menu()

            # click handler
            for btn in [audio_button, video_button, back_button]:
                btn.handle_event(event)

        # draw and check hover for buttons
        for btn in [audio_button, video_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

    # release video data
    cap.release()
    pygame.quit()

def main():
    main_menu()

if __name__ == "__main__":
    main()