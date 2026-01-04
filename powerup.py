
import pygame
import random

class PowerUp:
    TYPES = ['double', 'shield', 'slow']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(self.TYPES)
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 2
        self.active = True
        
        # Colors per type
        if self.type == 'double':
            self.color = (255, 100, 255) # Pink/Purple
            self.label = "2X"
        elif self.type == 'shield':
            self.color = (100, 255, 100) # Green
            self.label = "SD"
        elif self.type == 'slow':
            self.color = (100, 200, 255) # Blue
            self.label = "SL"
            
    def update(self):
        self.y += self.speed
        self.rect.y = int(self.y)
        
        if self.y > 1000: # Assuming screen height < 1000
            self.active = False
            
    def draw(self, surface):
        if not self.active: return
        
        # Floating effect with sine wave potentially, but simple drop for now
        # Draw Glassy Box
        box_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.rect(box_surf, (*self.color, 150), (0, 0, 30, 30), border_radius=5)
        pygame.draw.rect(box_surf, (255, 255, 255), (0, 0, 30, 30), 2, border_radius=5)
        
        # Font
        font = pygame.font.SysFont("arial", 12, bold=True)
        text = font.render(self.label, True, (255, 255, 255))
        text_rect = text.get_rect(center=(15, 15))
        box_surf.blit(text, text_rect)
        
        surface.blit(box_surf, (self.x - 5, self.y - 5))
