
import pygame
import sys
import random

from player import Player
from bullet import Bullet
from level import LevelManager
from ui import UI
from effects import Starfield, Explosion, ScreenShake
from powerup import PowerUp

from sound_manager import SoundManager

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Space Shooter Glass")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def main():
    running = True
    game_state = "MENU" # MENU, PLAYING, GAMEOVER
    
    # Game Objects
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    level_manager = LevelManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    ui = UI()
    starfield = Starfield(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen_shake = ScreenShake()
    sound_manager = SoundManager()
    
    # Start Music
    sound_manager.play_music()
    
    bullets = []
    enemy_bullets = [] # Boss bullets mainly
    powerups = []
    explosions = []
    
    # Touch input state
    touch_active = {'left': False, 'right': False, 'shoot': False}
    touch_rects = {}
    
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if game_state == "MENU":
                    if event.key == pygame.K_SPACE:
                        game_state = "PLAYING"
                        sound_manager.play('shoot') # Feedback sound
                        level_manager.start_level()
                elif game_state == "GAMEOVER":
                    if event.key == pygame.K_r:
                        # Reset Game
                        player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
                        level_manager = LevelManager(SCREEN_WIDTH, SCREEN_HEIGHT)
                        level_manager.start_level()
                        bullets = []
                        enemy_bullets = []
                        powerups = []
                        explosions = []
                        game_state = "PLAYING"
                elif game_state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        new_bullets = player.shoot(pygame.time.get_ticks())
                        if new_bullets:
                            bullets.extend(new_bullets)
                            sound_manager.play('shoot')
            
            # Touch Input Handling (Mouse simulation for PC, actual touch for mobile if supported lib)
            if event.type == pygame.MOUSEBUTTONDOWN and game_state == "PLAYING":
                m_pos = pygame.mouse.get_pos()
                if touch_rects:
                    if touch_rects['left'].collidepoint(m_pos): touch_active['left'] = True
                    if touch_rects['right'].collidepoint(m_pos): touch_active['right'] = True
                    if touch_rects['shoot'].collidepoint(m_pos): 
                        touch_active['shoot'] = True
                        new_bullets = player.shoot(pygame.time.get_ticks())
                        if new_bullets:
                            bullets.extend(new_bullets)
                            sound_manager.play('shoot')

            if event.type == pygame.MOUSEBUTTONUP:
                touch_active['left'] = False
                touch_active['right'] = False
                touch_active['shoot'] = False

        # 2. Update
        starfield.update()
        shake_x, shake_y = screen_shake.update()
        
        if game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            
            # Combine Keyboard and Touch Input
            move_left = keys[pygame.K_LEFT] or keys[pygame.K_a] or touch_active['left']
            move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d] or touch_active['right']
            
            # Simple wrapper to update player with boolean flags instead of raw keys if we wanted to refactor player,
            # but currently player.update takes keys. Let's hack it or modify player.
            # Easiest: modifying player.update to accept direct booleans or just mocking keys?
            # Let's modify call execution.
            # Actually, player.update reads keys directly. Let's make a custom keys-like object or modify player logic.
            # Simpler: Modify Player.update() signature is overkill.
            # Let's just manually move if touch is active.
            if touch_active['left']: player.x -= player.speed
            if touch_active['right']: player.x += player.speed
            
            player.update(keys) # Handles bounds and other logic, keyboard movement adds to touch movement.
            
            # Level & Spawning
            level_manager.update(player.rect, enemy_bullets)
            
            # Entities
            for b in bullets: b.update()
            for eb in enemy_bullets: eb.update()
            for p in powerups: p.update()
            
            for e in level_manager.enemies:
                e.update(slow_active=player.slow_motion_active)
                
                # Player-Enemy Collision
                if e.rect.colliderect(player.rect):
                    if not player.shield_active:
                        player.take_damage(20)
                        screen_shake.start(10, 5)
                        sound_manager.play('explosion')
                        explosions.append(Explosion(e.rect.centerx, e.rect.centery))
                        e.active = False # Enemy dies on crash
                    else:
                         e.active = False # Shield destroys enemy
                         explosions.append(Explosion(e.rect.centerx, e.rect.centery))
                         sound_manager.play('explosion')
                         player.score += 10

            # Bullet-Enemy Collision
            for b in bullets[:]:
                if not b.active: continue
                # Check normal enemies
                for e in level_manager.enemies:
                    if e.active and b.rect.colliderect(e.rect):
                        b.active = False
                        is_dead = e.take_damage(10)
                        if is_dead:
                            explosions.append(Explosion(e.rect.centerx, e.rect.centery))
                            sound_manager.play('explosion')
                            player.score += 10
                            # Drop Powerup Chance
                            if random.random() < 0.1:
                                powerups.append(PowerUp(e.rect.centerx, e.rect.centery))
                        break
                
                # Check Boss
                if level_manager.boss_active and level_manager.boss:
                     if b.rect.colliderect(level_manager.boss.rect):
                         b.active = False
                         is_dead = level_manager.boss.take_damage(5) # Less damage to boss
                         if is_dead:
                             explosions.append(Explosion(level_manager.boss.rect.centerx, level_manager.boss.rect.centery, color=(200, 50, 200)))
                             sound_manager.play('explosion')
                             player.score += 500
                             screen_shake.start(30, 10)
            
            # Enemy Bullets - Player Collision
            for eb in enemy_bullets[:]:
                if eb.active and eb.rect.colliderect(player.rect):
                    eb.active = False
                    player.take_damage(10)
                    screen_shake.start(5, 3)
            
            # Powerup-Player Collision
            for p in powerups[:]:
                if p.active and p.rect.colliderect(player.rect):
                    p.active = False
                    player.activate_powerup(p.type)
                    sound_manager.play('powerup')

            # Cleanup
            bullets = [b for b in bullets if b.active]
            enemy_bullets = [b for b in enemy_bullets if b.active]
            powerups = [p for p in powerups if p.active]
            
            # Explosions (Visual only)
            active_explosions = []
            for ex in explosions:
                if ex.update():
                    active_explosions.append(ex)
            explosions = active_explosions

            # Check Game Over
            if player.health <= 0:
                game_state = "GAMEOVER"

        # 3. Draw
        # Apply shake offset
        display_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        starfield.draw(display_surf)
        
        if game_state == "PLAYING" or game_state == "GAMEOVER":
            for p in powerups: p.draw(display_surf)
            for b in bullets: b.draw(display_surf)
            for eb in enemy_bullets: eb.draw(display_surf)
            
            for e in level_manager.enemies: e.draw(display_surf)
            
            if level_manager.boss_active and level_manager.boss:
                level_manager.boss.draw(display_surf)
                
            player.draw(display_surf)
            
            for ex in explosions: ex.draw(display_surf)
            
            # Blit world to screen with offset
            screen.blit(display_surf, (shake_x, shake_y))
            
            # HUD (No Shake)
            ui.draw_hud(screen, player, level_manager)
            ui.draw_boss_health(screen, level_manager.boss)
            
            # Draw Touch Controls if playing
            if game_state == "PLAYING":
                 touch_rects = ui.draw_touch_controls(screen)
            
            if game_state == "GAMEOVER":
                ui.draw_game_over(screen, player.score)
                
        elif game_state == "MENU":
            screen.blit(display_surf, (0, 0)) # Just stars
            # Title Screen
            ui.draw_glass_panel(screen, pygame.Rect(100, 200, 400, 300))
            ui.draw_text(screen, "SPACE SHOOTER", SCREEN_WIDTH//2, 250, center=True, font_type='title')
            ui.draw_text(screen, "Press SPACE to Start", SCREEN_WIDTH//2, 400, center=True, font_type='large')
            
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
