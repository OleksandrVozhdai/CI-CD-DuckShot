from operator import truediv

import pygame
import random
import time

class Bird:
    def __init__(self, value, x, y, speed, hp, DirectionTimeChange, right, left, up, down, sprite_sheet, SpritePerRow, SpriteWidth, SpriteHeight):
        self.value = value
        self.x = x
        self.y = y
        self.hp = hp
        self.birdSpeed = speed
        self.current_frame = 0
        self.frame_delay = 5
        self.frame_timer = 0
        self.flipped = False
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.sprite_sheet = sprite_sheet
        self.SpritePerRow = SpritePerRow
        self.SpriteWidth = SpriteWidth
        self.SpriteHeight = SpriteHeight
        self.sprite_rect = pygame.Rect(self.x, self.y, SpriteWidth, SpriteHeight)
        self.DirChoice = 1
        self.last_choice_time = time.time()
        self.gravity = 2
        self.alive = True
        self.frozen_frame = None
        self.DirectionTimeChange = DirectionTimeChange

    def check_collision(self, mouse_pos):
        if self.alive:
            if self.sprite_rect.collidepoint(mouse_pos):
                return True

    def get_frame(self):
        row = self.current_frame // self.SpritePerRow
        col = self.current_frame % self.SpritePerRow
        x = col * self.SpriteWidth
        y = row * self.SpriteHeight
        return self.sprite_sheet.subsurface(pygame.Rect(x, y, self.SpriteWidth, self.SpriteHeight))


    def update(self, screen):
        if self.alive:
            current_time = time.time()

            if self.x < -400:
                self.flipped = False
                self.right = False
                self.left = True
            if self.x >= 1900:
                self.flipped = True
                self.right = True
                self.left = False
            if self.y < 0:
                self.up = False
                self.down = True
            if self.y >= 650:
                self.up = True
                self.down = False

            if current_time - self.last_choice_time >= self.DirectionTimeChange: #change direction every 1 second
                self.DirChoice = random.choice([-1, 1])
                self.last_choice_time = current_time

            if self.right:
                self.x -= self.birdSpeed * 3
            if self.left:
                self.x += self.birdSpeed * 3
            if self.up:
                self.y -= self.birdSpeed * self.gravity * self.DirChoice
            if self.down:
                self.y += self.birdSpeed * self.DirChoice
        else:
            self.y += self.gravity * 4.5

        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % (self.SpritePerRow * (self.sprite_sheet.get_height() // self.SpriteHeight))

        self.sprite_rect = pygame.Rect(self.x, self.y, self.SpriteWidth, self.SpriteHeight)

    def draw(self, screen):
        current_image = self.get_frame()
        if self.alive:
            if self.flipped:
                current_image = pygame.transform.flip(current_image, True, False)
        else:
            self.frame_delay = 1
            current_image = pygame.transform.flip(current_image, False, True)

        screen.blit(current_image, (self.x, self.y))
    def kill(self):
        self.alive = False