
import pygame
import sys
import random
import asyncio

from player import Player
from bullet import Bullet
from level import LevelManager
from ui import UI
from effects import Starfield, Explosion, ScreenShake, Nebula, FloatingText
from powerup import PowerUp
from sound_manager import SoundManager
from save_manager import SaveManager

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Space Shooter Glass")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def reset_game(save_manager):
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, upgrades=save_manager.data['upgrades'])
    level_manager = LevelManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    return player, level_manager

async def main():
    save_manager = SaveManager()
    running = True
    game_state = "MENU" # MENU, PLAYING, GAMEOVER, SHOP
    
    # Game Objects
    player, level_manager = reset_game(save_manager)
    ui = UI()
    starfield = Starfield(SCREEN_WIDTH, SCREEN_HEIGHT)
    nebula = Nebula(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen_shake = ScreenShake()
    sound_manager = SoundManager()
    sound_manager.play_music()
    
    # Game Lists
    bullets = []
    enemy_bullets = []
    powerups = []
    explosions = []
    floating_texts = []
    
    # Game State
    combo = 1
    combo_timer = 0
    flash_alpha = 0
    shop_buttons = {}
    
    # Sound & Transition State
    last_level = 1
    boss_was_active = False
    level_text_timer = 0
    game_over_sound_played = False
    low_health_sound_timer = 0
    
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
                    if game_state == "SHOP":
                        game_state = "MENU"
                    else:
                        running = False
                if game_state == "MENU":
                    if event.key == pygame.K_SPACE:
                        player, level_manager = reset_game(save_manager)
                        game_state = "PLAYING"
                        sound_manager.play('shoot')
                        level_manager.start_level()
                        last_level = level_manager.level
                        game_over_sound_played = False
                        level_text_timer = 90
                    if event.key == pygame.K_s:
                        game_state = "SHOP"
                elif game_state == "GAMEOVER":
                    if event.key == pygame.K_r:
                        player, level_manager = reset_game(save_manager)
                        bullets, enemy_bullets, powerups, explosions = [], [], [], []
                        game_state = "PLAYING"
                        level_manager.start_level()
                        last_level = level_manager.level
                        game_over_sound_played = False
                        level_text_timer = 90
                    if event.key == pygame.K_m:
                        game_state = "MENU"
                elif game_state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        new_bullets = player.shoot(pygame.time.get_ticks())
                        if new_bullets:
                            bullets.extend(new_bullets)
                            sound_manager.play('shoot')
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        if player.activate_secondary():
                            sound_manager.play('boss_enter') # Reuse for deep rumble
                            screen_shake.start(20, 10)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                if game_state == "PLAYING":
                    if touch_rects:
                        if touch_rects['left'].collidepoint(m_pos): touch_active['left'] = True
                        if touch_rects['right'].collidepoint(m_pos): touch_active['right'] = True
                        if touch_rects['shoot'].collidepoint(m_pos): 
                            touch_active['shoot'] = True
                            new_bullets = player.shoot(pygame.time.get_ticks())
                            if new_bullets:
                                bullets.extend(new_bullets)
                                sound_manager.play('shoot')
                        if 'emp' in touch_rects and touch_rects['emp'].collidepoint(m_pos):
                            if player.activate_secondary():
                                sound_manager.play('boss_enter')
                                screen_shake.start(20, 10)
                elif game_state == "SHOP":
                    for key, (rect, cost) in shop_buttons.items():
                        if rect.collidepoint(m_pos):
                            if save_manager.upgrade_item(key, cost):
                                sound_manager.play('powerup')

            if event.type == pygame.MOUSEBUTTONUP:
                touch_active['left'] = False
                touch_active['right'] = False
                touch_active['shoot'] = False

        # 2. Update
        starfield.update()
        nebula.update()
        shake_x, shake_y = screen_shake.update()
        if flash_alpha > 0: flash_alpha -= 10
        
        if game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            if touch_active['left']: player.x -= player.speed
            if touch_active['right']: player.x += player.speed
            
            player.update(keys)
            level_manager.update(player.rect, enemy_bullets)
            
            # Combo Logic
            if combo_timer > 0:
                combo_timer -= 1
            else:
                combo = 1
            
            # Level / Boss Detect
            if level_manager.level > last_level:
                sound_manager.play('level_complete')
                level_text_timer = 90 # 1.5 seconds
                last_level = level_manager.level
            
            if level_manager.boss_active and not boss_was_active:
                sound_manager.play('boss_enter')
                boss_was_active = True
            elif not level_manager.boss_active:
                boss_was_active = False

            if level_text_timer > 0: level_text_timer -= 1

            for b in bullets: b.update()
            for eb in enemy_bullets: eb.update()
            
            # Magnet Upgrade Logic
            magnet_range = 100 + player.upgrades['magnet'] * 50
            for p in powerups: 
                p.update()
                if player.upgrades['magnet'] > 0:
                    dist = pygame.math.Vector2(player.rect.center).distance_to(p.rect.center)
                    if dist < magnet_range:
                        p.x += (player.rect.centerx - p.rect.centerx) * 0.05
                        p.y += (player.rect.centery - p.rect.centery) * 0.05

            for e in level_manager.enemies:
                new_eb = e.update(slow_active=player.slow_motion_active, player_rect=player.rect)
                if new_eb: enemy_bullets.extend(new_eb)
                
                # EMP vs Enemies
                if player.emp_active:
                    dist = pygame.math.Vector2(player.rect.center).distance_to(e.rect.center)
                    if dist < player.emp_radius:
                        e.active = False
                        player.score += 10 * combo
                        floating_texts.append(FloatingText(e.rect.x, e.rect.y, f"+{10*combo}", (0, 255, 255)))
                        explosions.append(Explosion(e.rect.centerx, e.rect.centery))

                if e.rect.colliderect(player.rect):
                    if not player.shield_active:
                        player.take_damage(20)
                        flash_alpha = 150
                        screen_shake.start(15, 8)
                        sound_manager.play('damage')
                        explosions.append(Explosion(e.rect.centerx, e.rect.centery))
                        e.active = False
                    else:
                         e.active = False
                         explosions.append(Explosion(e.rect.centerx, e.rect.centery))
                         sound_manager.play('explosion')
                         player.score += 10

            for b in bullets[:]:
                if not b.active: continue
                for e in level_manager.enemies:
                    if e.active and b.rect.colliderect(e.rect):
                        b.active = False
                        if e.take_damage(10):
                            explosions.append(Explosion(e.rect.centerx, e.rect.centery))
                            sound_manager.play('explosion')
                            player.score += 10 * combo
                            floating_texts.append(FloatingText(e.rect.x, e.rect.y, f"+{10*combo}"))
                            combo += 1
                            combo_timer = 120 # 2 seconds
                            if random.random() < 0.1: powerups.append(PowerUp(e.rect.centerx, e.rect.centery))
                        break
                
                if level_manager.boss_active and level_manager.boss:
                     if b.rect.colliderect(level_manager.boss.rect):
                         b.active = False
                         if level_manager.boss.take_damage(5):
                             explosions.append(Explosion(level_manager.boss.rect.centerx, level_manager.boss.rect.centery, color=(200, 50, 200)))
                             sound_manager.play('explosion')
                             player.score += 500
                             screen_shake.start(30, 10)
            
            for eb in enemy_bullets[:]:
                if eb.active and eb.rect.colliderect(player.rect):
                    eb.active = False
                    if not player.shield_active:
                        player.take_damage(10)
                        sound_manager.play('damage')
                        flash_alpha = 100
                        screen_shake.start(5, 3)
            
            for p in powerups[:]:
                if p.active and p.rect.colliderect(player.rect):
                    p.active = False
                    player.activate_powerup(p.type)
                    sound_manager.play('powerup')

            bullets = [b for b in bullets if b.active]
            enemy_bullets = [b for b in enemy_bullets if b.active]
            powerups = [p for p in powerups if p.active]
            explosions = [ex for ex in explosions if ex.update()]
            floating_texts = [ft for ft in floating_texts if ft.update()]

            if player.health <= player.max_health * 0.3:
                low_health_sound_timer -= 1
                if low_health_sound_timer <= 0:
                    sound_manager.play('low_health')
                    low_health_sound_timer = 30 # 0.5s

            if player.health <= 0:
                game_state = "GAMEOVER"
                if not game_over_sound_played:
                    sound_manager.play('game_over')
                    game_over_sound_played = True
                save_manager.add_credits(player.score // 10)
                save_manager.add_score("PLAYER", player.score)

        # 3. Draw
        display_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        starfield.draw(display_surf)
        
        if game_state in ["PLAYING", "GAMEOVER"]:
            nebula.draw(display_surf)
            for p in powerups: p.draw(display_surf)
            for b in bullets: b.draw(display_surf)
            for eb in enemy_bullets: eb.draw(display_surf)
            for e in level_manager.enemies: e.draw(display_surf)
            if level_manager.boss: level_manager.boss.draw(display_surf)
            player.draw(display_surf)
            for ex in explosions: ex.draw(display_surf)
            for ft in floating_texts: ft.draw(display_surf, ui.font_small)
            
            screen.blit(display_surf, (shake_x, shake_y))
            ui.draw_hud(screen, player, level_manager, credits=save_manager.data['credits'])
            ui.draw_combo(screen, combo)
            ui.draw_boss_health(screen, level_manager.boss)
            if game_state == "PLAYING":
                 touch_rects = ui.draw_touch_controls(screen)
                 if level_text_timer > 0:
                     ui.draw_level_overlay(screen, level_manager.level)
                 
                 # Low Health Glitch
                 if player.health <= player.max_health * 0.3:
                     # Very slight offset of surface to simulate glitch
                     if random.random() < 0.1:
                         screen.blit(screen, (random.randint(-5, 5), random.randint(-5, 5)), special_flags=pygame.BLEND_ADD)

            if flash_alpha > 0: ui.draw_screen_flash(screen, (255, 50, 50), flash_alpha)
            if game_state == "GAMEOVER":
                ui.draw_game_over(screen, player.score)
                
        elif game_state == "MENU":
            screen.blit(display_surf, (0, 0))
            ui.draw_glass_panel(screen, pygame.Rect(100, 150, 400, 500))
            ui.draw_text(screen, "SPACE SHOOTER", SCREEN_WIDTH//2, 200, center=True, font_type='title')
            ui.draw_text(screen, "Press SPACE to Start", SCREEN_WIDTH//2, 300, center=True, font_type='large')
            ui.draw_text(screen, "Press 'S' for Hanger (Shop)", SCREEN_WIDTH//2, 360, center=True, font_type='small', color=(0, 255, 255))
            ui.draw_leaderboard(screen, save_manager.data['leaderboard'])

        elif game_state == "SHOP":
            screen.blit(display_surf, (0, 0))
            shop_buttons = ui.draw_shop(screen, save_manager.data['credits'], save_manager.data['upgrades'])
            
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0) # Required for web

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
