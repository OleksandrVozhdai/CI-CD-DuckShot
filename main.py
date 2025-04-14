import pygame
import sys
from Button import ImageButton
import cv2
from Game import Game
from Settings import Settings

pygame.init()
pygame.font.init()
info = pygame.display.Info()

# Initialize cap first so it is available
video_path = "Assets/Background/lvl1.mp4"
cap = cv2.VideoCapture(video_path)

# Limit video frame rate for optimization
cap.set(cv2.CAP_PROP_FPS, 60)  # Set 30 FPS for stability
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1000)   # Increase buffer for fast frame reading

# Now initialize settings with cap
settings = Settings(info.current_w, info.current_h, cap)  # Initialize settings with current screen resolution

# Initialize screen depending on fullscreen mode for the main menu
if settings.fullscreen:
    screen = pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((settings.width, settings.height), pygame.RESIZABLE)

my_font = pygame.font.SysFont('Comic Sans MS', 30)
font = pygame.font.SysFont('Comic Sans MS', 72)

pygame.display.set_caption("Duck Hunt")

# Initialize buttons with current resolution
start_button = ImageButton((settings.width - 252) / 2, settings.height * 0.35, 252, 74, "", "Assets/Buttons/new_game_button.png",
                          "Assets/Buttons/new_game_button_hover.png", "Assets/Sounds/click.mp3", settings)
settings_button = ImageButton((settings.width - 252) / 2, settings.height * 0.45, 252, 74, "", "Assets/Buttons/settings_button.png",
                             "Assets/Buttons/settings_button_hover.png", "Assets/Sounds/click.mp3", settings)
exit_button = ImageButton((settings.width - 252) / 2, settings.height * 0.55, 252, 74, "", "Assets/Buttons/exit_button.png",
                         "Assets/Buttons/exit_button_hover.png", "Assets/Sounds/click.mp3", settings)

def draw_text_with_outline(text, font, text_color, outline_color, x, y, surface):
    text_surface = font.render(text, True, text_color)
    text_outline = font.render(text, True, outline_color)

    text_rect = text_surface.get_rect(center=(x, y))

    surface.blit(text_outline, text_rect.move(2, 2))
    surface.blit(text_outline, text_rect.move(-2, -2))
    surface.blit(text_outline, text_rect.move(2, -2))
    surface.blit(text_outline, text_rect.move(-2, 2))

    surface.blit(text_surface, text_rect)

def fade_screen():
    fade_surface = pygame.Surface((settings.width, settings.height))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 256, 10):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

def main_menu():
    global screen, cap, start_button, settings_button, exit_button
    running = True
    clock = pygame.time.Clock()  # Add Clock for FPS management
    last_frame = None # Buffer for the last video frame

    while running:
        try:
            # Retry reading frame until successful (max 5 attempts)
            ret, frame = None, None
            attempts = 5
            while attempts > 0 and (not ret or frame is None):
                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                attempts -= 1
                if attempts == 0 and not ret:
                    raise Exception("Video download error")
            # Scale video to current resolution with optimization
            info = pygame.display.Info()
            max_width, max_height = min(settings.width, info.current_w), min(settings.height, info.current_h)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (max_width, max_height), interpolation=cv2.INTER_LINEAR)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            last_frame = frame_surface  # Save last frame
            screen.blit(frame_surface, (0, 0))
        except Exception as e:
            print(f"ОVideo download error (Menu): {e}")
            if last_frame:
                screen.blit(last_frame, (0, 0)) # Use last successful frame if error
            else:
                screen.fill((0, 0, 0))  # Black screen only if no buffer available

        draw_text_with_outline("Duck Hunt", font, (255, 255, 255), (0, 0, 0), settings.width / 2, settings.height * 0.2, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fade_screen()
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
            if event.type == pygame.USEREVENT:
                if event.button == start_button:
                    fade_screen()
                    # restore menu
                    select_level()
                elif event.button == settings_button:
                    fade_screen()
                    screen = settings.settings_menu(screen, font, lambda text, f, tc, oc, x, y: draw_text_with_outline(text, f, tc, oc, x, y, screen), main_menu)
                    if screen:
                        settings.width, settings.height = screen.get_width(), screen.get_height()

                        start_button = ImageButton((settings.width - 252) / 2, settings.height * 0.35, 252, 74, "",
                                                   "Assets/Buttons/new_game_button.png",
                                                  "Assets/Buttons/new_game_button_hover.png", "Assets/Sounds/click.mp3", settings)
                        settings_button = ImageButton((settings.width - 252) / 2, settings.height * 0.45, 252, 74, "",
                                                      "Assets/Buttons/settings_button.png",
                                                     "Assets/Buttons/settings_button_hover.png", "Assets/Sounds/click.mp3", settings)
                        exit_button = ImageButton((settings.width - 252) / 2, settings.height * 0.55, 252, 74, "",
                                                  "Assets/Buttons/exit_button.png",
                                                 "Assets/Buttons/exit_button_hover.png", "Assets/Sounds/click.mp3", settings)
                elif event.button == exit_button:
                    fade_screen()
                    running = False
                    break

            for btn in [start_button, settings_button, exit_button]:
                btn.handle_event(event)

        for btn in [start_button, settings_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)  #60 fps

    cap.release()
    pygame.quit()
    sys.exit()

def levelScreenSettings(game_last_frame, last_frame):
    if game_last_frame:
        if settings.fullscreen:
            screen = pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((settings.width, settings.height), pygame.RESIZABLE)
        screen.blit(game_last_frame, (0, 0))
        pygame.display.flip()
    elif last_frame:
        if settings.fullscreen:
            screen = pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((settings.width, settings.height), pygame.RESIZABLE)
        screen.blit(last_frame, (0, 0))
        pygame.display.flip()

def select_level():
    global screen, cap, settings
    running = True
    clock = pygame.time.Clock()  #for fps control
    last_frame = None  # last video frame

    if screen is None:
        if settings.fullscreen:
            screen = pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((settings.width, settings.height), pygame.RESIZABLE)

    button_width = 80
    button_spacing = 10
    total_buttons_width = 3 * button_width + 2 * button_spacing
    start_x = (settings.width - total_buttons_width) / 2

    Lbutton1 = ImageButton(start_x - 5, settings.height * 0.35 - 5, button_width + 10, 74 + 10, "",
                           "Assets/Buttons/level_but_1_bird.png",
                           "Assets/Buttons/level_but_hover_1_bird.png", "Assets/Sounds/click.mp3", settings)
    Lbutton2 = ImageButton(start_x + button_width + button_spacing, settings.height * 0.35, button_width, 74, "",
                           "Assets/Buttons/level_but_2.png",
                           "Assets/Buttons/level_but_hover_2.png", "Assets/Sounds/click.mp3", settings)
    Lbutton3 = ImageButton(start_x + 2 * (button_width + button_spacing) - 5, settings.height * 0.35 - 5, button_width + 10, 74 + 10, "",
                           "Assets/Buttons/level_but_3_bird.png",
                           "Assets/Buttons/level_but_hover_3_bird.png", "Assets/Sounds/click.mp3", settings)
    Lbutton4 = ImageButton(start_x - 5, settings.height * 0.45 - 5, button_width + 10, 74 + 10, "",
                           "Assets/Buttons/level_but_4_bird.png",
                           "Assets/Buttons/level_but_hover_4_bird.png", "Assets/Sounds/click.mp3", settings)
    Lbutton5 = ImageButton(start_x + button_width + button_spacing, settings.height * 0.45, button_width, 74, "",
                           "Assets/Buttons/level_but_5.png",
                           "Assets/Buttons/level_but_hover_5.png", "Assets/Sounds/click.mp3", settings)
    Lbutton6 = ImageButton(start_x + 2 * (button_width + button_spacing) - 5, settings.height * 0.45 - 5, button_width + 10, 74 + 10, "",
                           "Assets/Buttons/level_but_6_bird.png",
                           "Assets/Buttons/level_but_hover_6_bird.png", "Assets/Sounds/click.mp3", settings)
    Lbutton7 = ImageButton(start_x - 5, settings.height * 0.55 - 5, button_width + 10, 74 + 10, "",
                           "Assets/Buttons/level_but_7_bird.png",
                           "Assets/Buttons/level_but_hover_7_bird.png", "Assets/Sounds/click.mp3", settings)
    Lbutton8 = ImageButton(start_x + button_width + button_spacing - 5, settings.height * 0.55 - 5, button_width + 10, 74 + 10, "",
                           "Assets/Buttons/level_but_8_bird.png",
                           "Assets/Buttons/level_but_hover_8_bird.png", "Assets/Sounds/click.mp3", settings)
    Lbutton9 = ImageButton(start_x + 2 * (button_width + button_spacing), settings.height * 0.55, button_width, 74, "",
                           "Assets/Buttons/level_but_9.png",
                           "Assets/Buttons/level_but_hover_9.png", "Assets/Sounds/click.mp3", settings)
    back_button = ImageButton((settings.width - 252) / 2, settings.height * 0.65, 252, 74, "",
                              "Assets/Buttons/back_button.png",
                              "Assets/Buttons/back_button_hover.png", "Assets/Sounds/click.mp3", settings)

    while running:
        try:
            ret, frame = None, None
            attempts = 5
            while attempts > 0 and (not ret or frame is None):
                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                attempts -= 1
                if attempts == 0 and not ret:
                    raise Exception("video error")

            info = pygame.display.Info()
            max_width, max_height = min(settings.width, info.current_w), min(settings.height, info.current_h)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (max_width, max_height), interpolation=cv2.INTER_LINEAR)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            last_frame = frame_surface
            screen.blit(frame_surface, (0, 0))
        except Exception as e:
            print(f"video error (Menu): {e}")
            if last_frame:
                screen.blit(last_frame, (0, 0))
            else:
                screen.fill((0, 0, 0))  #if no background

        draw_text_with_outline("Select level", font, (255, 255, 255), (0, 0, 0), settings.width / 2, settings.height * 0.2, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fade_screen()
                running = False
                cap.release()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
            if event.type == pygame.USEREVENT:
                fade_screen()
                if event.button == Lbutton1:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Assets/Sounds/level_music.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    game = Game(fullscreen=settings.fullscreen, cap=cap, screen=screen, last_frame=last_frame,
                                bird_speed= 0, birdLevelCount= 6, levelType=1, ammoLevel = 0)
                    game_last_frame = game.start_level()
                    levelScreenSettings(game_last_frame, last_frame)
                if event.button == Lbutton2:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Assets/Sounds/level_music.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    game = Game(fullscreen=settings.fullscreen, cap=cap, screen=screen, last_frame=last_frame,
                                bird_speed= 0, birdLevelCount= 6, levelType=2, ammoLevel = 0)
                    game_last_frame = game.start_level()
                    levelScreenSettings(game_last_frame, last_frame)
                if event.button == Lbutton3:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Assets/Sounds/level_music.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    game = Game(fullscreen=settings.fullscreen, cap=cap, screen=screen, last_frame=last_frame,
                                bird_speed=1, birdLevelCount=8, levelType=3, ammoLevel = 1)
                    game_last_frame = game.start_level()
                    levelScreenSettings(game_last_frame, last_frame)
                if event.button == Lbutton4:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Assets/Sounds/level_music.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    game = Game(fullscreen=settings.fullscreen, cap=cap, screen=screen, last_frame=last_frame,
                                bird_speed=1, birdLevelCount=10, levelType=4, ammoLevel = 1)
                    game_last_frame = game.start_level()
                    levelScreenSettings(game_last_frame, last_frame)
                if event.button == Lbutton5:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Assets/Sounds/level_music.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    game = Game(fullscreen=settings.fullscreen, cap=cap, screen=screen, last_frame=last_frame,
                                bird_speed=1, birdLevelCount=12, levelType=5, ammoLevel = 1)
                    game_last_frame = game.start_level()
                    levelScreenSettings(game_last_frame, last_frame)
                if event.button == Lbutton6:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Assets/Sounds/level_music.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    game = Game(fullscreen=settings.fullscreen, cap=cap, screen=screen, last_frame=last_frame,
                                bird_speed=1, birdLevelCount=14, levelType=6, ammoLevel = 2)
                    game_last_frame = game.start_level()
                    levelScreenSettings(game_last_frame, last_frame)
                if event.button == Lbutton7:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Assets/Sounds/level_music.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    game = Game(fullscreen=settings.fullscreen, cap=cap, screen=screen, last_frame=last_frame,
                                bird_speed=2, birdLevelCount=16, levelType=7, ammoLevel = 2)
                    game_last_frame = game.start_level()
                    levelScreenSettings(game_last_frame, last_frame)
                if event.button == Lbutton8:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Assets/Sounds/level_music.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    game = Game(fullscreen=settings.fullscreen, cap=cap, screen=screen, last_frame=last_frame,
                                bird_speed=2, birdLevelCount=18, levelType=8, ammoLevel = 3)
                    game_last_frame = game.start_level()
                    levelScreenSettings(game_last_frame, last_frame)
                if event.button == Lbutton9:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Assets/Sounds/level_music.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    game = Game(fullscreen=settings.fullscreen, cap=cap, screen=screen, last_frame=last_frame,
                                bird_speed=2, birdLevelCount=25, levelType=9, ammoLevel = 3)
                    game_last_frame = game.start_level()
                    levelScreenSettings(game_last_frame, last_frame)
                elif event.button == back_button:
                    fade_screen()
                    running = False

                    if last_frame:
                        if settings.fullscreen:
                            screen = pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((settings.width, settings.height), pygame.RESIZABLE)
                        screen.blit(last_frame, (0, 0))
                        pygame.display.flip()
                    break

            for btn in [Lbutton1, Lbutton2, Lbutton3, Lbutton4, Lbutton5, Lbutton6, Lbutton7, Lbutton8, Lbutton9, back_button]:
                btn.handle_event(event)

        for btn in [Lbutton1, Lbutton2, Lbutton3, Lbutton4, Lbutton5, Lbutton6, Lbutton7, Lbutton8, Lbutton9, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)  #60 fps

def main():
    main_menu()

if __name__ == "__main__":
    main()