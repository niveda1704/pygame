
import pygame
import random
import math

class Enemy:
    def __init__(self, x, y, enemy_type='basic'):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.active = True
        self.max_health = 20
        self.health = self.max_health
        
        # Base stats
        if self.type == 'basic':
            self.speed_y = 2
            self.speed_x = 0
            self.color = (255, 100, 100)
            self.health = 20
        elif self.type == 'fast':
            self.speed_y = 4
            self.speed_x = 0
            self.color = (255, 200, 50)
            self.health = 10
            self.width = 30
            self.height = 30
        elif self.type == 'sine':
            self.speed_y = 1.5
            self.speed_x = 0
            self.color = (200, 100, 255)
            self.health = 30
            self.initial_x = x
            self.t = 0
            
        self.rect.width = self.width
        self.rect.height = self.height

    def update(self, slow_active=False):
        speed_modifier = 0.5 if slow_active else 1.0
        
        if self.type == 'sine':
            self.y += self.speed_y * speed_modifier
            self.t += 0.05
            self.x = self.initial_x + math.sin(self.t) * 50
        else:
            self.y += self.speed_y * speed_modifier
            self.x += self.speed_x * speed_modifier
            
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        if self.y > 1000:
            self.active = False

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.active = False
            return True # Dead
        return False

    def draw(self, surface):
        if not self.active: return
        
        # Draw soft glow
        glow_surf = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*self.color, 50), (self.width//2 + 10, self.height//2 + 10), self.width//2 + 10)
        surface.blit(glow_surf, (self.x - 10, self.y - 10))
        
        # Draw Enemy Shape
        if self.type == 'basic':
            pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        elif self.type == 'fast':
            points = [
                (self.rect.centerx, self.rect.bottom),
                (self.rect.left, self.rect.top),
                (self.rect.right, self.rect.top)
            ]
            pygame.draw.polygon(surface, self.color, points)
        elif self.type == 'sine':
             pygame.draw.circle(surface, self.color, self.rect.center, self.width//2)
