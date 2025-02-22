import pygame
import random
from pygame import mixer
import os
import cv2
import numpy as np
import math

# Inisialisasi pygame
pygame.init()
mixer.init()

# Ukuran layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game dengan Interaksi NPC dan Barang")

# State untuk mengontrol video opening
class GameState:
    OPENING = 0
    PLAYING = 1

# Load gambar background untuk tiap area
backgrounds = {
    0: pygame.transform.scale(pygame.image.load("assets/background2.png"), (WIDTH, HEIGHT)),
    1: pygame.transform.scale(pygame.image.load("assets/background.png"), (WIDTH, HEIGHT))
}

# Sprite karakter
sprite_sheet = pygame.image.load("assets/sara.png")  
sprite_width = 64
sprite_height = 64
frame_count = 9

# Sprite NPC
npc_sprite_sheet = pygame.image.load("assets/serigala.png")  
npc_sprite_width = 32
npc_sprite_height = 64
npc_frame_count = 5

# Sprite Question (ikon animasi "E")
question_sprite_sheet = pygame.image.load("assets/question.png")  
question_sprite_width = 16
question_sprite_height = 16
question_frame_count = 5

# Sprite chest
chest_sprite_sheet = pygame.image.load("assets/chest.png")  
chest_sprite_width = 32
chest_sprite_height = 32
chest_frame_count = 10

# Variabel untuk lompat
is_jumping = False
jump_velocity = 0
gravity = 0.5
ground_y = 465  # Posisi karakter di tanah

# Gambar hadiah
reward_images = {
    "Koin Emas": pygame.image.load("assets/coin.png"), 
    "Pedang": pygame.image.load("assets/sword.png"),
    "Potion": pygame.image.load("assets/potion.gif"),
    "Pakaian Baru": pygame.image.load("assets/egg.png")
}

# Posisi awal karakter dan area
x, y = 0, 465
speed = 5
current_area = 0

npc_positions = {
    0: (475, 465),  # Posisi NPC di Area 0
    1: (300, 465)   # Posisi NPC di Area 1 (ubah sesuai kebutuhan)
}

# Posisi Chest
chest_positions = {
    0: (300, 500),
    1: (400, 500)
}

# Inventori
inventory = {"Koin Emas": 0, "Pedang": 0, "Potion": 0, "Pakaian Baru": 0}
show_inventory = False
inventory_font = pygame.font.Font(None, 24)
inventory_slot_size = 50  # Ukuran slot inventori
inventory_padding = 10

# Animasi karakter
current_frame = 0
moving_left = False

# Animasi NPC
npc_current_frame = 0
npc_time_elapsed = 0
npc_animation_speed = 0.2

# Animasi Question
question_current_frame = 0
question_time_elapsed = 0
question_animation_speed = 0.1

# Animasi chest
chest_current_frame = 0
chest_time_elapsed = 0
chest_animation_speed = 0.1
chest_opening = False
chest_opened = False

# Animasi reward
reward_y_offset = 0
reward_scale = 1.0
reward_animating = False
reward_rotation = 0  # Untuk rotasi koin
reward_shake_offset = 0  # Untuk getaran pedang
reward_float_offset = 0  # Untuk mengapung potion
reward_pulse_scale = 1.0  # Untuk pulse pakaian
reward_animation_time = 0  # Waktu animasi berjalan

# State untuk chest di tiap area
chests_state = {
    0: {"opened": False, "animating": False, "frame": 0, "opened_time": None},
    1: {"opened": False, "animating": False, "frame": 0, "opened_time": None}
}

# Font untuk teks interaksi
font = pygame.font.Font(None, 36)

# Dialog NPC
dialog_lines = ["Halo! Apa kabar?", "Cuaca hari ini sangat bagus!", "Aku sedang menunggu seseorang.", "Sampai jumpa lagi!"]
dialog_index = 0
show_dialog = False

# Hadiah
reward = None
reward_time = 0
reward_display_duration = 2000

current_state = GameState.OPENING

class VideoOpening:
    def __init__(self):
        # Daftar video yang akan diputar
        self.video_files = [
            "assets/opening.mp4",
            "assets/opening1.mp4", # Tambahkan file video sesuai kebutuhan
        ]
        self.current_video = 0
        
    def play_single_video(self, video_path):
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                print(f"Error: Tidak dapat membuka video {video_path}")
                return True
                
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Convert frame dari BGR ke RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Resize frame ke ukuran window
                frame = cv2.resize(frame, (WIDTH, HEIGHT))
                # Convert ke format Pygame
                frame = np.rot90(frame)
                frame = pygame.surfarray.make_surface(frame)
                
                screen.blit(frame, (0,0))
                
                # Tampilkan informasi video
                font = pygame.font.Font(None, 36)
                skip_text = font.render("Press SPACE to skip", True, (255, 255, 255))
                
                screen.blit(skip_text, (WIDTH - 525, HEIGHT - 50))
                
                pygame.display.flip()
                
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        cap.release()
                        return False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            cap.release()
                            return True
                            
                clock.tick(60)  # Control frame rate
                
            cap.release()
            return True
            
        except Exception as e:
            print(f"Error playing video {video_path}: {e}")
            return True
            
    def play_all_videos(self):
        try:
            while self.current_video < len(self.video_files):
                # Tampilkan loading screen
                screen.fill((0, 0, 0))
                font = pygame.font.Font(None, 36)
                loading_text = font.render(f"Loading Video {self.current_video + 1}...", True, (255, 255, 255))
                screen.blit(loading_text, (WIDTH//2 - 100, HEIGHT//2))
                pygame.display.flip()
                
                # Putar video current
                if not self.play_single_video(self.video_files[self.current_video]):
                    return False
                    
                self.current_video += 1
                
                # Tampilkan transisi antar video
                if self.current_video < len(self.video_files):
                    self.show_transition()
                    
            return True
            
        except Exception as e:
            print(f"Error in video sequence: {e}")
            return True
            
    def show_transition(self):
        # Efek fade hitam sederhana
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        
        for alpha in range(0, 255, 5):
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(5)

# Modifikasi fungsi play_opening_video
def play_opening_video():
    video_player = VideoOpening()
    return video_player.play_all_videos()

def animate_character():
    frame_y = sprite_height * (9 if moving_left else 11)
    frame_x = current_frame * sprite_width
    return sprite_sheet.subsurface((frame_x, frame_y, sprite_width, sprite_height))

def animate_npc():
    global npc_current_frame, npc_time_elapsed
    npc_time_elapsed += 1 / 60
    if npc_time_elapsed >= 0.2:
        npc_current_frame = (npc_current_frame + 1) % npc_frame_count
        npc_time_elapsed = 0
    return npc_sprite_sheet.subsurface((npc_current_frame * npc_sprite_width, 0, npc_sprite_width, npc_sprite_height))

def animate_question():
    global question_current_frame, question_time_elapsed
    question_time_elapsed += 1 / 60
    if question_time_elapsed >= 0.1:
        question_current_frame = (question_current_frame + 1) % question_frame_count
        question_time_elapsed = 0
    return question_sprite_sheet.subsurface((question_current_frame * question_sprite_width, 0, question_sprite_width, question_sprite_height))

def animate_chest(area):
    chest_state = chests_state[area]
    if chest_state["animating"]:
        if chest_state["frame"] < chest_frame_count - 1:
            chest_state["frame"] += 1
        else:
            chest_state["animating"] = False
            chest_state["opened"] = True
    
    frame_x = chest_state["frame"] * chest_sprite_width
    return chest_sprite_sheet.subsurface((frame_x, 0, chest_sprite_width, chest_sprite_height))

def open_chest(area):
    if not chests_state[area]["opened"] and not chests_state[area]["animating"]:
        chests_state[area]["animating"] = True
        chests_state[area]["frame"] = 0
        global reward, reward_time, reward_y_offset, reward_scale, reward_animating
        global reward_rotation, reward_shake_offset, reward_float_offset, reward_pulse_scale, reward_animation_time
        reward = random.choice(list(reward_images.keys()))
        reward_time = pygame.time.get_ticks()
        reward_y_offset = 0
        reward_scale = 0.5
        reward_animating = True
        reward_rotation = 0
        reward_shake_offset = 0
        reward_float_offset = 0
        reward_pulse_scale = 1.0
        reward_animation_time = 0
        # Catat waktu saat chest dibuka
        chests_state[area]["opened_time"] = pygame.time.get_ticks()
        
def animate_reward(reward_name, reward_image, elapsed_time):
    global reward_y_offset, reward_scale, reward_animating
    global reward_rotation, reward_shake_offset, reward_float_offset, reward_pulse_scale, reward_animation_time
    
    reward_animation_time = elapsed_time / 1000  # Konversi ke detik
    
    # Animasi naik dasar untuk semua reward
    animation_duration = 0.5  # 500ms untuk naik
    if elapsed_time < animation_duration * 1000:
        progress = elapsed_time / (animation_duration * 1000)
        reward_y_offset = -50 * progress
        reward_scale = 0.5 + (0.5 * progress)
    else:
        reward_y_offset = -50
        reward_scale = 1.0
    
    # Animasi khusus untuk setiap reward
    transformed_image = reward_image
    
    if reward_name == "Koin Emas":
        reward_float_offset = 10 * math.sin(reward_animation_time * 2)
        # Animasi rotasi
        # reward_rotation = (reward_animation_time * 360) % 360  # Rotasi penuh
        # transformed_image = pygame.transform.rotate(reward_image, reward_rotation)
    
    elif reward_name == "Pedang":
        reward_float_offset = 10 * math.sin(reward_animation_time * 2)
        # Animasi getar
        # reward_shake_offset = 5 * math.sin(reward_animation_time * 15)  # Frekuensi getaran
    
    elif reward_name == "Potion":
        # Animasi mengapung
        reward_float_offset = 10 * math.sin(reward_animation_time * 2)  # Naik-turun lambat
    
    elif reward_name == "Pakaian Baru":
        reward_float_offset = 10 * math.sin(reward_animation_time * 2)
        # Animasi pulse
        # reward_pulse_scale = 1.0 + 0.2 * math.sin(reward_animation_time * 5)  # Membesar-men kecil
    
    # Terapkan transformasi
    scaled_width = int(transformed_image.get_width() * reward_scale * reward_pulse_scale)
    scaled_height = int(transformed_image.get_height() * reward_scale * reward_pulse_scale)
    scaled_reward = pygame.transform.scale(transformed_image, (scaled_width, scaled_height))
    
    # Hitung posisi
    reward_x = (WIDTH - scaled_width) // 2 + reward_shake_offset
    reward_y = (HEIGHT - scaled_height) // 2 + reward_y_offset + reward_float_offset
    
    return scaled_reward, (reward_x, reward_y)

def render_inventory():
    if show_inventory:
        # Background inventori
        inventory_width = (inventory_slot_size + inventory_padding) * 4 + inventory_padding
        inventory_height = inventory_slot_size + inventory_padding * 2 + 30  # +30 untuk teks jumlah
        inventory_bg = pygame.Surface((inventory_width, inventory_height))
        inventory_bg.fill((50, 50, 50))
        inventory_bg.set_alpha(200)
        inventory_x = (WIDTH - inventory_width) // 2
        inventory_y = (HEIGHT - inventory_height) // 2
        screen.blit(inventory_bg, (inventory_x, inventory_y))

        # Render setiap item
        for i, (item_name, count) in enumerate(inventory.items()):
            slot_x = inventory_x + inventory_padding + i * (inventory_slot_size + inventory_padding)
            slot_y = inventory_y + inventory_padding
            
            # Gambar item
            item_image = pygame.transform.scale(reward_images[item_name], (inventory_slot_size, inventory_slot_size))
            screen.blit(item_image, (slot_x, slot_y))
            
            # Jumlah item
            count_text = inventory_font.render(f"x{count}", True, (255, 255, 255))
            screen.blit(count_text, (slot_x, slot_y + inventory_slot_size + 5))

def show_npc_dialog():
    global dialog_index, show_dialog
    if not show_dialog:
        show_dialog = True
        dialog_index = 0
    else:
        if dialog_index < len(dialog_lines) - 1:
            dialog_index += 1
        else:
            show_dialog = False

# Game loop
running = True
clock = pygame.time.Clock()

npc_x, npc_y = npc_positions[current_area]

while running:
    if current_state == GameState.OPENING:
        if play_opening_video():
            current_state = GameState.PLAYING
        else:
            running = False
        continue
        
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                chest_x, chest_y = chest_positions[current_area]
                chest_distance = ((x - chest_x) ** 2 + (y - chest_y) ** 2) ** 0.5
                if chest_distance < 100:
                    open_chest(current_area)
                npc_x, npc_y = npc_positions[current_area]
                distance_to_npc = ((x - npc_x) ** 2 + (y - npc_y) ** 2) ** 0.5
                if distance_to_npc < 100:
                    show_npc_dialog()
            if event.key == pygame.K_UP and not is_jumping and not show_dialog:
                is_jumping = True
                jump_velocity = -10
            if event.key == pygame.K_i:  # Tombol 'I' untuk toggle inventori
                show_inventory = not show_inventory

    if is_jumping:
        y += jump_velocity  # Update posisi karakter secara vertikal
        jump_velocity += gravity  # Tambahkan gravitasi
        if y >= ground_y:  # Jika sudah menyentuh tanah
            y = ground_y
            is_jumping = False  # Reset status lompat
    
    if not show_dialog:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if not (current_area == 0 and x <= 0):  # Tambah batas kiri di Area 0
                x -= speed
                current_frame = (current_frame + 1) % frame_count
                moving_left = True
        elif keys[pygame.K_RIGHT]:
            if not (current_area == 1 and x >= WIDTH - 64):  # Tambah batas kanan di Area 1
                x += speed
                current_frame = (current_frame + 1) % frame_count
                moving_left = False

            
  # Cek perubahan area
    previous_area = current_area  # Simpan area sebelum berubah
    if x < 0 and current_area > 0:
        current_area -= 1
        x = WIDTH - 64  
    elif x > WIDTH - 64 and current_area < 1:
        current_area += 1
        x = 0  
    
    # Jika area berubah, perbarui posisi NPC
    if current_area != previous_area:
        npc_x, npc_y = npc_positions[current_area]  # Hanya ubah posisi saat pindah area

    # Cek respawn chest
    current_time = pygame.time.get_ticks()
    for area in chests_state:
        if chests_state[area]["opened"] and chests_state[area]["opened_time"]:
            time_since_opened = current_time - chests_state[area]["opened_time"]
            if time_since_opened >= 7000:  # 7 detik dalam milidetik
                chests_state[area]["opened"] = False
                chests_state[area]["animating"] = False
                chests_state[area]["frame"] = 0
                chests_state[area]["opened_time"] = None

    # Render game
    screen.blit(backgrounds[current_area], (0, 0))
    screen.blit(animate_character(), (x, y))
    screen.blit(animate_npc(), (npc_x, npc_y))

    # Render chest
    chest_x, chest_y = chest_positions[current_area]
    if not chests_state[current_area]["opened"]:
        screen.blit(animate_chest(current_area), (chest_x, chest_y))

    # Tampilkan ikon E jika dekat dengan NPC atau chest yang belum dibuka
    distance_to_npc = ((x - npc_x) ** 2 + (y - npc_y) ** 2) ** 0.5
    chest_distance = ((x - chest_x) ** 2 + (y - chest_y) ** 2) ** 0.5
    
    if (distance_to_npc < 100 and not show_dialog) or (chest_distance < 100 and not chests_state[current_area]["opened"]):
        question_frame = animate_question()
        question_frame = pygame.transform.scale(question_frame, (32, 32))
        if distance_to_npc < 100:
            screen.blit(question_frame, (npc_x + npc_sprite_width // 2 + 15, npc_y - 10))
        if chest_distance < 100 and not chests_state[current_area]["opened"]:
            screen.blit(question_frame, (chest_x + chest_sprite_width // 2, chest_y - 10))

    # Tampilkan reward
    if reward and pygame.time.get_ticks() - reward_time < reward_display_duration:
        reward_image = reward_images[reward]
        elapsed_time = pygame.time.get_ticks() - reward_time
        animated_reward, reward_pos = animate_reward(reward, reward_image, elapsed_time)
        screen.blit(animated_reward, reward_pos)
    elif reward:  # Reset saat reward hilang dan tambahkan ke inventori
        inventory[reward] += 1  # Tambahkan reward ke inventori
        reward = None
        reward_y_offset = 0
        reward_scale = 1.0
        reward_animating = False
        reward_rotation = 0
        reward_shake_offset = 0
        reward_float_offset = 0
        reward_pulse_scale = 1.0
        reward_animation_time = 0

    # Tampilkan dialog
    if show_dialog:
        dialog_text = dialog_lines[dialog_index]
        dialog_surface = font.render(dialog_text, True, (255, 255, 255))
        dialog_rect = dialog_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        
        dialog_bg = pygame.Surface((dialog_surface.get_width() + 20, dialog_surface.get_height() + 20))
        dialog_bg.fill((0, 0, 0))
        dialog_bg.set_alpha(128)
        screen.blit(dialog_bg, dialog_rect)
        screen.blit(dialog_surface, dialog_rect)

    # Render inventori
    render_inventory()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
