import pygame
import sys
from flappy_bird import FlappyBirdGame, SCREEN_WIDTH, SCREEN_HEIGHT

class FlappyBirdVisualization(FlappyBirdGame):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird AI Visualization")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 36, bold=True)
    
    def draw_bird(self):
        """Draw a more detailed bird with rotation and animation"""
        # Create a surface for the bird
        bird_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        
        # Draw bird body
        pygame.draw.ellipse(bird_surface, (255, 204, 0), (0, 0, 30, 30))
        
        # Draw wing with animation
        wing_flap = 0
        if self.bird.flap_counter > 0:
            wing_flap = 5
        elif int(self.bird.animation_counter) % 2 == 0:
            wing_flap = 3
        else:
            wing_flap = 0
            
        wing_offset = wing_flap
        pygame.draw.ellipse(bird_surface, (255, 150, 0), 
                           (10, 15 - wing_offset, 15, 15))
        
        # Draw eye
        pygame.draw.circle(bird_surface, (0, 0, 0), (22, 13), 4)
        pygame.draw.circle(bird_surface, (255, 255, 255), (23, 12), 2)
        
        # Draw beak
        beak_points = [(25, 15), (35, 12), (35, 18)]
        pygame.draw.polygon(bird_surface, (255, 100, 0), beak_points)
        
        # Draw tail
        tail_points = [(0, 15), (-8, 10), (-8, 20)]
        pygame.draw.polygon(bird_surface, (255, 150, 0), tail_points)
        
        # Rotate and draw bird
        rotated_bird = pygame.transform.rotate(bird_surface, -self.bird.rotation)
        bird_rect = rotated_bird.get_rect(center=(self.bird.x + 15, self.bird.y + 15))
        self.screen.blit(rotated_bird, bird_rect.topleft)
    
    def draw_pipe(self, pipe):
        """Draw a more detailed pipe with caps and textures"""
        top_pipe, bottom_pipe = pipe.get_rects()
        
        # Draw pipe body with texture
        pygame.draw.rect(self.screen, pipe.top_pipe_color, top_pipe)
        pygame.draw.rect(self.screen, pipe.bottom_pipe_color, bottom_pipe)
        
        # Draw pipe caps
        cap_height = 15
        pygame.draw.rect(self.screen, pipe.cap_color, 
                        (top_pipe.x - 3, top_pipe.height - cap_height, 
                         56, cap_height))
        pygame.draw.rect(self.screen, pipe.cap_color, 
                        (bottom_pipe.x - 3, bottom_pipe.y, 
                         56, cap_height))
        
        # Draw pipe details
        for i in range(0, top_pipe.height, 20):
            pygame.draw.line(self.screen, (0, 80, 0), 
                            (top_pipe.x, top_pipe.y + i), 
                            (top_pipe.x + 50, top_pipe.y + i), 1)
        
        for i in range(0, bottom_pipe.height, 20):
            pygame.draw.line(self.screen, (0, 80, 0), 
                            (bottom_pipe.x, bottom_pipe.y + i), 
                            (bottom_pipe.x + 50, bottom_pipe.y + i), 1)
    
    def draw_score(self):
        """Draw the score with enhanced styling"""
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        shadow = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(shadow, (11, 11))
        self.screen.blit(score_text, (10, 10))
        
        # Draw score border
        score_rect = pygame.Rect(5, 5, score_text.get_width() + 10, score_text.get_height() + 10)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), score_rect, 2)
        pygame.draw.rect(self.screen, (100, 100, 100, 100), score_rect, 1)
    
    def draw_game_over(self):
        """Draw an enhanced game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.big_font.render("GAME OVER", True, (255, 50, 50))
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        restart_text = self.font.render("Press R to Restart", True, (200, 200, 100))
        
        # Draw text with borders
        game_over_rect = pygame.Rect(
            SCREEN_WIDTH//2 - game_over_text.get_width()//2 - 10,
            SCREEN_HEIGHT//2 - 70,
            game_over_text.get_width() + 20,
            game_over_text.get_height() + 10
        )
        pygame.draw.rect(self.screen, (50, 50, 50), game_over_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), game_over_rect, 2)
        self.screen.blit(game_over_text, 
                        (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                         SCREEN_HEIGHT//2 - 65))
        
        score_rect = pygame.Rect(
            SCREEN_WIDTH//2 - score_text.get_width()//2 - 10,
            SCREEN_HEIGHT//2 - 10,
            score_text.get_width() + 20,
            score_text.get_height() + 10
        )
        pygame.draw.rect(self.screen, (50, 50, 50), score_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), score_rect, 2)
        self.screen.blit(score_text, 
                        (SCREEN_WIDTH//2 - score_text.get_width()//2, 
                         SCREEN_HEIGHT//2 - 5))
        
        restart_rect = pygame.Rect(
            SCREEN_WIDTH//2 - restart_text.get_width()//2 - 10,
            SCREEN_HEIGHT//2 + 40,
            restart_text.get_width() + 20,
            restart_text.get_height() + 10
        )
        pygame.draw.rect(self.screen, (50, 50, 50), restart_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), restart_rect, 2)
        self.screen.blit(restart_text, 
                        (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                         SCREEN_HEIGHT//2 + 45))

# For visualization
if __name__ == "__main__":
    game = FlappyBirdVisualization()
    game.run()