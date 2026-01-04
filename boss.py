
import pygame
import random
import math
from bullet import Bullet

class Boss:
    def __init__(self, screen_width, level):
        self.screen_width = screen_width
        self.width = 150
        self.height = 100
        self.x = (screen_width - self.width) // 2
        self.y = -self.height
        self.target_y = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.active = True
        self.max_health = 500 + (level * 100)
        self.health = self.max_health
        self.speed = 2
        self.moving_right = True
        
        self.state = 'entering' # entering, fighting
        self.attack_timer = 0
        self.attack_cooldown = 60 # frames
        self.phase = 0 # 0: move, 1: attack
        
    def update(self, player_rect):
        if not self.active: return []
        
        boss_bullets = []
        
        if self.state == 'entering':
            if self.y < self.target_y:
                self.y += 2
            else:
                self.state = 'fighting'
        elif self.state == 'fighting':
            # Movement
            if self.moving_right:
                self.x += self.speed
                if self.x + self.width > self.screen_width - 20:
                    self.moving_right = False
            else:
                self.x -= self.speed
                if self.x < 20:
                    self.moving_right = True
            
            # Attack logic
            self.attack_timer += 1
            if self.attack_timer >= self.attack_cooldown:
                self.attack_timer = 0
                pattern = random.choice(['spread', 'aimed', 'circle'])
                boss_bullets = self.attack(pattern, player_rect)
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        return boss_bullets

    def attack(self, pattern, player_rect):
        bullets = []
        center_x = self.rect.centerx
        bottom_y = self.rect.bottom
        
        if pattern == 'spread':
            for i in range(-2, 3):
                # Pass dx for spread
                b = Bullet(center_x, bottom_y, speed=5, dx=i*2, bullet_type='boss')
                bullets.append(b)
                
        elif pattern == 'aimed':
            # Simple stream
            bullets.append(Bullet(center_x, bottom_y, speed=7, bullet_type='boss'))
            bullets.append(Bullet(center_x - 30, bottom_y, speed=7, bullet_type='boss'))
            bullets.append(Bullet(center_x + 30, bottom_y, speed=7, bullet_type='boss'))
            
        return bullets

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.active = False
            return True
        return False

    def draw(self, surface):
        if not self.active: return
        
        # Draw complex shape for Boss
        # Main Body
        pygame.draw.rect(surface, (150, 0, 50), self.rect, border_radius=20)
        # Inner Core
        pygame.draw.circle(surface, (255, 50, 50), self.rect.center, 30)
        # Wings info
        pygame.draw.polygon(surface, (100, 0, 0), [
            (self.rect.left, self.rect.top),
            (self.rect.left - 30, self.rect.centery),
            (self.rect.left, self.rect.bottom)
        ])
        pygame.draw.polygon(surface, (100, 0, 0), [
            (self.rect.right, self.rect.top),
            (self.rect.right + 30, self.rect.centery),
            (self.rect.right, self.rect.bottom)
        ])
        
        # Glow
        s = pygame.Surface((self.width + 100, self.height + 50), pygame.SRCALPHA)
        pygame.draw.ellipse(s, (255, 0, 0, 50), s.get_rect())
        surface.blit(s, (self.x - 50, self.y - 25))
