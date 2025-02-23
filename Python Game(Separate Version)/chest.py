# chest.py
import pygame
import random
import math
from inventory import Inventory
from player import Player

class ChestSystem:
    def __init__(self, chest_positions, inventory):
        self.sprite_sheet = pygame.image.load("assets/chest.png")
        self.sprite_width = 32
        self.sprite_height = 32
        self.frame_count = 10
        self.positions = chest_positions
        self.inventory = inventory  # Simpan instance inventory
        self.chests_state = {
            0: {"opened": False, "animating": False, "frame": 0, "opened_time": None},
            1: {"opened": False, "animating": False, "frame": 0, "opened_time": None}
        }
        self.reward = None
        self.reward_time = 0
        self.reward_display_duration = 2000
        self.reward_y_offset = 0
        self.reward_scale = 1.0
        self.reward_animating = False
        self.reward_rotation = 0
        self.reward_shake_offset = 0
        self.reward_float_offset = 0
        self.reward_pulse_scale = 1.0
        self.reward_animation_time = 0
        self.reward_images = {
            "Koin Emas": pygame.image.load("assets/coin.png"),
            "Pedang": pygame.image.load("assets/sword.png"),
            "Potion": pygame.image.load("assets/potion.gif"),
            "Pakaian Baru": pygame.image.load("assets/egg.png")
        }
        self.question_sprite_sheet = pygame.image.load("assets/question.png")
        self.question_sprite_width = 16
        self.question_sprite_height = 16
        self.question_frame_count = 5
        self.question_current_frame = 0
        self.question_time_elapsed = 0
        self.question_animation_speed = 0.1

    def animate_chest(self, area):
        chest_state = self.chests_state[area]
        if chest_state["animating"]:
            if chest_state["frame"] < self.frame_count - 1:
                chest_state["frame"] += 1
            else:
                chest_state["animating"] = False
                chest_state["opened"] = True
        frame_x = chest_state["frame"] * self.sprite_width
        return self.sprite_sheet.subsurface((frame_x, 0, self.sprite_width, self.sprite_height))

    def animate_question(self):
        self.question_time_elapsed += 1 / 60
        if self.question_time_elapsed >= self.question_animation_speed:
            self.question_current_frame = (self.question_current_frame + 1) % self.question_frame_count
            self.question_time_elapsed = 0
        return pygame.transform.scale(
            self.question_sprite_sheet.subsurface((self.question_current_frame * self.question_sprite_width, 0, self.question_sprite_width, self.question_sprite_height)),
            (32, 32)
        )

    def interact(self, player_x, player_y, area):
        chest_x, chest_y = self.positions[area]
        chest_distance = ((player_x - chest_x) ** 2 + (player_y - chest_y) ** 2) ** 0.5
        if chest_distance < 100 and not self.chests_state[area]["opened"] and not self.chests_state[area]["animating"]:
            self.chests_state[area]["animating"] = True
            self.chests_state[area]["frame"] = 0
            self.chests_state[area]["opened_time"] = pygame.time.get_ticks()
            self.reward = random.choice(list(self.reward_images.keys()))
            self.reward_time = pygame.time.get_ticks()
            self.reward_y_offset = 0
            self.reward_scale = 0.5
            self.reward_animating = True
            self.reward_rotation = 0
            self.reward_shake_offset = 0
            self.reward_float_offset = 0
            self.reward_pulse_scale = 1.0
            self.reward_animation_time = 0

    def update(self, area):
        current_time = pygame.time.get_ticks()
        if self.chests_state[area]["opened"] and self.chests_state[area]["opened_time"]:
            time_since_opened = current_time - self.chests_state[area]["opened_time"]
            if time_since_opened >= 7000:
                self.chests_state[area]["opened"] = False
                self.chests_state[area]["animating"] = False
                self.chests_state[area]["frame"] = 0
                self.chests_state[area]["opened_time"] = None

    def render(self, screen, area, player):
        chest_x, chest_y = self.positions[area]
        if not self.chests_state[area]["opened"]:
            screen.blit(self.animate_chest(area), (chest_x, chest_y))
            chest_distance = ((player.x - chest_x) ** 2 + (player.y - chest_y) ** 2) ** 0.5
            if chest_distance < 100:
                screen.blit(self.animate_question(), (chest_x + self.sprite_width // 2, chest_y - 10))

    def render_reward(self, screen):
        if self.reward and pygame.time.get_ticks() - self.reward_time < self.reward_display_duration:
            reward_image = self.reward_images[self.reward]
            elapsed_time = pygame.time.get_ticks() - self.reward_time
            self.reward_animation_time = elapsed_time / 1000
            animation_duration = 0.5
            if elapsed_time < animation_duration * 1000:
                progress = elapsed_time / (animation_duration * 1000)
                self.reward_y_offset = -50 * progress
                self.reward_scale = 0.5 + (0.5 * progress)
            else:
                self.reward_y_offset = -50
                self.reward_scale = 1.0
            
            if self.reward == "Koin Emas":
                self.reward_float_offset = 10 * math.sin(self.reward_animation_time * 2)
            elif self.reward == "Pedang":
                self.reward_float_offset = 10 * math.sin(self.reward_animation_time * 2)
            elif self.reward == "Potion":
                self.reward_float_offset = 10 * math.sin(self.reward_animation_time * 2)
            elif self.reward == "Pakaian Baru":
                self.reward_float_offset = 10 * math.sin(self.reward_animation_time * 2)
            
            scaled_width = int(reward_image.get_width() * self.reward_scale * self.reward_pulse_scale)
            scaled_height = int(reward_image.get_height() * self.reward_scale * self.reward_pulse_scale)
            scaled_reward = pygame.transform.scale(reward_image, (scaled_width, scaled_height))
            reward_x = (screen.get_width() - scaled_width) // 2 + self.reward_shake_offset
            reward_y = (screen.get_height() - scaled_height) // 2 + self.reward_y_offset + self.reward_float_offset
            screen.blit(scaled_reward, (reward_x, reward_y))
        elif self.reward:
            print(f"Adding item: {self.reward}")
            self.inventory.add_item(self.reward)
            self.reward = None
            self.reward_y_offset = 0
            self.reward_scale = 1.0
            self.reward_animating = False
            self.reward_rotation = 0
            self.reward_shake_offset = 0
            self.reward_float_offset = 0
            self.reward_pulse_scale = 1.0
            self.reward_animation_time = 0