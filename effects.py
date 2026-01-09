
import pygame
import random
import math

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

class Starfield:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Divide stars into 3 layers: [Distant, Mid, Near]
        self.layers = [
            {'stars': [self._create_star(0.5, 1, 150) for _ in range(50)], 'speed_mult': 1},
            {'stars': [self._create_star(1.2, 2, 200) for _ in range(30)], 'speed_mult': 2},
            {'stars': [self._create_star(2.5, 3, 255) for _ in range(15)], 'speed_mult': 4}
        ]
            
    def _create_star(self, speed_base, size, brightness):
        return {
            'x': random.randint(0, self.width),
            'y': random.randint(0, self.height),
            'speed': speed_base,
            'size': size,
            'brightness': brightness
        }

    def update(self):
        for layer in self.layers:
            for star in layer['stars']:
                star['y'] += star['speed']
                if star['y'] > self.height:
                    star['y'] = 0
                    star['x'] = random.randint(0, self.width)
    
    def draw(self, surface):
        surface.fill((5, 5, 15)) # Darker cosmic blue
        for layer in self.layers:
            for star in layer['stars']:
                color = (star['brightness'], star['brightness'], star['brightness'])
                pygame.draw.circle(surface, color, (int(star['x']), int(star['y'])), int(star['size']))

class TrailParticle(Particle):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 1, 30)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(1, 3) # Move downwards
        self.size = random.uniform(2, 5)

class Trail:
    def __init__(self, color=(0, 200, 255)):
        self.particles = []
        self.color = color

    def add(self, x, y):
        self.particles.append(TrailParticle(x, y, self.color))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.age < p.lifetime]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

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

class Nebula:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.blobs = []
        for _ in range(3):
            self.blobs.append(self._create_blob())

    def _create_blob(self):
        # Large soft colorful clouds
        colors = [(80, 0, 150), (0, 80, 150), (100, 0, 100)]
        return {
            'x': random.randint(0, self.width),
            'y': random.randint(0, self.height),
            'size': random.randint(200, 400),
            'color': random.choice(colors),
            'speed': random.uniform(0.1, 0.3)
        }

    def update(self):
        for b in self.blobs:
            b['y'] += b['speed']
            if b['y'] > self.height + b['size']:
                b['y'] = -b['size']
                b['x'] = random.randint(0, self.width)

    def draw(self, surface):
        for b in self.blobs:
            # We draw a very soft circle by using a surface with per-pixel alpha
            s = pygame.Surface((b['size']*2, b['size']*2), pygame.SRCALPHA)
            # Multi-layered circles for a gradient effect
            for r in range(b['size'], 0, -20):
                alpha = int(40 * (1 - r/b['size']))
                pygame.draw.circle(s, (*b['color'], alpha), (b['size'], b['size']), r)
            surface.blit(s, (b['x']-b['size'], b['y']-b['size']))

class FloatingText:
    def __init__(self, x, y, text, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = 40
        self.age = 0
        self.vy = -1.5

    def update(self):
        self.y += self.vy
        self.age += 1
        return self.age < self.lifetime

    def draw(self, surface, font):
        alpha = int(255 * (1 - self.age/self.lifetime))
        text_surf = font.render(self.text, True, self.color)
        text_surf.set_alpha(alpha)
        surface.blit(text_surf, (self.x, self.y))

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
