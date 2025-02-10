import pygame
from Birds import Bird
import random
import time
import cv2
import sys

class Game:
    def __init__(self):
        self.start_time = None #it does nothing but don't touch it. Attribute warning
        self.running = None #it does nothing but don't touch it. Attribute warning
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.video_path = "Assets/Background/lvl1.mp4"
        self.cap = cv2.VideoCapture(self.video_path)
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)

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
        self.birdSpeed = 1
        self.spawn_point = [(-60, 0), (-60, 400), (self.WIDTH + 10, 400), (self.WIDTH + 10, 0)]
        self.ground_spawn_point = [0, 1000]
        self.birdLevelCount = 11 #how many birds can be on screen. Recommended number 9-13

        #Player stats
        self.level_timer = 40 #If you want to change time fo level, u need to make sure that background video length is >= level_timer
        self.score = 0
        self.blink_time = 0
        self.blink_duration = 100
        self.death_times = {}
        self.shootDelay = 500
        self.last_shot_time = 0
        self.ammo = 8

        #Initialize bird list
        self.birds = []

    #Function to start level
    def start_level(self):
        pygame.mouse.set_visible(False)
        self.running = True
        self.start_time = time.time()

        #Game loop
        while self.running:
            self.handle_events()
            self.update_game_state()
            self.draw_game_state()
            pygame.display.flip()
            self.clock.tick(self.level_timer)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(pygame.mouse.get_pos())

    def handle_mouse_click(self, mouse_pos):
       if self.ammo > 0:
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot_time >= self.shootDelay:
            for bird in self.birds:
                if bird.check_collision(mouse_pos):
                    self.blink_time = pygame.time.get_ticks()
                    bird.hp -= 1
                    bird.birdSpeed += 2
                    bird.frame_delay -= 2
                    if bird.hp <= 0:
                        bird.kill()
                        self.birdLevelCount += 1
                        self.death_times[bird] = pygame.time.get_ticks()
                        self.score += bird.value
                    break

            self.last_shot_time = current_time
            self.ammo -= 1

    def update_game_state(self):
        #Update game duration
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time >= 40:
            self.running = False
            pygame.mouse.set_visible(True)
            print(f"Game Over! Score: {self.score}")
            return

        #Remove birds that are dead for too long
        current_time = pygame.time.get_ticks()
        for bird in list(self.birds):
            if bird in self.death_times and current_time - self.death_times[bird] >= 3000:
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
            if current_time - self.last_shot_time >= 3000:
                self.ammo = 5
            return

    def spawn_bird(self):
        spawn_points = random.choice(self.spawn_point)

        if self.birdLevelCount > 0:
            bird_types = ["blue", "red", "yellow", "black-fatty", "diagonally"]
            spawn_weight = [50, 30, 10, 9, 1] # birds rarity

            bird_type = random.choices(bird_types, weights = spawn_weight, k= 1)[0]

            new_bird = None #it does nothing but don't touch it, or you will get "reference" warning

            #Blue Bird
            if bird_type == "blue":
                new_bird = Bird(1, spawn_points[0], spawn_points[1], random.choice([0.75, 1, 1.25, 1.5]), 1, 1, False,
                                True, random.choice([True, False]), random.choice([True, False]),
                                self.sprite_sheet_blue, self.SpritePerRow, self.SpriteWidth_Blue, self.SpriteHeight_Blue)
            #Red Bird
            elif bird_type == "red":
                new_bird = Bird(2, spawn_points[0], spawn_points[1], 3, 1, 0.1, False,
                                True, random.choice([True, False]), random.choice([True, False]),
                                self.sprite_sheet_red, self.SpritePerRow, self.SpriteWidth_Red, self.SpriteHeight_Red)
            #Yellow Bird
            elif bird_type == "yellow":
                new_bird = Bird(10, spawn_points[0], spawn_points[1], 9, 1, 1, False, True, random.choice([True, False]),
                                random.choice([True, False]),
                                self.sprite_sheet_yellow, self.SpritePerRow, self.SpriteWidth_Yellow, self.SpriteHeight_Yellow)
            #Black Bird
            elif bird_type == "black-fatty":
                new_bird = Bird(5, spawn_points[0], spawn_points[1], 0.4, 3, 1, False, True, random.choice([True, False]),
                                random.choice([True, False]),
                                self.sprite_sheet_BlackFatty, self.SpritePerRow, self.SpriteWidth_BlackFatty, self.SpriteHeight_BlackFatty)

            #Diagonally Bird
            elif bird_type == "diagonally":
                new_bird = Bird(7, self.ground_spawn_point[0], self.ground_spawn_point[1],
                                2, 2, 99999, False,
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

        # Draw HUD
        padding = self.WIDTH * 0.007  # Відступ між елементами
        score_text = self.my_font.render("Score: " + str(self.score), False, (0, 0, 0))
        timer_text = self.my_font.render("Time: " + str(int(self.level_timer - (time.time() - self.start_time))), False,
                                         (0, 0, 0))

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(timer_text, (10, 10 + score_text.get_height() + padding))

        # Draw Ammo
        ammo = pygame.image.load('Assets/Hud/ammo.png')
        ammo = pygame.transform.scale(ammo, (self.WIDTH // 128, self.HEIGHT // 27))

        ammo_y = 10 + score_text.get_height() + timer_text.get_height() + 2 * padding
        for i in range(self.ammo):
            self.screen.blit(ammo, (10 + i * (self.WIDTH * 0.012), ammo_y))

        # Blink effect
        if pygame.time.get_ticks() - self.blink_time < self.blink_duration:
            self.screen.fill((255, 255, 255))

        # Draw scope
        mouse_x, mouse_y = pygame.mouse.get_pos()
        scope = pygame.image.load('Assets/Hud/scope.png')
        scope = pygame.transform.scale(scope, (self.WIDTH // 27.4, self.HEIGHT // 15.4))
        scope_rect = scope.get_rect(center=(mouse_x, mouse_y))
        self.screen.blit(scope, scope_rect)