import pygame

class Bird:
    def __init__(self, x, y, right, left, up, down, sprite_sheet, SpritePerRow, SpriteWidth, SpriteHeight):
        self.x = x
        self.y = y
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


    def check_collision(self, mouse_pos):
        if self.sprite_rect.collidepoint(mouse_pos):
            return True

    def get_frame(self):
        row = self.current_frame // self.SpritePerRow
        col = self.current_frame % self.SpritePerRow
        x = col * self.SpriteWidth
        y = row * self.SpriteHeight
        return self.sprite_sheet.subsurface(pygame.Rect(x, y, self.SpriteWidth, self.SpriteHeight))

    def update(self, birdSpeed, screen):
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

        if self.right:
            self.x -= birdSpeed * 3
        if self.left:
            self.x += birdSpeed * 3
        if self.up:
            self.y -= birdSpeed
        if self.down:
            self.y += birdSpeed

        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % (self.SpritePerRow * (self.sprite_sheet.get_height() // self.SpriteHeight))

        self.sprite_rect = pygame.Rect(self.x, self.y, self.SpriteWidth, self.SpriteHeight)

    def draw(self, screen):
        current_image = self.get_frame()
        if self.flipped:
            current_image = pygame.transform.flip(current_image, True, False)
        screen.blit(current_image, (self.x, self.y))
