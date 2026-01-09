
import pygame
from bullet import Bullet
from effects import Trail

class Player:
    def __init__(self, screen_width, screen_height, upgrades=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = 50
        self.height = 40
        self.x = screen_width // 2
        self.y = screen_height - 100
        
        # Upgrades (Defaults)
        self.upgrades = upgrades or {'speed': 0, 'fire_rate': 0, 'health': 0, 'magnet': 0}
        
        self.speed = 5 + self.upgrades['speed'] * 0.5
        self.shoot_delay = 250 - self.upgrades['fire_rate'] * 20
        self.max_health = 100 + self.upgrades['health'] * 20
        self.health = self.max_health
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.score = 0
        
        # Visuals
        self.tilt_angle = 0
        self.max_tilt = 15
        self.trail = Trail()
        
        # Attack state
        self.last_shot_time = 0
        
        # PowerUps
        self.double_bullet_active = False
        self.double_bullet_timer = 0
        self.shield_active = False
        self.shield_timer = 0
        self.slow_motion_active = False
        self.slow_motion_timer = 0
        
        # Secondary Weapon (EMP)
        self.emp_energy = 100
        self.emp_max_energy = 100
        self.emp_active = False
        self.emp_radius = 0
        self.emp_max_radius = 300

    def update(self, keys):
        # Movement & Tilting
        target_tilt = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            target_tilt = self.max_tilt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            target_tilt = -self.max_tilt
            
        # Smooth Tilt transition
        self.tilt_angle += (target_tilt - self.tilt_angle) * 0.1
            
        # Bounds
        self.x = max(0, min(self.x, self.screen_width - self.width))
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Exhaust
        self.trail.add(self.rect.centerx, self.rect.bottom - 5)
        self.trail.update()
        
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
        
        # EMP Charge
        self.emp_energy = min(self.emp_max_energy, self.emp_energy + 0.1)
        
        if self.emp_active:
            self.emp_radius += 10
            if self.emp_radius > self.emp_max_radius:
                self.emp_active = False
                self.emp_radius = 0

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
        elif p_type == 'health':
            self.health = min(self.max_health, self.health + 30)

    def activate_secondary(self):
        if self.emp_energy >= 100:
            self.emp_energy = 0
            self.emp_active = True
            self.emp_radius = 0
            return True
        return False

    def draw(self, surface):
        self.trail.draw(surface)
        
        # Draw Ship - Triangle shape with rotation/tilting
        ship_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        points = [
            (self.width // 2, 0),
            (0, self.height),
            (self.width // 2, self.height - 10),
            (self.width, self.height)
        ]
        pygame.draw.polygon(ship_surf, (0, 200, 255), points)
        
        # Engine Glow
        pygame.draw.circle(ship_surf, (0, 255, 255, 100), (self.width // 2, self.height - 5), 5)
        
        # Rotate based on tilt
        rotated_ship = pygame.transform.rotate(ship_surf, self.tilt_angle)
        rot_rect = rotated_ship.get_rect(center=self.rect.center)
        surface.blit(rotated_ship, rot_rect.topleft)
        
        # Shield Visualization
        if self.shield_active:
            shield_surf = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            pygame.draw.ellipse(shield_surf, (100, 255, 100, 100), shield_surf.get_rect(), width=2)
            pygame.draw.ellipse(shield_surf, (100, 255, 100, 30), shield_surf.get_rect())
            surface.blit(shield_surf, (self.rect.centerx - self.width//2 - 10, self.rect.centery - self.height//2 - 10))

        # EMP Nova Drawing
        if self.emp_active:
            emp_surf = pygame.Surface((self.emp_radius*2, self.emp_radius*2), pygame.SRCALPHA)
            alpha = max(0, 150 - (self.emp_radius / self.emp_max_radius) * 150)
            pygame.draw.circle(emp_surf, (0, 255, 255, alpha), (self.emp_radius, self.emp_radius), self.emp_radius, 2)
            surface.blit(emp_surf, (self.rect.centerx - self.emp_radius, self.rect.centery - self.emp_radius))
