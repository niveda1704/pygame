
import pygame

class UI:
    def __init__(self, font_name=None):
        self.font_small = pygame.font.SysFont("arial", 18) if font_name is None else pygame.font.Font(font_name, 18)
        self.font_large = pygame.font.SysFont("arial", 36) if font_name is None else pygame.font.Font(font_name, 36)
        self.font_title = pygame.font.SysFont("arial", 64, bold=True) if font_name is None else pygame.font.Font(font_name, 64)

    def draw_glass_panel(self, surface, rect, color=(255, 255, 255, 30), border_radius=15, border_color=(255, 255, 255, 100)):
        """
        Draws a rectangle with a glassmorphism effect.
        """
        # Create a surface for the panel
        panel_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        
        # Draw the main semi-transparent fill
        pygame.draw.rect(panel_surf, color, panel_surf.get_rect(), border_radius=border_radius)
        
        # Draw a subtle border/stroke to define edges (the "shine")
        pygame.draw.rect(panel_surf, border_color, panel_surf.get_rect(), 2, border_radius=border_radius)
        
        surface.blit(panel_surf, rect)

    def draw_bar(self, surface, x, y, width, height, value, max_value, color=(0, 255, 100)):
        # Background bar
        bg_rect = pygame.Rect(x, y, width, height)
        self.draw_glass_panel(surface, bg_rect, color=(50, 50, 50, 150), border_radius=5)

        # Foreground bar
        if value > 0:
            fill_width = int((value / max_value) * width)
            fill_rect = pygame.Rect(x, y, fill_width, height)
            
            # Create a glowy bar
            bar_surf = pygame.Surface((fill_width, height), pygame.SRCALPHA)
            pygame.draw.rect(bar_surf, (*color, 200), bar_surf.get_rect(), border_radius=5)
            surface.blit(bar_surf, (x, y))

    def draw_text(self, surface, text, x, y, center=False, font_type='small', color=(255, 255, 255)):
        font = self.font_small
        if font_type == 'large':
            font = self.font_large
        elif font_type == 'title':
            font = self.font_title

        text_surf = font.render(text, True, color)
        
        # Simple drop shadow for readability
        shadow_surf = font.render(text, True, (0, 0, 0, 128))
        
        rect = text_surf.get_rect()
        if center:
            rect.center = (x, y)
            surface.blit(shadow_surf, (rect.x + 2, rect.y + 2))
            surface.blit(text_surf, rect)
        else:
            rect.topleft = (x, y)
            surface.blit(shadow_surf, (rect.x + 2, rect.y + 2))
            surface.blit(text_surf, rect)

    def draw_boss_health(self, surface, boss):
        if boss and boss.active:
            screen_w = surface.get_width()
            bar_w = 400
            bar_h = 20
            x = (screen_w - bar_w) // 2
            y = 80
            
            self.draw_text(surface, "BOSS", screen_w // 2, y - 25, center=True, font_type='large', color=(255, 50, 50))
            self.draw_bar(surface, x, y, bar_w, bar_h, boss.health, boss.max_health, color=(255, 50, 50))

    def draw_hud(self, surface, player, level_manager):
        # Top Left: Score & Level
        panel_w, panel_h = 200, 80
        pad = 20
        self.draw_glass_panel(surface, pygame.Rect(pad, pad, panel_w, panel_h))
        
        self.draw_text(surface, f"Score: {player.score}", pad + 15, pad + 15, font_type='small')
        self.draw_text(surface, f"Level: {level_manager.level}", pad + 15, pad + 45, font_type='small')

        # Top Right: Health
        health_panel_w = 220
        self.draw_glass_panel(surface, pygame.Rect(surface.get_width() - health_panel_w - pad, pad, health_panel_w, panel_h))
        self.draw_text(surface, "Health", surface.get_width() - health_panel_w - pad + 15, pad + 10, font_type='small')
        self.draw_bar(surface, surface.get_width() - health_panel_w - pad + 15, pad + 40, 190, 20, player.health, player.max_health, color=(0, 200, 255))

    def draw_game_over(self, surface, score):
        w, h = surface.get_width(), surface.get_height()
        # Dark overlay
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Glass panel
        panel_w, panel_h = 400, 300
        panel_rect = pygame.Rect((w - panel_w)//2, (h - panel_h)//2, panel_w, panel_h)
        self.draw_glass_panel(surface, panel_rect, color=(50, 50, 70, 200), border_radius=30)

        self.draw_text(surface, "GAME OVER", w//2, h//2 - 80, center=True, font_type='title')
        self.draw_text(surface, f"Final Score: {score}", w//2, h//2 + 10, center=True, font_type='large')
        self.draw_text(surface, "Press 'R' to Restart", w//2, h//2 + 80, center=True, font_type='small', color=(200, 200, 200))

    def draw_touch_controls(self, surface):
        """
        Draws on-screen controls for touch devices.
        Returns a dictionary of rects for input handling.
        """
        w, h = surface.get_width(), surface.get_height()
        btn_size = 80
        margin = 30
        
        # Positions
        left_rect = pygame.Rect(margin, h - margin - btn_size, btn_size, btn_size)
        right_rect = pygame.Rect(margin + btn_size + 20, h - margin - btn_size, btn_size, btn_size)
        shoot_rect = pygame.Rect(w - margin - btn_size, h - margin - btn_size, btn_size, btn_size)
        
        # Draw Left Btn
        self.draw_glass_panel(surface, left_rect, color=(255, 255, 255, 50), border_radius=40)
        self.draw_text(surface, "<", left_rect.centerx, left_rect.centery - 10, center=True, font_type='large')
        
        # Draw Right Btn
        self.draw_glass_panel(surface, right_rect, color=(255, 255, 255, 50), border_radius=40)
        self.draw_text(surface, ">", right_rect.centerx, right_rect.centery - 10, center=True, font_type='large')
        
        # Draw Shoot Btn
        self.draw_glass_panel(surface, shoot_rect, color=(255, 100, 100, 50), border_radius=40)
        self.draw_text(surface, "O", shoot_rect.centerx, shoot_rect.centery - 10, center=True, font_type='large')
        
        return {
            'left': left_rect,
            'right': right_rect,
            'shoot': shoot_rect
        }
