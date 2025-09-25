import pygame
import random
import sys

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_POWER = -5
PIPE_SPEED = 3
PIPE_GAP = 150
BIRD_WIDTH = 30
BIRD_HEIGHT = 30
PIPE_WIDTH = 50

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.alive = True
        self.flap_counter = 0
        self.rotation = 0
        self.animation_counter = 0
    
    def flap(self):
        self.velocity = FLAP_POWER
        self.flap_counter = 5
    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Rotate bird based on velocity
        self.rotation = max(-30, min(self.velocity * 2, 90))
        
        # Update flap animation
        if self.flap_counter > 0:
            self.flap_counter -= 1
        
        # Animation counter for wing flapping
        self.animation_counter = (self.animation_counter + 0.2) % 10
        
        # Check boundaries
        if self.y <= 0:
            self.y = 0
            self.velocity = 0
        if self.y >= SCREEN_HEIGHT - BIRD_HEIGHT:
            self.y = SCREEN_HEIGHT - BIRD_HEIGHT
            self.alive = False
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)
    
    def is_alive(self):
        return self.alive

class Pipe:
    def __init__(self):
        self.gap_y = random.randint(100, SCREEN_HEIGHT - 100 - PIPE_GAP)
        self.x = SCREEN_WIDTH
        self.passed = False
        self.color = (34, 139, 34)  # Forest green
        self.top_pipe_color = (34, 139, 34)
        self.bottom_pipe_color = (34, 139, 34)
        self.cap_color = (0, 100, 0)
    
    def update(self):
        self.x -= PIPE_SPEED
    
    def get_rects(self):
        # Top pipe
        top_pipe = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y)
        # Bottom pipe
        bottom_pipe = pygame.Rect(self.x, self.gap_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (self.gap_y + PIPE_GAP))
        return top_pipe, bottom_pipe
    
    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 36, bold=True)
        
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.background_x = 0
        self.clouds = []
        self.generate_clouds()
        
        # Add initial pipe
        self.pipes.append(Pipe())
        
        # Timer for adding new pipes
        self.pipe_timer = 0
    
    def generate_clouds(self):
        """Generate initial clouds"""
        self.clouds = []
        for i in range(5):
            self.clouds.append([
                random.randint(0, SCREEN_WIDTH),
                random.randint(20, 150),
                random.randint(30, 60),  # width
                random.randint(20, 40),  # height
                random.uniform(0.2, 0.5)  # speed
            ])
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.bird.flap()
                if event.key == pygame.K_r and self.game_over:
                    self.restart_game()
    
    def update(self):
        if self.game_over:
            return
        
        # Update bird
        self.bird.update()
        
        # Check if bird is dead
        if not self.bird.is_alive():
            self.game_over = True
            return
        
        # Update pipes
        for pipe in self.pipes:
            pipe.update()
        
        # Remove off-screen pipes
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]
        
        # Add new pipes
        self.pipe_timer += 1
        if self.pipe_timer >= 100:  # Add a new pipe every 100 frames
            self.pipes.append(Pipe())
            self.pipe_timer = 0
        
        # Check for collisions and scoring
        bird_rect = self.bird.get_rect()
        for pipe in self.pipes:
            top_pipe, bottom_pipe = pipe.get_rects()
            
            # Check collision
            if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
                self.game_over = True
                return
            
            # Check if bird passed the pipe
            if not pipe.passed and pipe.x + PIPE_WIDTH < self.bird.x:
                pipe.passed = True
                self.score += 1
    
    def draw_background(self):
        """Draw a beautiful sky background with clouds"""
        # Sky gradient
        for y in range(SCREEN_HEIGHT):
            color_value = 135 + int(121 * (y / SCREEN_HEIGHT))
            color = (135, 190 + int(46 * (y / SCREEN_HEIGHT)), color_value)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Draw sun
        pygame.draw.circle(self.screen, (255, 255, 200), (SCREEN_WIDTH - 50, 50), 30)
        
        # Draw clouds
        for cloud in self.clouds:
            x, y, width, height, speed = cloud
            pygame.draw.ellipse(self.screen, (250, 250, 250), (x, y, width, height))
            pygame.draw.ellipse(self.screen, (250, 250, 250), (x + 10, y - 10, width - 10, height))
            pygame.draw.ellipse(self.screen, (250, 250, 250), (x + 15, y + 5, width - 15, height))
            
            # Move cloud
            cloud[0] -= speed
            if cloud[0] < -100:
                cloud[0] = SCREEN_WIDTH + 20
                cloud[1] = random.randint(20, 150)
    
    def draw_ground(self):
        """Draw a grassy ground"""
        # Ground
        pygame.draw.rect(self.screen, (165, 42, 42), (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20))
        
        # Grass
        for i in range(0, SCREEN_WIDTH, 5):
            height = random.randint(5, 15)
            pygame.draw.line(self.screen, (34, 139, 34), 
                            (i, SCREEN_HEIGHT - 20), 
                            (i, SCREEN_HEIGHT - 20 - height), 2)
    
    def draw_bird(self):
        """Draw a detailed bird with rotation"""
        # Create a surface for the bird
        bird_surface = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT), pygame.SRCALPHA)
        
        # Draw bird body
        pygame.draw.ellipse(bird_surface, (255, 204, 0), (0, 0, BIRD_WIDTH, BIRD_HEIGHT))
        
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
                           (BIRD_WIDTH//3, BIRD_HEIGHT//2 - wing_offset, 
                            BIRD_WIDTH//2, BIRD_HEIGHT//2))
        
        # Draw eye
        pygame.draw.circle(bird_surface, (0, 0, 0), (BIRD_WIDTH - 8, BIRD_HEIGHT//2 - 2), 4)
        pygame.draw.circle(bird_surface, (255, 255, 255), (BIRD_WIDTH - 7, BIRD_HEIGHT//2 - 3), 2)
        
        # Draw beak
        beak_points = [(BIRD_WIDTH - 5, BIRD_HEIGHT//2), 
                      (BIRD_WIDTH + 5, BIRD_HEIGHT//2 - 3),
                      (BIRD_WIDTH + 5, BIRD_HEIGHT//2 + 3)]
        pygame.draw.polygon(bird_surface, (255, 100, 0), beak_points)
        
        # Rotate and draw bird
        rotated_bird = pygame.transform.rotate(bird_surface, -self.bird.rotation)
        bird_rect = rotated_bird.get_rect(center=(self.bird.x + BIRD_WIDTH//2, 
                                                 self.bird.y + BIRD_HEIGHT//2))
        self.screen.blit(rotated_bird, bird_rect.topleft)
    
    def draw_pipe(self, pipe):
        """Draw a detailed pipe with caps"""
        top_pipe, bottom_pipe = pipe.get_rects()
        
        # Draw pipe body
        pygame.draw.rect(self.screen, pipe.top_pipe_color, top_pipe)
        pygame.draw.rect(self.screen, pipe.bottom_pipe_color, bottom_pipe)
        
        # Draw pipe caps
        cap_height = 15
        pygame.draw.rect(self.screen, pipe.cap_color, 
                        (top_pipe.x - 3, top_pipe.height - cap_height, 
                         PIPE_WIDTH + 6, cap_height))
        pygame.draw.rect(self.screen, pipe.cap_color, 
                        (bottom_pipe.x - 3, bottom_pipe.y, 
                         PIPE_WIDTH + 6, cap_height))
    
    def draw_score(self):
        """Draw the score with shadow effect"""
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        shadow = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(shadow, (11, 11))
        self.screen.blit(score_text, (10, 10))
    
    def draw_game_over(self):
        """Draw the game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.big_font.render("GAME OVER", True, (255, 50, 50))
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        restart_text = self.font.render("Press R to Restart", True, (200, 200, 100))
        
        self.screen.blit(game_over_text, 
                        (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                         SCREEN_HEIGHT//2 - 50))
        self.screen.blit(score_text, 
                        (SCREEN_WIDTH//2 - score_text.get_width()//2, 
                         SCREEN_HEIGHT//2))
        self.screen.blit(restart_text, 
                        (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                         SCREEN_HEIGHT//2 + 50))
    
    def draw(self):
        """Enhanced draw method"""
        self.draw_background()
        
        # Draw pipes
        for pipe in self.pipes:
            self.draw_pipe(pipe)
        
        # Draw ground
        self.draw_ground()
        
        # Draw bird
        self.draw_bird()
        
        # Draw score
        self.draw_score()
        
        # Draw game over message
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def restart_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.pipes.append(Pipe())
        self.pipe_timer = 0
        self.generate_clouds()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

# For manual play testing
if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()