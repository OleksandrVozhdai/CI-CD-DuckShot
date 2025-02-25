import pygame
from Birds import Bird
import random
import time
import cv2
import sys

class Game:
    pygame.mixer.init()
    def __init__(self, fullscreen=False, cap=None, screen=None, last_frame=None, bird_speed = None, birdLevelCount = None,
                 levelType = None, ammoLevel = None):
        self.start_time = None #it does nothing but don't touch it. Attribute warning
        self.running = None #it does nothing but don't touch it. Attribute warning
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h

        self.shot_sound = pygame.mixer.Sound("Assets/Sounds/shot_sound.wav")
        self.reload_sound = pygame.mixer.Sound("Assets/Sounds/reload_sound.mp3")
        self.awp_shot_sound = pygame.mixer.Sound("Assets/Sounds/awp_shot_sound.mp3")

        self.sound_play = False

        if screen is not None:
            self.screen = screen
        else:
            if fullscreen:
                self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.video_path = "Assets/Background/lvl1.mp4"
        self.cap = cv2.VideoCapture(self.video_path)
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.paused = False
        self.pause_start_time = 0
        self.total_paused_time = 0
        self.exit_to_menu = False
        self.show_controls = False
        #bird sprite-sheet sett
        self.SpritePerRow= 5
        self.Rows = 4

        #birds sprite blue
        self.sprite_sheet_blue = pygame.image.load("Assets/Birds/birdFlyBlue.png").convert_alpha()
        self.sprite_sheet_blue = pygame.transform.scale(self.sprite_sheet_blue, (500, 400))

        self.SpriteWidth_Blue = self.sprite_sheet_blue.get_width() // self.SpritePerRow
        self.SpriteHeight_Blue = self.sprite_sheet_blue.get_height() // self.Rows

        #birds sprite red
        self.sprite_sheet_red = pygame.image.load("Assets/Birds/birdFlyRed.png").convert_alpha()
        self.sprite_sheet_red = pygame.transform.scale(self.sprite_sheet_red, (500, 400))

        self.SpriteWidth_Red = self.sprite_sheet_red.get_width() // self.SpritePerRow
        self.SpriteHeight_Red = self.sprite_sheet_red.get_height() // self.Rows

        #birds sprite yellow
        self.sprite_sheet_yellow = pygame.image.load("Assets/Birds/birdFlyYellow.png").convert_alpha()
        self.sprite_sheet_yellow = pygame.transform.scale(self.sprite_sheet_yellow, (500, 400))

        self.SpriteWidth_Yellow = self.sprite_sheet_yellow.get_width() // self.SpritePerRow
        self.SpriteHeight_Yellow = self.sprite_sheet_yellow.get_height() // self.Rows

        #birds sprite black fatty
        self.sprite_sheet_BlackFatty = pygame.image.load("Assets/Birds/birdFlyBlack.png").convert_alpha()
        self.sprite_sheet_BlackFatty = pygame.transform.scale(self.sprite_sheet_BlackFatty, (1000, 800))

        self.SpriteWidth_BlackFatty = self.sprite_sheet_BlackFatty.get_width() // self.SpritePerRow
        self.SpriteHeight_BlackFatty = self.sprite_sheet_BlackFatty.get_height() // self.Rows

        #bird sprite diagonally
        self.sprite_sheet_Diagonally = pygame.image.load("Assets/Birds/birdFlyDiagonal.png").convert_alpha()
        self.sprite_sheet_Diagonally = pygame.transform.scale(self.sprite_sheet_Diagonally, (1000, 800))

        self.SpriteWidth_Diagonally = self.sprite_sheet_Diagonally.get_width() // self.SpritePerRow
        self.SpriteHeight_Diagonally = self.sprite_sheet_Diagonally.get_height() // self.Rows

        #Bird parameters
        self.birdSpeed = bird_speed
        self.spawn_point = [(-200, 0), (-200, 400), (self.WIDTH + 10, 400), (self.WIDTH + 10, 0)]
        self.ground_spawn_point = [0, 1000]
        self.birdLevelCount = birdLevelCount #how many birds can be on screen. Recommended number 9-13

        #Player stats
        self.level_timer = 40 #If you want to change time fo level, u need to make sure that background video length is >= level_timer
        self.score = 0
        self.blink_time = 0
        self.blink_duration = 100
        self.death_times = {}
        self.shootDelay = 500
        self.last_shot_time = 0
        self.ammo = None
        self.magazine = None

        #Initialize bird list
        self.birds = []


        #Level settings
        self.levelType = levelType
        self.ammoLevel = ammoLevel

        if ammoLevel == 0:
            self.ammo = 4
            self.magazine = 4
        elif ammoLevel == 1:
            self.ammo = 6
            self.magazine = 6
        elif ammoLevel == 2:
            self.ammo = 8
            self.magazine = 8
        elif ammoLevel == 3:
            self.ammo = 10
            self.magazine = 10

    #Function to start level
    def start_level(self):
        pygame.mouse.set_visible(False)
        self.running = True
        self.start_time = time.time()
        self.total_shots = 0
        self.total_hits = 0

        while self.running:
            self.handle_events()
            if self.exit_to_menu:
                return

            if self.paused:
                self.draw_pause_screen()
                pygame.display.flip()
                self.clock.tick(10)
                continue

            self.update_game_state()
            self.draw_game_state()
            pygame.display.flip()
            self.clock.tick(self.level_timer)

        self.show_statistics()

    def show_statistics(self):
        self.screen.fill((0, 0, 0))
        accuracy = (self.total_hits / self.total_shots * 100) if self.total_shots > 0 else 0

        stats_text = [
            f"Total Shots: {self.total_shots}",
            f"Hits: {self.total_hits}",
            f"Hit Accuracy: {accuracy:.2f}%",
            f"Birds Shot Down: {len(self.death_times)}",
            f"Score: {self.score}"
        ]

        y_offset = self.HEIGHT // 3
        for text in stats_text:
            rendered_text = self.my_font.render(text, True, (255, 255, 255))
            text_rect = rendered_text.get_rect(center=(self.WIDTH // 2, y_offset))
            self.screen.blit(rendered_text, text_rect)
            y_offset += 50

        pygame.mixer.music.stop()
        pygame.display.flip()
        pygame.time.wait(5000)
        pygame.mixer.music.load("Assets/Sounds/main_theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def draw_pause_screen(self):
        font = pygame.font.SysFont('Comic Sans MS', 72)
        text = font.render("Paused", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.show_controls = not self.show_controls

                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_p:
                    if not self.paused:
                        self.pause_start_time = time.time()
                    else:
                        self.total_paused_time += time.time() - self.pause_start_time
                    self.paused = not self.paused

                elif event.key == pygame.K_m:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Assets/Sounds/main_theme.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    pygame.mouse.set_visible(True)
                    self.running = False
                    self.exit_to_menu = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(pygame.mouse.get_pos())

    def handle_mouse_click(self, mouse_pos):
        if self.ammo > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.shootDelay:
                self.awp_shot_sound.play()
                self.total_shots += 1
                for bird in self.birds:
                    if bird.check_collision(mouse_pos):
                        self.blink_time = pygame.time.get_ticks()
                        bird.hp -= 1
                        bird.birdSpeed += 2
                        bird.frame_delay -= 2
                        if bird.hp <= 0:
                            bird.kill()
                            self.birdLevelCount += 1
                            self.death_times[bird.id] = pygame.time.get_ticks()
                            self.score += bird.value
                            self.total_hits += 1
                        break
                self.last_shot_time = current_time
                self.ammo -= 1

    def update_game_state(self):
        if self.paused:
            return

        current_time = time.time()
        elapsed_time = current_time - self.start_time - self.total_paused_time

        if elapsed_time >= 40:
            self.running = False
            pygame.mouse.set_visible(True)
            print(f"Game Over! Score: {self.score}")
            return

        #Remove birds that are dead for too long
        current_time = pygame.time.get_ticks()
        for bird in list(self.birds):
            if bird in self.death_times and current_time - self.death_times[bird] >= 5000:
                self.birds.remove(bird)
                del self.death_times[bird]

        #Spawn birds
        if random.randint(0, 100) <= 1:
            self.spawn_bird()

        #Update birds
        for bird in self.birds:
            bird.update()

        #reloading
        if self.ammo <= 0:
            if self.sound_play == False:
                self.sound_play = True
                self.reload_sound.play()
            if current_time - self.last_shot_time >= 3000:
                self.ammo = self.magazine
                self.sound_play = False
            return

    def spawn_bird(self):
        spawn_points = random.choice(self.spawn_point)

        if self.birdLevelCount > 0:
            bird_types = ["blue", "red", "yellow", "black-fatty", "diagonally"]

            new_bird = None #it does nothing but don't touch it, or you will get "reference" warning


            #level difficulty constructor settings, don't touch it

            #easy
            if self.birdSpeed == 0:
                blueSpeed = random.choice([0.5, 0.75, 1])
                redSpeed = random.choice([1, 2, 3])
                yellowSpeed = 6
                blackSpeed = 0.3
                blackHp = 2
                diagonallySpeed = 1.5
            # normal
            elif self.birdSpeed == 1:
                blueSpeed = random.choice([0.75, 1, 1.25, 1.5])
                redSpeed = 3
                yellowSpeed = 9
                blackSpeed = 0.4
                blackHp = 3
                diagonallySpeed = 2
            #hard
            elif self.birdSpeed == 2:
                blueSpeed = random.choice([1.25, 1.5, 1.75, 2])
                redSpeed = 5
                yellowSpeed = 12
                blackSpeed = 0.8
                blackHp = 4
                diagonallySpeed = 4
                ...
            else : #if something goes wrong
                blueSpeed = 1
                redSpeed = 1
                yellowSpeed = 1
                blackSpeed = 1
                blackHp = 1
                diagonallySpeed = 1

            if self.levelType  < 2:
                spawn_weight = [100, 0, 0, 0, 0]  # birds rarity
            elif 2 <= self.levelType <= 3:
                spawn_weight = [65, 30, 0, 0, 0]
            elif 3 < self.levelType <= 5:
                spawn_weight = [65, 30, 5, 0, 0]
            elif 5 < self.levelType <= 6:
                spawn_weight = [50, 30, 10, 10, 0]
            elif self.levelType > 6 :
                spawn_weight = [20, 20, 20, 20, 20]
            else : spawn_weight = [50, 30, 10, 9, 1] #if something goes wrong

            bird_type = random.choices(bird_types, weights=spawn_weight, k=1)[0]
            # # # # # # # # # # # #

            #Blue Bird
            if bird_type == "blue":
                new_bird = Bird(1, spawn_points[0], spawn_points[1], blueSpeed, 1, 1, False,
                                True, random.choice([True, False]), random.choice([True, False]),
                                self.sprite_sheet_blue, self.SpritePerRow, self.SpriteWidth_Blue, self.SpriteHeight_Blue)
            #Red Bird
            elif bird_type == "red":
                new_bird = Bird(2, spawn_points[0], spawn_points[1], redSpeed, 1, 0.1, False,
                                True, random.choice([True, False]), random.choice([True, False]),
                                self.sprite_sheet_red, self.SpritePerRow, self.SpriteWidth_Red, self.SpriteHeight_Red)
            #Yellow Bird
            elif bird_type == "yellow":
                new_bird = Bird(10, spawn_points[0], spawn_points[1], yellowSpeed, 1, 1, False, True, random.choice([True, False]),
                                random.choice([True, False]),
                                self.sprite_sheet_yellow, self.SpritePerRow, self.SpriteWidth_Yellow, self.SpriteHeight_Yellow)
            #Black Bird
            elif bird_type == "black-fatty":
                new_bird = Bird(5, spawn_points[0], spawn_points[1], blackSpeed, blackHp, 1, False, True, random.choice([True, False]),
                                random.choice([True, False]),
                                self.sprite_sheet_BlackFatty, self.SpritePerRow, self.SpriteWidth_BlackFatty, self.SpriteHeight_BlackFatty)

            #Diagonally Bird
            elif bird_type == "diagonally":
                new_bird = Bird(7, self.ground_spawn_point[0], self.ground_spawn_point[1],
                                diagonallySpeed, 2, 99999, False,
                                True, True, False,
                                self.sprite_sheet_Diagonally, self.SpritePerRow, self.SpriteWidth_Diagonally, self.SpriteHeight_Diagonally)

            self.birds.append(new_bird)
            self.birdLevelCount -= 1

    def draw_game_state(self):
        # Video background
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.WIDTH, self.HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        self.screen.blit(frame_surface, (0, 0))

        # Draw birds
        for bird in self.birds:
            bird.draw(self.screen)

        # Draw HUD background (semi-transparent black rectangle)
        hud_height = self.HEIGHT // 10
        hud_surface = pygame.Surface((self.WIDTH, hud_height), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 150))  # Black with 150 alpha (semi-transparent)
        self.screen.blit(hud_surface, (0, self.HEIGHT - hud_height))

        # Draw HUD elements (centered)
        elapsed_time = time.time() - (self.start_time + self.total_paused_time)
        timer_text = self.my_font.render(f"Time: {max(0, int(self.level_timer - elapsed_time))}", False, (255, 255, 255))
        score_text = self.my_font.render(f"Score: {self.score}", False, (255, 255, 255))

        text_y = self.HEIGHT - hud_height // 2 - timer_text.get_height() // 2
        total_text_width = timer_text.get_width() + 50 + score_text.get_width()
        text_x = (self.WIDTH - total_text_width) // 2

        self.screen.blit(timer_text, (text_x, text_y))
        self.screen.blit(score_text, (text_x + timer_text.get_width() + 50, text_y))
        # Draw HUD controls text
        controls_text = self.my_font.render("H - Help", False, (255, 255, 255))
        controls_x = 10
        controls_y = self.HEIGHT - hud_height + 10

        self.screen.blit(controls_text, (controls_x, controls_y))

        # Draw Ammo icons
        ammo = pygame.image.load('Assets/Hud/ammo.png')
        ammo = pygame.transform.scale(ammo, (self.WIDTH // 128, self.HEIGHT // 27))
        ammo_x_start = self.WIDTH - (self.ammo * (self.WIDTH * 0.012)) - (self.WIDTH * 0.02)
        ammo_y = self.HEIGHT - hud_height // 2 - ammo.get_height() // 2

        for i in range(self.ammo):
            self.screen.blit(ammo, (ammo_x_start + i * (self.WIDTH * 0.012), ammo_y))

        # Blink effect
        if pygame.time.get_ticks() - self.blink_time < self.blink_duration:
            self.screen.fill((255, 255, 255))

        # Draw scope
        mouse_x, mouse_y = pygame.mouse.get_pos()
        scope = pygame.image.load('Assets/Hud/scope.png')
        scope = pygame.transform.scale(scope, (self.WIDTH // 27.4, self.HEIGHT // 15.4))
        scope_rect = scope.get_rect(center=(mouse_x, mouse_y))
        self.screen.blit(scope, scope_rect)
        # Draw control hints if H is pressed

        if self.show_controls:
            controls_hint = [
                "ESC - Close game",
                "P - Pause",
                "M - Main Menu",
            ]

            hint_x = 10
            hint_y = 10

            for i, text in enumerate(controls_hint):
                hint_text = self.my_font.render(text, False, (0, 0, 0))
                self.screen.blit(hint_text, (hint_x, hint_y + i * 30))