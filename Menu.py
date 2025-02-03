import pygame
import sys
from Button import ImageButton
import cv2
import time
import random
from Birds import Bird

pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 1920, 1080
my_font = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Hunt")

video_path = "Assets/Background/lvl1.mp4"
cap = cv2.VideoCapture(video_path)

def main_menu():
    start_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, "Нова гра", "Assets/Buttons/green_button.png","Assets/Buttons/green_button_hover.png", "Assets/Sounds/click.mp3")
    settings_button = ImageButton(WIDTH / 2 - (252 / 2), 450, 252, 74, "Налаштування", "Assets/Buttons/green_button.png","Assets/Buttons/green_button_hover.png", "Assets/Sounds/click.mp3")
    exit_button = ImageButton(WIDTH / 2 - (252 / 2), 550, 252, 74, "Вихід", "Assets/Buttons/green_button.png","Assets/Buttons/green_button_hover.png", "Assets/Sounds/click.mp3")

    running = True
    while running:

        # video bg
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1920, 1080))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

        font = pygame.font.SysFont('Comic Sans MS', 72)
        text_surface = font.render("Duck Hunt", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH/2, 270))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.USEREVENT and event.button == start_button:
                new_game()

            if event.type == pygame.USEREVENT and event.button == settings_button:
                settings_menu()

            if event.type == pygame.USEREVENT and event.button == exit_button:
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

def settings_menu():
    audio_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, "Аудіо", "Assets/Buttons/green_button.png","Assets/Buttons/green_button_hover.png", "Assets/Sounds/click.mp3")
    video_button = ImageButton(WIDTH / 2 - (252 / 2), 450, 252, 74, "Відео","Assets/Buttons/green_button.png", "Assets/Buttons/green_button_hover.png","Assets/Sounds/click.mp3")
    back_button = ImageButton(WIDTH / 2 - (252 / 2), 550, 252, 74, "Назад", "Assets/Buttons/green_button.png","Assets/Buttons/green_button_hover.png", "Assets/Sounds/click.mp3")

    running = True
    while running:
        # video bg
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1920, 1080))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface,  (0, 0))

        font = pygame.font.SysFont('Comic Sans MS', 72)
        text_surface = font.render("Settings", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 270))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == pygame.USEREVENT and event.button == back_button:
                main_menu()

            for btn in [audio_button, video_button, back_button]:
                btn.handle_event(event)

        for btn in [audio_button, video_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

    cap.release()
    pygame.quit()

def new_game():
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    # background video
    video_path = "Assets/Background/lvl1.mp4"
    cap = cv2.VideoCapture(video_path)

    # scope
    scope = pygame.image.load('Assets/Hud/scope.png')
    scope = pygame.transform.scale(scope, (70, 70))

    # birds sprite blue
    sprite_sheet_blue = pygame.image.load("Assets/Birds/birdFlyBlue.png").convert_alpha()
    sprite_sheet_blue = pygame.transform.scale(sprite_sheet_blue, (500, 400))

    SpritePerRow_Blue = 5
    Rows_Blue = 4
    SpriteWidth_Blue = sprite_sheet_blue.get_width() // SpritePerRow_Blue
    SpriteHeight_Blue = sprite_sheet_blue.get_height() // Rows_Blue

    # birds sprite red
    sprite_sheet_red = pygame.image.load("Assets/Birds/birdFlyRed.png").convert_alpha()
    sprite_sheet_red = pygame.transform.scale(sprite_sheet_red, (500, 400))

    SpritePerRow_Red = 5
    Rows_Red = 4
    SpriteWidth_Red = sprite_sheet_red.get_width() // SpritePerRow_Red
    SpriteHeight_Red = sprite_sheet_red.get_height() // Rows_Red

    # timer
    game_duration = 40
    start_time = time.time()

    birds = []
    birdSpeed = 1

    spawn_point = [(-30, 0), (-30, 400), (1700, 400), (1700, 0)]
    score = 0
    blink_time = 0
    blink_duration = 100

    running = True
    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= game_duration:
            print(f"Game is over. Your Score: {score}")
            break  # Вихід з циклу гри

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(True)  # Повертаємо курсор миші після гри
                    main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for bird in birds:
                    if bird.check_collision(mouse_pos):
                        blink_time = pygame.time.get_ticks()
                        birds.remove(bird)
                        score += 1
                        break

        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1920, 1080))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

        text_surface = my_font.render("Score : " + str(score), False, (0, 0, 0))
        screen.blit(text_surface, (1300, 100))

        if random.randint(0, 100) <= 1:
            spawn_points = random.choice(spawn_point)
            bird_type = random.choice(["blue", "red"])
            if bird_type == "blue":
                new_bird = Bird(spawn_points[0], spawn_points[1], False, True, random.choice([True, False]),
                                random.choice([True, False]),
                                sprite_sheet_blue, SpritePerRow_Blue, SpriteWidth_Blue, SpriteHeight_Blue)
            elif bird_type == "red":
                new_bird = Bird(spawn_points[0], spawn_points[1], False, True, random.choice([True, False]),
                                random.choice([True, False]),
                                sprite_sheet_red, SpritePerRow_Red, SpriteWidth_Red, SpriteHeight_Red)
            birds.append(new_bird)

        for bird in birds:
            bird.update(birdSpeed, screen)
            bird.draw(screen)

        if pygame.time.get_ticks() - blink_time < blink_duration:
            screen.fill((255, 255, 255))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        scope_rect = scope.get_rect(center=(mouse_x, mouse_y))
        screen.blit(scope, scope_rect)

        pygame.display.flip()
        clock.tick(60)

    cap.release()
    pygame.mouse.set_visible(True)  # Повертаємо курсор миші після гри
    main_menu()

def main():
    main_menu()

if __name__ == "__main__":
    main()



