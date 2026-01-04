
import random
from enemy import Enemy
from boss import Boss

class LevelManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = 1
        self.enemies = []
        self.boss = None
        self.boss_active = False
        
        # Wave management
        self.spawn_timer = 0
        self.spawn_delay = 60 # frames
        self.wave_count = 0
        self.enemies_per_wave = 10
        self.enemies_spawned_in_level = 0
        self.enemies_to_spawn = 10
        
        self.level_transition = False
        self.transition_timer = 0

    def start_level(self):
        self.enemies_to_spawn = 10 + (self.level * 2)
        self.enemies_spawned_in_level = 0
        self.spawn_delay = max(20, 60 - (self.level * 2))
        self.level_transition = False

    def update(self, player_rect, bullets):
        if self.level_transition:
            self.transition_timer += 1
            if self.transition_timer > 120: # 2 seconds pause between levels
                self.level += 1
                self.start_level()
            return
            
        # Check if boss level
        if self.level % 5 == 0:
            if not self.boss_active and self.enemies_spawned_in_level == 0: # Start boss immediately at level start?
                # Actually let's just make the whole level the boss fight
                 if not self.boss:
                     self.boss = Boss(self.screen_width, self.level)
                     self.boss_active = True
            
            if self.boss and self.boss.active:
                boss_bullets = self.boss.update(player_rect)
                for b in boss_bullets:
                    bullets.append(b)
                if not self.boss.active:
                    # Boss defeated
                    self.boss_active = False
                    self.boss = None
                    self.level_transition = True
                    self.transition_timer = 0
            return

        # Normal Level Spawning
        if self.enemies_spawned_in_level < self.enemies_to_spawn:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_timer = 0
                self.spawn_enemy()
        elif len(self.enemies) == 0:
            # Level Complete
            self.level_transition = True
            self.transition_timer = 0

        # Update Enemies
        for enemy in self.enemies:
            # Note: We pass strict slow-mo status from main, but here we just coordinate
            pass 
            
        # Cleanup dead enemies
        self.enemies = [e for e in self.enemies if e.active]

    def spawn_enemy(self):
        x = random.randint(50, self.screen_width - 50)
        # Determine enemy type based on level
        r = random.random()
        e_type = 'basic'
        
        if self.level > 2:
            if r < 0.2: e_type = 'fast'
        if self.level > 3:
            if r < 0.4 and r > 0.2: e_type = 'sine'
            
        enemy = Enemy(x, -50, enemy_type=e_type)
        self.enemies.append(enemy)
        self.enemies_spawned_in_level += 1
