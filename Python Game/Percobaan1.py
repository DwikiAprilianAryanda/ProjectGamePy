import pygame
import random

# Inisialisasi pygame
pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game dengan Interaksi NPC dan Barang")

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
    "Pakaian Baru": pygame.image.load("assets/clothes.png")
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

# State untuk chest di tiap area
chests_state = {
    0: {"opened": False, "animating": False, "frame": 0},
    1: {"opened": False, "animating": False, "frame": 0}
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
        global reward, reward_time
        reward = random.choice(list(reward_images.keys()))
        reward_time = pygame.time.get_ticks()

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
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                # Cek jarak dengan chest
                chest_x, chest_y = chest_positions[current_area]
                chest_distance = ((x - chest_x) ** 2 + (y - chest_y) ** 2) ** 0.5
                if chest_distance < 100:
                    open_chest(current_area)
                # Cek jarak dengan NPC
                npc_x, npc_y = npc_positions[current_area]
                distance_to_npc = ((x - npc_x) ** 2 + (y - npc_y) ** 2) ** 0.5
                if distance_to_npc < 100:
                    show_npc_dialog()
            if event.key == pygame.K_UP and not is_jumping and not show_dialog:  # Lompat hanya jika di tanah
                is_jumping = True
                jump_velocity = -10  # Kecepatan awal lompat

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
        screen.blit(reward_image, (WIDTH // 2, HEIGHT // 2))
    else:
        reward = None

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

    pygame.display.update()
    clock.tick(60)

pygame.quit()
