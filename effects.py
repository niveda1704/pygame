
import pygame
import random
import math

class Starfield:
    def __init__(self, width, height, star_count=100):
        self.width = width
        self.height = height
        self.stars = []
        for _ in range(star_count):
            self.stars.append(self._create_star())
            
    def _create_star(self):
        # x, y, speed, size, brightness
        return {
            'x': random.randint(0, self.width),
            'y': random.randint(0, self.height),
            'speed': random.uniform(0.5, 3.0),
            'size': random.uniform(1, 2),
            'brightness': random.randint(150, 255)
        }

    def update(self):
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > self.height:
                star['y'] = 0
                star['x'] = random.randint(0, self.width)
    
    def draw(self, surface):
        surface.fill((10, 10, 20)) # Dark blue-black background
        for star in self.stars:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(surface, color, (int(star['x']), int(star['y'])), int(star['size']))

class Particle:
    def __init__(self, x, y, color, speed, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = speed * random.uniform(0.5, 1.5)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.lifetime = lifetime
        self.age = 0
        self.size = random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        self.size = max(0, self.size - 0.05)

    def draw(self, surface):
        if self.age < self.lifetime:
            alpha = max(0, 255 - (self.age / self.lifetime) * 255)
            # Create a transparent surface for the particle
            s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            color_with_alpha = (*self.color, int(alpha))
            pygame.draw.circle(s, color_with_alpha, (int(self.size), int(self.size)), int(self.size))
            surface.blit(s, (self.x - self.size, self.y - self.size))

class Explosion:
    def __init__(self, x, y, color=(255, 100, 50)):
        self.particles = []
        for _ in range(20):
            self.particles.append(Particle(x, y, color, random.uniform(2, 5), random.randint(20, 40)))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.age < p.lifetime]
        return len(self.particles) > 0

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

class ScreenShake:
    def __init__(self):
        self.duration = 0
        self.intensity = 0

    def start(self, duration, intensity):
        self.duration = duration
        self.intensity = intensity

    def update(self):
        if self.duration > 0:
            self.duration -= 1
            ox = random.uniform(-self.intensity, self.intensity)
            oy = random.uniform(-self.intensity, self.intensity)
            return ox, oy
        return 0, 0
