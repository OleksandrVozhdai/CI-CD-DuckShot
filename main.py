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

# Ограничим частоту кадров видео для оптимизации
cap.set(cv2.CAP_PROP_FPS, 30)  # Установим 30 FPS для стабильности
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1000)  # Увеличим буфер для быстрого чтения кадров

# Теперь инициализируем settings с cap
settings = Settings(info.current_w, info.current_h, cap)  # Инициализируем настройки с текущим разрешением монитора

# Инициализируем экран в зависимости от полноэкранного режима для главного меню
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
    clock = pygame.time.Clock()  # Добавляем Clock для управления FPS
    last_frame = None  # Буфер для последнего кадра видео

    while running:
        try:
            # Повторяем попытку чтения кадра до успеха (максимум 5 попыток)
            ret, frame = None, None
            attempts = 5
            while attempts > 0 and (not ret or frame is None):
                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                attempts -= 1
                if attempts == 0 and not ret:
                    raise Exception("Не удалось загрузить кадр видео после нескольких попыток")
            # Масштабируем видео под текущее разрешение с оптимизацией
            info = pygame.display.Info()
            max_width, max_height = min(settings.width, info.current_w), min(settings.height, info.current_h)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (max_width, max_height), interpolation=cv2.INTER_LINEAR)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            last_frame = frame_surface  # Сохраняем последний кадр
            screen.blit(frame_surface, (0, 0))
        except Exception as e:
            print(f"Ошибка при обработке видео в главном меню: {e}")
            if last_frame:
                screen.blit(last_frame, (0, 0))  # Используем последний удачный кадр, если ошибка
            else:
                screen.fill((0, 0, 0))  # Черный экран только если нет буфера

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
                    # Восстанавливаем вызов меню выбора уровней
                    select_level()
                elif event.button == settings_button:
                    screen = settings.settings_menu(screen, font, lambda text, f, tc, oc, x, y: draw_text_with_outline(text, f, tc, oc, x, y, screen), main_menu)
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
        clock.tick(60)  # Устанавливаем 60 FPS для плавного рендеринга

    cap.release()
    pygame.quit()
    sys.exit()

def select_level():
    global screen, cap, settings
    running = True
    clock = pygame.time.Clock()  # Добавляем Clock для управления FPS
    last_frame = None  # Буфер для последнего кадра видео

    # Явно указываем, что screen — глобальная переменная
    if screen is None:
        if settings.fullscreen:
            screen = pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((settings.width, settings.height), pygame.RESIZABLE)

    # Пересоздаем кнопки с учетом текущего разрешения и центрируем по горизонтали
    button_width = 80
    button_spacing = 10
    total_buttons_width = 3 * button_width + 2 * button_spacing  # 3 кнопки в ряду с промежутками
    start_x = (settings.width - total_buttons_width) / 2  # Центр ряда кнопок

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
            # Повторяем попытку чтения кадра до успеха (максимум 5 попыток)
            ret, frame = None, None
            attempts = 5
            while attempts > 0 and (not ret or frame is None):
                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                attempts -= 1
                if attempts == 0 and not ret:
                    raise Exception("Не удалось загрузить кадр видео после нескольких попыток")
            # Масштабируем видео под текущее разрешение с оптимизацией
            info = pygame.display.Info()
            max_width, max_height = min(settings.width, info.current_w), min(settings.height, info.current_h)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (max_width, max_height), interpolation=cv2.INTER_LINEAR)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            last_frame = frame_surface  # Сохраняем последний кадр
            screen.blit(frame_surface, (0, 0))
        except Exception as e:
            print(f"Ошибка при обработке видео в выборе уровня: {e}")
            if last_frame:
                screen.blit(last_frame, (0, 0))  # Используем последний удачный кадр, если ошибка
            else:
                screen.fill((0, 0, 0))  # Черный экран только если нет буфера

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
                    # Создаем объект Game с учетом текущего значения fullscreen из settings
                    game = Game(fullscreen=settings.fullscreen, cap=cap, screen=screen, last_frame=last_frame)
                    game_last_frame = game.start_level()
                    # После завершения игры восстанавливаем screen и буфер с плавным переходом
                    if game_last_frame:  # Используем последний кадр из игры
                        if settings.fullscreen:
                            screen = pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((settings.width, settings.height), pygame.RESIZABLE)
                        screen.blit(game_last_frame, (0, 0))  # Немедленно отображаем последний кадр
                        pygame.display.flip()
                    elif last_frame:  # Если кадр из игры отсутствует, используем последний кадр меню
                        if settings.fullscreen:
                            screen = pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((settings.width, settings.height), pygame.RESIZABLE)
                        screen.blit(last_frame, (0, 0))  # Немедленно отображаем последний кадр
                        pygame.display.flip()
                elif event.button == back_button:
                    running = False
                    # Плавное восстановление экрана с использованием последнего кадра
                    if last_frame:
                        if settings.fullscreen:
                            screen = pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((settings.width, settings.height), pygame.RESIZABLE)
                        screen.blit(last_frame, (0, 0))  # Немедленно отображаем последний кадр
                        pygame.display.flip()
                    break

            for btn in [Lbutton1, Lbutton2, Lbutton3, Lbutton4, Lbutton5, Lbutton6, Lbutton7, Lbutton8, Lbutton9, back_button]:
                btn.handle_event(event)

        for btn in [Lbutton1, Lbutton2, Lbutton3, Lbutton4, Lbutton5, Lbutton6, Lbutton7, Lbutton8, Lbutton9, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # Устанавливаем 60 FPS для плавного рендеринга

    # Этот блок больше не нужен, так как восстановление обрабатывается выше
    #if settings.fullscreen:
    #    screen = pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)
    #else:
    #    screen = pygame.display.set_mode((settings.width, settings.height), pygame.RESIZABLE)

def main():
    main_menu()

if __name__ == "__main__":
    main()