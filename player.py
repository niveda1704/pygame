
import pygame
from bullet import Bullet

class Player:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = 50
        self.height = 40
        self.x = screen_width // 2
        self.y = screen_height - 100
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.max_health = 100
        self.health = 100
        self.score = 0
        
        # Attack state
        self.last_shot_time = 0
        self.shoot_delay = 250 # ms
        
        # PowerUps
        self.double_bullet_active = False
        self.double_bullet_timer = 0
        self.shield_active = False
        self.shield_timer = 0
        self.slow_motion_active = False
        self.slow_motion_timer = 0

    def update(self, keys):
        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            
        # Bounds
        self.x = max(0, min(self.x, self.screen_width - self.width))
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Powerup timers
        dt = 16 # Approx for 60fps
        if self.double_bullet_active:
            self.double_bullet_timer -= dt
            if self.double_bullet_timer <= 0:
                self.double_bullet_active = False
        
        if self.shield_active:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_active = False
                
        if self.slow_motion_active:
            self.slow_motion_timer -= dt
            if self.slow_motion_timer <= 0:
                self.slow_motion_active = False

    def shoot(self, current_time):
        if current_time - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = current_time
            bullets = []
            if self.double_bullet_active:
                bullets.append(Bullet(self.rect.centerx - 10, self.rect.top))
                bullets.append(Bullet(self.rect.centerx + 10, self.rect.top))
            else:
                bullets.append(Bullet(self.rect.centerx, self.rect.top))
            return bullets
        return []

    def take_damage(self, amount):
        if self.shield_active:
            return # No damage if shield is up
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def activate_powerup(self, p_type):
        duration = 5000 # 5 seconds
        if p_type == 'double':
            self.double_bullet_active = True
            self.double_bullet_timer = duration
        elif p_type == 'shield':
            self.shield_active = True
            self.shield_timer = duration
        elif p_type == 'slow':
            self.slow_motion_active = True
            self.slow_motion_timer = duration

    def draw(self, surface):
        # Draw Ship - Triangle shape
        # Body
        points = [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.centerx, self.rect.bottom - 10),
            (self.rect.right, self.rect.bottom)
        ]
        pygame.draw.polygon(surface, (0, 200, 255), points)
        
        # Engine Glow
        pygame.draw.circle(surface, (0, 255, 255, 100), (self.rect.centerx, self.rect.bottom - 5), 5)
        
        # Shield Visualization
        if self.shield_active:
            shield_surf = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            pygame.draw.ellipse(shield_surf, (100, 255, 100, 100), shield_surf.get_rect(), width=2)
            pygame.draw.ellipse(shield_surf, (100, 255, 100, 30), shield_surf.get_rect())
            surface.blit(shield_surf, (self.x - 10, self.y - 10))
