# main.py
import pygame
import numpy as np
from player import Player
from npc import NPC
from chest import ChestSystem
from inventory import Inventory
from menu import Menu, InGameMenu
from video import VideoOpening

# Inisialisasi pygame
pygame.init()
pygame.mixer.init()

# Ukuran layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game dengan Interaksi NPC dan Barang")
clock = pygame.time.Clock()

# State game
class GameState:
    OPENING = 0
    MENU = 1
    PLAYING = 2
    INGAME_MENU = 3

# Load gambar background
backgrounds = {
    0: pygame.transform.scale(pygame.image.load("assets/background2.png"), (WIDTH, HEIGHT)),
    1: pygame.transform.scale(pygame.image.load("assets/background.png"), (WIDTH, HEIGHT))
}

# Load background music
pygame.mixer.music.load("assets/background_music.mp3")
pygame.mixer.music.set_volume(0.5)

reward_images = {  # Definisikan reward_images terlebih dahulu agar bisa digunakan berulang
    "Koin Emas": pygame.image.load("assets/coin.png"),
    "Pedang": pygame.image.load("assets/sword.png"),
    "Potion": pygame.image.load("assets/potion.gif"),
    "Pakaian Baru": pygame.image.load("assets/egg.png")
}

# Inisialisasi objek
inventory = Inventory(reward_images=reward_images)  # Buat instance inventory dulu
player = Player(0, 465)
npc = NPC(npc_positions={0: (475, 465), 1: (300, 465)})
chest_system = ChestSystem(chest_positions={0: (300, 500), 1: (400, 500)}, inventory=inventory)
menu = Menu()
ingame_menu = InGameMenu()
video = VideoOpening()

current_state = GameState.OPENING
current_area = 0
background_music_playing = False

def reset_game():
    global player, npc, chest_system, inventory, current_area, background_music_playing
    inventory = Inventory(reward_images=reward_images)  # Buat instance inventory dulu
    player = Player(0, 465)
    npc = NPC(npc_positions={0: (475, 465), 1: (300, 465)})
    chest_system = ChestSystem(chest_positions={0: (300, 500), 1: (400, 500)}, inventory=inventory)  # Pastikan inventory dilewatkan di reset
    current_area = 0
    if background_music_playing:
        pygame.mixer.music.stop()
        background_music_playing = False

# Game loop
running = True
while running:
    if current_state == GameState.OPENING:
        if video.play_all_videos(screen, clock):
            current_state = GameState.MENU
        else:
            running = False
    
    elif current_state == GameState.MENU:
        if background_music_playing:
            pygame.mixer.music.stop()
            background_music_playing = False
        action = menu.handle_menu(screen, clock)
        if action == "start":
            current_state = GameState.PLAYING
        elif action == "exit":
            running = False
    
    elif current_state == GameState.PLAYING:
        if not background_music_playing:
            pygame.mixer.music.play(-1)
            background_music_playing = True
        
        screen.blit(backgrounds[current_area], (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not npc.show_dialog:  # Hanya lompat jika tidak ada dialog
                    player.jump()
                if event.key == pygame.K_e:
                    chest_system.interact(player.x, player.y, current_area)
                    npc.interact(player.x, player.y, current_area)
                if event.key == pygame.K_i:
                    inventory.toggle()
                if event.key == pygame.K_ESCAPE:
                    current_state = GameState.INGAME_MENU

        keys = pygame.key.get_pressed()
        if not npc.show_dialog:
            player.update(keys, current_area)
        chest_system.update(current_area)
        
        if player.x < 0 and current_area > 0:
            current_area -= 1
            player.x = WIDTH - player.sprite_width
            npc.update_position(current_area)
        elif player.x > WIDTH - player.sprite_width and current_area < 1:
            current_area += 1
            player.x = 0
            npc.update_position(current_area)
        
        screen.blit(player.animate(), (player.x, player.y))
        screen.blit(npc.animate(), (npc.x, npc.y))
        chest_system.render(screen, current_area, player)
        inventory.render(screen)
        chest_system.render_reward(screen)
        npc.render_dialog(screen, player.x, player.y)
        pygame.display.update()
    
    elif current_state == GameState.INGAME_MENU:
        action = ingame_menu.handle_menu(screen, clock)
        if action == "resume":
            current_state = GameState.PLAYING
        elif action == "restart":
            reset_game()
            current_state = GameState.PLAYING
        elif action == "menu":
            reset_game()
            current_state = GameState.MENU
        elif action == "exit":
            running = False
    
    clock.tick(60)

if background_music_playing:
    pygame.mixer.music.stop()
pygame.quit()