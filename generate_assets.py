
import wave
import math
import struct
import random
import os

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Parameters
SAMPLE_RATE = 44100

def generate_tone(frequency, duration, volume=0.5):
    n_samples = int(SAMPLE_RATE * duration)
    data = []
    for i in range(n_samples):
        # Sine wave
        value = math.sin(2 * math.pi * frequency * i / SAMPLE_RATE)
        # Add basic decay for some sounds
        amp = volume * 32767
        data.append(int(value * amp))
    return data

def generate_noise(duration, volume=0.5):
    n_samples = int(SAMPLE_RATE * duration)
    data = []
    for i in range(n_samples):
        value = random.uniform(-1, 1)
        amp = volume * 32767 * (1 - (i/n_samples)) # Decay
        data.append(int(value * amp))
    return data

def generate_music_loop(duration=10):
    # Simple Arpeggio C Major: C, E, G
    notes = [261.63, 329.63, 392.00, 523.25] # C4, E4, G4, C5
    tempo = 0.2
    data = []
    
    total_samples = int(SAMPLE_RATE * duration)
    current_sample = 0
    
    while current_sample < total_samples:
        for note in notes:
            # Generate shorter notes
            n_samples = int(SAMPLE_RATE * tempo)
            for i in range(n_samples):
                t = i / SAMPLE_RATE
                # Sawtooth-ish wave for retro feel
                value = (2 * (t * note - math.floor(0.5 + t * note))) 
                amp = 0.2 * 32767
                data.append(int(value * amp))
            current_sample += n_samples
            if current_sample >= total_samples: break
            
    return data[:total_samples]

def save_wav(filename, data):
    with wave.open(filename, 'w') as f:
        f.setnchannels(1) # Mono
        f.setsampwidth(2) # 2 bytes (16-bit)
        f.setframerate(SAMPLE_RATE)
        # Convert to bytes
        packed_data = struct.pack('<' + ('h' * len(data)), *data)
        f.writeframes(packed_data)
    print(f"Generated {filename}")

def main():
    base_path = "d:/game/space_shooter/assets/sounds"
    create_dir(base_path)

    # 1. Shoot Sound (Shorter, crisp kick)
    shoot_data = []
    duration = 0.1
    for i in range(int(SAMPLE_RATE * duration)):
        freq = 1200 - (i / (SAMPLE_RATE * duration)) * 800 
        val = math.sin(2 * math.pi * freq * i / SAMPLE_RATE)
        # Add a bit of noise for texture
        val += random.uniform(-0.1, 0.1)
        shoot_data.append(int(val * 0.4 * 32767 * (1 - i/(SAMPLE_RATE * duration))))
    save_wav(f"{base_path}/shoot.wav", shoot_data)

    # 2. Explosion (Stronger Noise decay)
    exp_data = generate_noise(0.6, 0.7)
    save_wav(f"{base_path}/explosion.wav", exp_data)

    # 3. Powerup (Rising complex chime)
    pup_data = []
    duration = 0.4
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / (SAMPLE_RATE * duration)
        freq = 400 + t * 400 + math.sin(t * 20) * 50 # Vibrato rising
        val = math.sin(2 * math.pi * freq * i / SAMPLE_RATE)
        pup_data.append(int(val * 0.5 * 32767 * (1 - t)))
    save_wav(f"{base_path}/powerup.wav", pup_data)

    # 4. Damage Sound (Low thud)
    dmg_data = []
    duration = 0.2
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / (SAMPLE_RATE * duration)
        freq = 150 - t * 100
        val = math.sin(2 * math.pi * freq * i / SAMPLE_RATE)
        # Add grit
        if random.random() > 0.8: val = random.uniform(-1, 1)
        dmg_data.append(int(val * 0.6 * 32767 * (1 - t)))
    save_wav(f"{base_path}/damage.wav", dmg_data)

    # 5. Game Over (Descending fail tone)
    go_data = []
    duration = 1.0
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / (SAMPLE_RATE * duration)
        freq = 300 - t * 250
        val = math.sin(2 * math.pi * freq * i / SAMPLE_RATE)
        # Pulse effect
        val *= (0.5 + 0.5 * math.sin(t * 30))
        go_data.append(int(val * 0.5 * 32767 * (1 - t)))
    save_wav(f"{base_path}/game_over.wav", go_data)

    # 6. Boss Enter (Dramatic sweep)
    boss_data = []
    duration = 1.5
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / (SAMPLE_RATE * duration)
        freq = 100 + math.sin(t * 5) * 50
        val = math.sin(2 * math.pi * freq * i / SAMPLE_RATE)
        # Low rumble noise
        val += random.uniform(-0.2, 0.2)
        boss_data.append(int(val * 0.7 * 32767 * (1 - t*0.5)))
    save_wav(f"{base_path}/boss_enter.wav", boss_data)

    # 7. Level Complete (Victory chime)
    win_data = []
    duration = 0.8
    notes = [440, 554, 659, 880] # A Major arpeggio
    samples_per_note = int(SAMPLE_RATE * duration / len(notes))
    for note in notes:
        for i in range(samples_per_note):
            t = i / samples_per_note
            val = math.sin(2 * math.pi * note * i / SAMPLE_RATE)
            win_data.append(int(val * 0.5 * 32767 * (1 - t)))
    save_wav(f"{base_path}/level_complete.wav", win_data)

    # 9. Low Health Alarm (Periodic beep)
    alarm_data = []
    duration = 0.5
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / (SAMPLE_RATE * duration)
        freq = 600
        # Beep for 0.1s, silence for 0.4s
        if t < 0.2:
            val = math.sin(2 * math.pi * freq * i / SAMPLE_RATE)
            alarm_data.append(int(val * 0.3 * 32767))
        else:
            alarm_data.append(0)
    save_wav(f"{base_path}/low_health.wav", alarm_data)

    # 10. Background Music (Updated Arpeggio Loop)
    music_data = generate_music_loop(16.0) 
    save_wav(f"{base_path}/bg_music.wav", music_data)

if __name__ == "__main__":
    main()
