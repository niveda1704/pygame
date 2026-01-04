
import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        pygame.mixer.init()
        self.load_sounds()

    def load_sounds(self):
        # Sound file paths
        sound_files = {
            'shoot': 'assets/sounds/shoot.wav',
            'explosion': 'assets/sounds/explosion.wav',
            'powerup': 'assets/sounds/powerup.wav',
            'music': 'assets/sounds/bg_music.wav'
        }
        
        for name, path in sound_files.items():
            if os.path.exists(path):
                try:
                    if name == 'music':
                        pygame.mixer.music.load(path)
                        self.sounds['music'] = True
                    else:
                        self.sounds[name] = pygame.mixer.Sound(path)
                except Exception as e:
                    print(f"Error loading sound {path}: {e}")
                    self.sounds[name] = None
            else:
                self.sounds[name] = None

    def play(self, name):
        if name in self.sounds and self.sounds[name]:
            if name != 'music':
                self.sounds[name].play()
    
    def play_music(self):
        if 'music' in self.sounds and self.sounds['music']:
            pygame.mixer.music.play(-1) # Loop indefinitely
