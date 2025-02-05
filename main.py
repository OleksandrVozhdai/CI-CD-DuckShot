import pygame
import sys
from Button import ImageButton
import cv2
from Game import Game

pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 1920, 1080
my_font = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Hunt")

video_path = "Assets/Background/lvl1.mp4"
cap = cv2.VideoCapture(video_path)

start_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, "Нова гра", "Assets/Buttons/green_button.png","Assets/Buttons/green_button_hover.png", "Assets/Sounds/click.mp3")
settings_button = ImageButton(WIDTH / 2 - (252 / 2), 450, 252, 74, "Налаштування", "Assets/Buttons/green_button.png","Assets/Buttons/green_button_hover.png", "Assets/Sounds/click.mp3")
exit_button = ImageButton(WIDTH / 2 - (252 / 2), 550, 252, 74, "Вихід", "Assets/Buttons/green_button.png","Assets/Buttons/green_button_hover.png", "Assets/Sounds/click.mp3")


def main_menu():
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
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.USEREVENT and event.button == start_button:
                levelone = Game()
                levelone.startlevel()

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

def main():
    main_menu()

if __name__ == "__main__":
    main()