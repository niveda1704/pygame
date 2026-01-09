
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
        elif self.type == 'tank':
            self.speed_y = 1
            self.speed_x = 0
            self.color = (150, 150, 150)
            self.health = 80
            self.width = 60
            self.height = 60
        elif self.type == 'vanguard':
            self.speed_y = 2
            self.speed_x = 0
            self.color = (255, 50, 50)
            self.health = 30
            self.last_shot = 0
            self.shoot_delay = 2000 # ms
        elif self.type == 'hunter':
            self.speed_y = 2.5
            self.speed_x = 0
            self.color = (50, 255, 200) # Cyan/Teal
            self.health = 25
            self.width = 35
            self.height = 35
            
        self.rect.width = self.width
        self.rect.height = self.height

    def update(self, slow_active=False, player_rect=None):
        speed_modifier = 0.5 if slow_active else 1.0
        new_bullets = []
        
        if self.type == 'sine':
            self.y += self.speed_y * speed_modifier
            self.t += 0.05
            self.x = self.initial_x + math.sin(self.t) * 50
        elif self.type == 'vanguard':
            self.y += self.speed_y * speed_modifier
            # Shoot logic
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot > self.shoot_delay:
                from bullet import Bullet
                new_bullets.append(Bullet(self.rect.centerx, self.rect.bottom, speed=5, color=(255, 100, 0)))
                self.last_shot = current_time
        elif self.type == 'hunter':
            self.y += self.speed_y * speed_modifier
            if player_rect:
                # Move towards player x
                if self.rect.centerx < player_rect.centerx: self.x += 1 * speed_modifier
                elif self.rect.centerx > player_rect.centerx: self.x -= 1 * speed_modifier
        else:
            self.y += self.speed_y * speed_modifier
            self.x += self.speed_x * speed_modifier
            
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        if self.y > 1000:
            self.active = False
            
        return new_bullets

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
        elif self.type == 'tank':
            pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
            pygame.draw.rect(surface, (200, 200, 200), (self.rect.x+10, self.rect.y+10, self.width-20, self.height-20), 2)
        elif self.type == 'vanguard':
            points = [
                (self.rect.left, self.rect.top),
                (self.rect.right, self.rect.top),
                (self.rect.centerx, self.rect.bottom)
            ]
            pygame.draw.polygon(surface, self.color, points)
            pygame.draw.circle(surface, (255, 255, 255), self.rect.center, 5) # Core
        elif self.type == 'hunter':
            # Diamond shape or spiked circle
            points = [
                (self.rect.centerx, self.rect.top),
                (self.rect.right, self.rect.centery),
                (self.rect.centerx, self.rect.bottom),
                (self.rect.left, self.rect.centery)
            ]
            pygame.draw.polygon(surface, self.color, points)
            pygame.draw.rect(surface, (255, 255, 255), (self.rect.centerx-2, self.rect.centery-2, 4, 4))
