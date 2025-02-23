# menu.py
import pygame

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)

    def render(self, screen, selected_option):
        screen.fill((0, 0, 0))
        title_text = self.font.render("Treasure Hunt Adventure", True, (255, 255, 255))
        screen.blit(title_text, title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4)))
        options = ["Start Game", "Exit"]
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_option else (255, 255, 255)
            option_text = self.font.render(option, True, color)
            screen.blit(option_text, option_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + i * 60)))
        pygame.display.update()

    def handle_menu(self, screen, clock):
        selected_option = 0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = max(0, selected_option - 1)
                    elif event.key == pygame.K_DOWN:
                        selected_option = min(1, selected_option + 1)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            return "start"
                        elif selected_option == 1:
                            return "exit"
            self.render(screen, selected_option)
            clock.tick(60)

class InGameMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)

    def render(self, screen, selected_option):
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        options = ["Resume", "Restart", "Back to Main Menu"]
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_option else (255, 255, 255)
            option_text = self.font.render(option, True, color)
            screen.blit(option_text, option_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + i * 60)))
        pygame.display.update()

    def handle_menu(self, screen, clock):
        selected_option = 0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = max(0, selected_option - 1)
                    elif event.key == pygame.K_DOWN:
                        selected_option = min(2, selected_option + 1)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            return "resume"
                        elif selected_option == 1:
                            return "restart"
                        elif selected_option == 2:
                            return "menu"
                    elif event.key == pygame.K_ESCAPE:
                        return "resume"
            self.render(screen, selected_option)
            clock.tick(60)