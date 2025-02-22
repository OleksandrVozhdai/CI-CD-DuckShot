import pygame
import sys
from Button import ImageButton
import cv2
from Game import Game
from Settings import Settings

pygame.init()
pygame.font.init()
info = pygame.display.Info()

# Спочатку ініціалізуємо cap, щоб він був доступний
video_path = "Assets/Background/lvl1.mp4"
cap = cv2.VideoCapture(video_path)

# Обмежимо частоту кадрів відео для оптимізації
cap.set(cv2.CAP_PROP_FPS, 30)  # Встановимо 30 FPS для стабільності

# Тепер ініціалізуємо settings з cap
settings = Settings(info.current_w, info.current_h, cap)  # Ініціалізуємо налаштування з поточною роздільною здатністю монітора

# Ініціалізуємо екран залежно від повноекранного режиму
if settings.fullscreen:
    screen = pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((settings.width, settings.height), pygame.RESIZABLE)

my_font = pygame.font.SysFont('Comic Sans MS', 30)
font = pygame.font.SysFont('Comic Sans MS', 72)

pygame.display.set_caption("Duck Hunt")

# Ініціалізація кнопок з урахуванням поточної роздільної здатності
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

def main_menu():
    global screen, cap, start_button, settings_button, exit_button
    running = True
    clock = pygame.time.Clock()  # Додаємо Clock для керування FPS
    last_frame = None  # Буфер для останнього кадру відео

    while running:
        try:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            # Масштабуємо відео під поточну роздільну здатність з оптимізацією
            info = pygame.display.Info()
            max_width, max_height = min(settings.width, info.current_w), min(settings.height, info.current_h)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (max_width, max_height), interpolation=cv2.INTER_LINEAR)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            last_frame = frame_surface  # Зберігаємо останній кадр
            screen.blit(frame_surface, (0, 0))
        except Exception as e:
            print(f"Помилка при обробці відео в головному меню: {e}")
            if last_frame:
                screen.blit(last_frame, (0, 0))  # Використовуємо останній вдалий кадр, якщо помилка
            else:
                screen.fill((0, 0, 0))  # Чорний екран тільки якщо немає буфера

        draw_text_with_outline("Duck Hunt", font, (255, 255, 255), (0, 0, 0), settings.width / 2, settings.height * 0.2, screen)

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
                    # Відновлюємо виклик меню вибору рівнів
                    select_level()
                elif event.button == settings_button:
                    screen = settings.settings_menu(screen, font, lambda text, f, tc, oc, x, y: draw_text_with_outline(text, f, tc, oc, x, y, screen), main_menu)
                    if screen:
                        settings.width, settings.height = screen.get_width(), screen.get_height()
                        # Позиціонуємо кнопки пропорційно новому розміру
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
        clock.tick(60)  # Встановлюємо 60 FPS для плавного рендерингу

    cap.release()
    pygame.quit()
    sys.exit()

def select_level():
    global screen, cap, settings
    running = True
    clock = pygame.time.Clock()  # Додаємо Clock для керування FPS
    last_frame = None  # Буфер для останнього кадру відео

    # Перестворюємо кнопки з урахуванням поточної роздільної здатності та центруємо по горизонталі
    button_width = 80
    button_spacing = 10
    total_buttons_width = 3 * button_width + 2 * button_spacing  # 3 кнопки в рядку з проміжками
    start_x = (settings.width - total_buttons_width) / 2  # Центр рядка кнопок

    Lbutton1 = ImageButton(start_x, settings.height * 0.35, button_width, 74, "", "Assets/Buttons/level_but_1.png",
                           "Assets/Buttons/level_but_hover_1.png", "Assets/Sounds/click.mp3", settings)
    Lbutton2 = ImageButton(start_x + button_width + button_spacing, settings.height * 0.35, button_width, 74, "", "Assets/Buttons/level_but_2.png",
                           "Assets/Buttons/level_but_hover_2.png", "Assets/Sounds/click.mp3", settings)
    Lbutton3 = ImageButton(start_x + 2 * (button_width + button_spacing), settings.height * 0.35, button_width, 74, "", "Assets/Buttons/level_but_3.png",
                           "Assets/Buttons/level_but_hover_3.png", "Assets/Sounds/click.mp3", settings)
    Lbutton4 = ImageButton(start_x, settings.height * 0.45, button_width, 74, "", "Assets/Buttons/level_but_4.png",
                           "Assets/Buttons/level_but_hover_4.png", "Assets/Sounds/click.mp3", settings)
    Lbutton5 = ImageButton(start_x + button_width + button_spacing, settings.height * 0.45, button_width, 74, "", "Assets/Buttons/level_but_5.png",
                           "Assets/Buttons/level_but_hover_5.png", "Assets/Sounds/click.mp3", settings)
    Lbutton6 = ImageButton(start_x + 2 * (button_width + button_spacing), settings.height * 0.45, button_width, 74, "", "Assets/Buttons/level_but_6.png",
                           "Assets/Buttons/level_but_hover_6.png", "Assets/Sounds/click.mp3", settings)
    Lbutton7 = ImageButton(start_x, settings.height * 0.55, button_width, 74, "", "Assets/Buttons/level_but_7.png",
                           "Assets/Buttons/level_but_hover_7.png", "Assets/Sounds/click.mp3", settings)
    Lbutton8 = ImageButton(start_x + button_width + button_spacing, settings.height * 0.55, button_width, 74, "", "Assets/Buttons/level_but_8.png",
                           "Assets/Buttons/level_but_hover_8.png", "Assets/Sounds/click.mp3", settings)
    Lbutton9 = ImageButton(start_x + 2 * (button_width + button_spacing), settings.height * 0.55, button_width, 74, "", "Assets/Buttons/level_but_9.png",
                           "Assets/Buttons/level_but_hover_9.png", "Assets/Sounds/click.mp3", settings)
    back_button = ImageButton((settings.width - 252) / 2, settings.height * 0.65, 252, 74, "", "Assets/Buttons/back_button.png",
                              "Assets/Buttons/back_button_hover.png", "Assets/Sounds/click.mp3", settings)

    while running:
        try:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            # Масштабуємо відео під поточну роздільну здатність з оптимізацією
            info = pygame.display.Info()
            max_width, max_height = min(settings.width, info.current_w), min(settings.height, info.current_h)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (max_width, max_height), interpolation=cv2.INTER_LINEAR)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            last_frame = frame_surface  # Зберігаємо останній кадр
            screen.blit(frame_surface, (0, 0))
        except Exception as e:
            print(f"Помилка при обробці відео у виборі рівня: {e}")
            if last_frame:
                screen.blit(last_frame, (0, 0))  # Використовуємо останній вдалий кадр, якщо помилка
            else:
                screen.fill((0, 0, 0))  # Чорний екран тільки якщо немає буфера

        draw_text_with_outline("Select level", font, (255, 255, 255), (0, 0, 0), settings.width / 2, settings.height * 0.2, screen)

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
                    # Створюємо об'єкт Game, використовуючи існуючий screen та cap
                    game = Game(screen=screen, cap=cap)
                    game.start_level()
                    # Відновлюємо екран з плавним переходом, використовуючи останній кадр
                    if last_frame:
                        screen.blit(last_frame, (0, 0))  # Негайно відображаємо останній кадр
                        pygame.display.flip()
                elif event.button == back_button:
                    running = False
                    # Плавне відновлення екрана з використанням останнього кадру
                    if last_frame:
                        screen.blit(last_frame, (0, 0))  # Негайно відображаємо останній кадр
                        pygame.display.flip()
                    break

            for btn in [Lbutton1, Lbutton2, Lbutton3, Lbutton4, Lbutton5, Lbutton6, Lbutton7, Lbutton8, Lbutton9, back_button]:
                btn.handle_event(event)

        for btn in [Lbutton1, Lbutton2, Lbutton3, Lbutton4, Lbutton5, Lbutton6, Lbutton7, Lbutton8, Lbutton9, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # Встановлюємо 60 FPS для плавного рендерингу

def main():
    main_menu()

if __name__ == "__main__":
    main()