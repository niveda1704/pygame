
# 🚀 Space Shooter Glass

[![Play Online](https://img.shields.io/badge/Play-Live_on_Web-brightgreen?style=for-the-badge&logo=google-chrome&logoColor=white)](https://pygame-ew8v.onrender.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github)](https://github.com/niveda1704/pygame)

A state-of-the-art, **Glassmorphism-styled** arcade shooter built with Python and Pygame. Experience high-octane combat with a modern aesthetic, featuring procedural cosmic effects, vibrant UI, and deep progression systems.

---

## 🎮 Play Now
The game is cross-platform and fully optimized for both Desktop and Mobile browsers!

### **[👉 Click Here to Play the Live Web Version](https://pygame-ew8v.onrender.com/)**

---

## ✨ Premium Features

*   **💎 Glassmorphism UI**: High-fidelity interface with real-time transparency, blurs, and glow effects.
*   **🌌 Dynamic Backgrounds**: Multi-layered Parallax starfields and procedurally drifting cosmic Nebulae.
*   **🛠️ Persistent Hangar**: Collect credits from destroyed enemies to permanently upgrade your engine, fire rate, hull, and magnet range.
*   **⚡ EMP Nova System**: A unique rechargeable secondary weapon that vaporizes surrounding threats and bullets.
*   **👾 Advanced Enemy AI**: 
    *   **Hunters**: Track your horizontal movement relentlessly.
    *   **Tanks**: Massive hulls that require focused fire.
    *   **Vanguards**: Specialized ships that fire back at you.
*   **🎼 Retro-Synth Audio**: 8+ custom-generated SFX including low-health alarms, boss fanfares, and ambient synth loops.

---

## ⌨️ Controls

| Action | Desktop Keyboard | Mobile / Touch |
| :--- | :--- | :--- |
| **Move** | `Arrows` or `WASD` | `<` and `>` Buttons |
| **Primary Fire** | `Space` | `O` Button |
| **EMP Nova** | `Left/Right Shift` | `!` Button |
| **Hangar (Shop)** | `S` (at Menu) | Tap Hangar |
| **Restart** | `R` (Game Over) | Tap Restart |
| **Pause/Menu** | `Esc` | - |

---

## 🛠️ Technical Setup

### **Requirements**
- **Python 3.12+**
- `pygame-ce` or `pygame`

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/niveda1704/pygame.git
   cd pygame/space_shooter
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```

---

## 🚀 Deployment & Web Support
This project uses **Pygbag** to compile Python into WebAssembly (WASM), making it compatible with any modern browser.

**To test the web build locally:**
```bash
python -m pygbag .
```
Then navigate to `http://localhost:8000`.

---

## 📜 Credits & License
Developed with ❤️ by **Niveda Sree**.
Distributed under the MIT License. See `LICENSE` for more information.
