
import pygame
import math

class Bullet:
    def __init__(self, x, y, speed=-10, dx=0, bullet_type='normal'):
        self.x = x
        self.y = y
        self.dy = speed
        self.dx = dx
        self.active = True
        self.type = bullet_type
        
        # Dimensions based on type
        if self.type == 'boss':
             self.width = 15
             self.height = 30
             self.color = (255, 50, 50)
        else:
             self.width = 6
             self.height = 15
             self.color = (100, 255, 255)

        self.rect = pygame.Rect(self.x - self.width//2, self.y, self.width, self.height)

    def update(self):
        self.y += self.dy
        self.x += self.dx
        self.rect.y = int(self.y)
        self.rect.x = int(self.x - self.width//2)
        
        # Deactivate if off screen
        if self.y < -50 or self.y > 1000: # Assuming typical height < 1000
            self.active = False

    def draw(self, surface):
        if not self.active: return
        
        # Draw with a glow
        # Core
        pygame.draw.rect(surface, (255, 255, 255), self.rect, border_radius=2)
        
        # Glow
        glow_surf = pygame.Surface((self.width * 4, self.height * 2), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*self.color, 80), (self.width, self.height//2, self.width * 2, self.height), border_radius=5)
        surface.blit(glow_surf, (self.x - self.width * 2, self.y - self.height//4))
