# inventory.py
import pygame

class Inventory:
    def __init__(self, reward_images):
        self.items = {"Koin Emas": 0, "Pedang": 0, "Potion": 0, "Pakaian Baru": 0}
        self.show = False
        self.font = pygame.font.Font(None, 24)
        self.slot_size = 50
        self.padding = 10
        self.reward_images = reward_images

    def toggle(self):
        self.show = not self.show

    def add_item(self, item_name):
        self.items[item_name] += 1

    def render(self, screen):
        if self.show:
            inventory_width = (self.slot_size + self.padding) * 4 + self.padding
            inventory_height = self.slot_size + self.padding * 2 + 30
            inventory_bg = pygame.Surface((inventory_width, inventory_height))
            inventory_bg.fill((50, 50, 50))
            inventory_bg.set_alpha(200)
            inventory_x = (screen.get_width() - inventory_width) // 2
            inventory_y = (screen.get_height() - inventory_height) // 2
            screen.blit(inventory_bg, (inventory_x, inventory_y))

            for i, (item_name, count) in enumerate(self.items.items()):
                slot_x = inventory_x + self.padding + i * (self.slot_size + self.padding)
                slot_y = inventory_y + self.padding
                item_image = pygame.transform.scale(self.reward_images[item_name], (self.slot_size, self.slot_size))
                screen.blit(item_image, (slot_x, slot_y))
                count_text = self.font.render(f"x{count}", True, (255, 255, 255))
                screen.blit(count_text, (slot_x, slot_y + self.slot_size + 5))