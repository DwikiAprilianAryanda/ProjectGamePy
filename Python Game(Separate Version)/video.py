# video.py
import pygame
import cv2
import numpy as np

class VideoOpening:
    def __init__(self):
        self.video_files = ["assets/opening.mp4", "assets/opening1.mp4"]
        self.current_video = 0

    def play_single_video(self, screen, clock, video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Tidak dapat membuka video {video_path}")
            return True
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (screen.get_width(), screen.get_height()))
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            
            screen.blit(frame, (0, 0))
            font = pygame.font.Font(None, 36)
            skip_text = font.render("Press SPACE to skip", True, (255, 255, 255))
            screen.blit(skip_text, (screen.get_width() - 525, screen.get_height() - 50))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    cap.release()
                    return True
            
            clock.tick(60)
        
        cap.release()
        return True

    def play_all_videos(self, screen, clock):
        while self.current_video < len(self.video_files):
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 36)
            loading_text = font.render(f"Loading Video {self.current_video + 1}...", True, (255, 255, 255))
            screen.blit(loading_text, (screen.get_width() // 2 - 100, screen.get_height() // 2))
            pygame.display.flip()
            
            if not self.play_single_video(screen, clock, self.video_files[self.current_video]):
                return False
            
            self.current_video += 1
            if self.current_video < len(self.video_files):
                fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
                fade_surface.fill((0, 0, 0))
                for alpha in range(0, 255, 5):
                    fade_surface.set_alpha(alpha)
                    screen.blit(fade_surface, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(5)
        
        return True