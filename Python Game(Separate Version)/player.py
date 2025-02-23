# player.py
import pygame

# Ukuran layar
WIDTH, HEIGHT = 800, 600

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite_sheet = pygame.image.load("assets/sara.png")
        self.sprite_width = 64
        self.sprite_height = 64
        self.frame_count = 9
        self.current_frame = 0
        self.moving_left = False
        self.is_jumping = False
        self.jump_velocity = 0
        self.jump_frame = 0
        self.jump_time_elapsed = 0
        self.jump_animation_speed = 0.1
        self.ground_y = 465
        self.speed = 5
        self.gravity = 0.5

    def animate(self):
        if self.is_jumping:
            self.jump_time_elapsed += 1 / 60
            if self.jump_time_elapsed >= self.jump_animation_speed:
                self.jump_frame = (self.jump_frame + 1) % self.frame_count
                self.jump_time_elapsed = 0
            frame_y = self.sprite_height * (2 if self.moving_left else 2)  # Baris 2 untuk lompat
            frame_x = self.jump_frame * self.sprite_width
        else:
            frame_y = self.sprite_height * (9 if self.moving_left else 11)
            frame_x = self.current_frame * self.sprite_width
        return self.sprite_sheet.subsurface((frame_x, frame_y, self.sprite_width, self.sprite_height))

    def update(self, keys, current_area):
        if self.is_jumping:
            self.y += self.jump_velocity
            self.jump_velocity += self.gravity
            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False
                self.jump_frame = 0
                self.jump_time_elapsed = 0
        
        if keys[pygame.K_LEFT] and not (current_area == 0 and self.x <= 0):
            self.x -= self.speed
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.moving_left = True
        elif keys[pygame.K_RIGHT] and not (current_area == 1 and self.x >= WIDTH - self.sprite_width):
            self.x += self.speed
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.moving_left = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = -10