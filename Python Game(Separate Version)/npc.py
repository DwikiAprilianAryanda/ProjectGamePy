# npc.py
import pygame

class NPC:
    def __init__(self, npc_positions):
        npc_positions = {
        0: (475, 465),  # Posisi NPC di Area 0
        1: (300, 465)   # Posisi NPC di Area 1 (ubah sesuai kebutuhan)
}
        self.sprite_sheet = pygame.image.load("assets/serigala.png")
        self.sprite_width = 32
        self.sprite_height = 64
        self.frame_count = 5
        self.current_frame = 0
        self.time_elapsed = 0
        self.animation_speed = 0.2
        self.positions = npc_positions
        self.x, self.y = self.positions[0]
        self.dialog_lines = ["Halo! Apa kabar?", "Cuaca hari ini sangat bagus!", "Aku sedang menunggu seseorang.", "Sampai jumpa lagi!"]
        self.dialog_index = 0
        self.show_dialog = False
        self.font = pygame.font.Font(None, 36)
        self.question_sprite_sheet = pygame.image.load("assets/question.png")
        self.question_sprite_width = 16
        self.question_sprite_height = 16
        self.question_frame_count = 5
        self.question_current_frame = 0
        self.question_time_elapsed = 0
        self.question_animation_speed = 0.1


    def animate(self):
        self.time_elapsed += 1 / 60
        if self.time_elapsed >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.time_elapsed = 0
        return self.sprite_sheet.subsurface((self.current_frame * self.sprite_width, 0, self.sprite_width, self.sprite_height))

    def animate_question(self):
        self.question_time_elapsed += 1 / 60
        if self.question_time_elapsed >= self.question_animation_speed:
            self.question_current_frame = (self.question_current_frame + 1) % self.question_frame_count
            self.question_time_elapsed = 0
        return pygame.transform.scale(
            self.question_sprite_sheet.subsurface((self.question_current_frame * self.question_sprite_width, 0, self.question_sprite_width, self.question_sprite_height)),
            (32, 32)
        )

    def update_position(self, current_area):
        self.x, self.y = self.positions[current_area]

    def interact(self, player_x, player_y, current_area):
        distance = ((player_x - self.x) ** 2 + (player_y - self.y) ** 2) ** 0.5
        if distance < 100 and not self.show_dialog:
            self.show_dialog = True
            self.dialog_index = 0
        elif distance < 100 and self.show_dialog:
            if self.dialog_index < len(self.dialog_lines) - 1:
                self.dialog_index += 1
            else:
                self.show_dialog = False

    def render_dialog(self, screen, player_x, player_y):
        distance = ((player_x - self.x) ** 2 + (player_y - self.y) ** 2) ** 0.5
        if distance < 100 and not self.show_dialog:  # Tampilkan ikon "E" jika dekat dan tidak ada dialog
            screen.blit(self.animate_question(), (self.x + self.sprite_width // 2 + 15, self.y - 10))
        
        if self.show_dialog:
            dialog_text = self.dialog_lines[self.dialog_index]
            dialog_surface = self.font.render(dialog_text, True, (255, 255, 255))
            dialog_rect = dialog_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
            dialog_bg = pygame.Surface((dialog_surface.get_width() + 20, dialog_surface.get_height() + 20))
            dialog_bg.fill((0, 0, 0))
            dialog_bg.set_alpha(128)
            screen.blit(dialog_bg, dialog_rect)
            screen.blit(dialog_surface, dialog_rect)
            
        