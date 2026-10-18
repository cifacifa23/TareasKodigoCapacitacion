import pygame
import random
import sys
import json
import os
import math
import array

# ==========================================
# ⚙️ CONFIGURACIÓN Y CONSTANTES DE BALANCE (800x800 Base)
# ==========================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60

BOSS_SCORE_INTERVAL = 30       
POWERUP_SPAWN_CHANCE = 0.004   

COLOR_BG = (12, 12, 20)
COLOR_GRID = (25, 25, 40)
COLOR_PLAYER = (102, 252, 241)
COLOR_PLAYER_SHIP = (69, 162, 158)
COLOR_BULLET = (241, 196, 15)
COLOR_ENEMY_BULLET = (231, 76, 60)
COLOR_METEOR = (189, 195, 199)
COLOR_BOSS = (155, 89, 182)
COLOR_SHIELD = (0, 243, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_ACCENT = (231, 76, 60)

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1)
pygame.display.set_caption("CyberSpace Arcade - 800x800 Resizable Edition")

# Ventana redimensionable como base
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
CLOCK = pygame.time.Clock()

FONT_SM = pygame.font.SysFont("Consolas", 18)
FONT_MD = pygame.font.SysFont("Consolas", 24, bold=True)
FONT_LG = pygame.font.SysFont("Consolas", 36, bold=True)

# ==========================================
# 🎵 SISTEMA DE AUDIO PROCEDURAL
# ==========================================
def generar_sonido(freq_inicial, freq_final, duracion, tipo="laser"):
    try:
        sample_rate = 22050
        num_samples = int(sample_rate * duracion)
        buf = array.array('h')
        for i in range(num_samples):
            t = i / sample_rate
            if tipo == "laser":
                freq = freq_inicial - (freq_inicial - freq_final) * (i / num_samples)
                val = int(16383 * math.sin(2 * math.pi * freq * t) * (1 - i / num_samples))
            elif tipo == "explosion":
                val = int(20000 * (random.random() * 2 - 1) * (1 - i / num_samples))
            else:
                freq = freq_inicial + int(100 * math.sin(t * 20))
                val = int(12000 * math.sin(2 * math.pi * freq * t) * (1 - i / num_samples))
            buf.append(val)
        return pygame.mixer.Sound(buffer=buf)
    except Exception:
        return None

SOUND_LASER = generar_sonido(800, 200, 0.1, "laser")
SOUND_EXPLOSION = generar_sonido(200, 50, 0.3, "explosion")
SOUND_POWERUP = generar_sonido(400, 800, 0.2, "powerup")

# ==========================================
# 📊 GESTIÓN DE HIGHSCORES (JSON)
# ==========================================
HIGHSCORE_FILE = "highscore.json"

def cargar_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return json.load(f).get("highscore", 0)
        except:
            return 0
    return 0

def guardar_highscore(score):
    try:
        current = cargar_highscore()
        if score > current:
            with open(HIGHSCORE_FILE, "w") as f:
                json.dump({"highscore": score}, f)
    except:
        pass

# ==========================================
# ✨ SISTEMA DE PARTÍCULAS
# ==========================================
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.life = random.randint(20, 35)
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            size = max(1, int(self.life / 5))
            pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), size, size))

# ==========================================
# 🚀 CLASES DEL JUEGO
# ==========================================
class Player:
    def __init__(self):
        self.width = 46
        self.height = 32
        self.x = SCREEN.get_width() // 2 - self.width // 2
        self.y = SCREEN.get_height() - 90
        self.speed = 6
        self.weapon_level = 1
        self.shield_active = False
        self.shield_timer = 0

    def move(self, keys):
        w, h = SCREEN.get_width(), SCREEN.get_height()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]: self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: self.y += self.speed

        self.x = max(10, min(w - self.width - 10, self.x))
        self.y = max(h // 2, min(h - self.height - 15, self.y))

        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0: self.shield_active = False

    def draw(self, surface):
        if self.shield_active:
            pygame.draw.circle(surface, COLOR_SHIELD, (int(self.x + self.width/2), int(self.y + self.height/2)), 34, 2)
        pygame.draw.rect(surface, COLOR_PLAYER_SHIP, (self.x, self.y + 12, self.width, 16))
        pygame.draw.polygon(surface, COLOR_PLAYER, [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ])

class Meteor:
    def __init__(self, diff_config):
        self.radius = random.randint(18, 32)
        w = SCREEN.get_width()
        self.x = random.randint(self.radius, w - self.radius)
        self.y = -60
        self.speed = random.randint(diff_config["meteor_min_speed"], diff_config["meteor_max_speed"])

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, COLOR_METEOR, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (100, 105, 110), (int(self.x - 4), int(self.y - 4)), self.radius // 3)

class Boss:
    def __init__(self, score_level, diff_config):
        self.w = 150
        self.h = 55
        w = SCREEN.get_width()
        self.x = w // 2 - self.w // 2
        self.y = 60
        self.max_health = 40 + (score_level // BOSS_SCORE_INTERVAL) * 25 * diff_config["boss_health_mult"]
        self.health = self.max_health
        self.direction = 3
        self.shoot_timer = 0
        self.angle_osc = 0

    def update(self):
        w = SCREEN.get_width()
        self.x += self.direction
        self.angle_osc += 0.05
        self.y = 60 + int(20 * math.sin(self.angle_osc))

        if self.x <= 20 or self.x >= w - self.w - 20:
            self.direction *= -1

    def draw(self, surface):
        color_furia = COLOR_ACCENT if self.health < self.max_health * 0.4 else COLOR_BOSS
        pygame.draw.rect(surface, color_furia, (self.x, self.y, self.w, self.h), border_radius=8)
        pygame.draw.rect(surface, COLOR_BULLET, (self.x + 12, self.y + self.h - 10, self.w - 24, 6))
        bar_w = self.w
        current_w = int((self.health / self.max_health) * bar_w)
        pygame.draw.rect(surface, (50, 50, 50), (self.x, self.y - 14, bar_w, 8), border_radius=4)
        pygame.draw.rect(surface, COLOR_ACCENT, (self.x, self.y - 14, current_w, 8), border_radius=4)

class PowerUp:
    def __init__(self):
        self.w = 30
        self.h = 30
        w = SCREEN.get_width()
        self.x = random.randint(30, w - 60)
        self.y = -40
        self.speed = 3
        self.type = random.choice(['weapon', 'shield', 'life'])

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        color = COLOR_BULLET if self.type == 'weapon' else (COLOR_SHIELD if self.type == 'shield' else (46, 204, 113))
        pygame.draw.rect(surface, color, (self.x, self.y, self.w, self.h), border_radius=6)
        letter = 'W' if self.type == 'weapon' else ('S' if self.type == 'shield' else '+')
        txt = FONT_MD.render(letter, True, (0, 0, 0))
        surface.blit(txt, (self.x + 8, self.y + 3))

# ==========================================
# 🎮 MENÚS Y ESTADOS DINÁMICOS
# ==========================================
def menu_dificultad():
    selected = 1
    options = [
        {"name": "FÁCIL", "vidas": 5, "meteor_min_speed": 2, "meteor_max_speed": 5, "spawn_rate": 35, "boss_health_mult": 0.8},
        {"name": "NORMAL", "vidas": 3, "meteor_min_speed": 4, "meteor_max_speed": 7, "spawn_rate": 25, "boss_health_mult": 1.0},
        {"name": "DIFÍCIL", "vidas": 1, "meteor_min_speed": 6, "meteor_max_speed": 10, "spawn_rate": 18, "boss_health_mult": 1.4}
    ]
    highscore = cargar_highscore()

    while True:
        w, h = SCREEN.get_width(), SCREEN.get_height()
        SCREEN.fill(COLOR_BG)
        
        # Rejilla adaptativa
        for x in range(0, w, 50):
            pygame.draw.line(SCREEN, COLOR_GRID, (x, 0), (x, h))
        for y in range(0, h, 50):
            pygame.draw.line(SCREEN, COLOR_GRID, (0, y), (w, y))

        title = FONT_LG.render("CYBER ARCADE 800x800", True, COLOR_PLAYER)
        hs_txt = FONT_MD.render(f"Récord Histórico: {highscore} pts", True, COLOR_BULLET)
        sub = FONT_MD.render("SELECCIONA DIFICULTAD", True, COLOR_TEXT)
        
        SCREEN.blit(title, (w//2 - title.get_width()//2, h//2 - 200))
        SCREEN.blit(hs_txt, (w//2 - hs_txt.get_width()//2, h//2 - 150))
        SCREEN.blit(sub, (w//2 - sub.get_width()//2, h//2 - 100))

        for i, opt in enumerate(options):
            color = COLOR_BULLET if (i + 1) == selected else COLOR_TEXT
            prefix = "> " if (i + 1) == selected else "  "
            txt = FONT_MD.render(f"{prefix}{opt['name']} (Vidas: {opt['vidas']})", True, color)
            SCREEN.blit(txt, (w//2 - 160, h//2 - 30 + (i * 55)))

        hint = FONT_SM.render("[W/S] Cambiar | [ENTER] Jugar | [F] Pantalla Completa", True, (150, 150, 180))
        SCREEN.blit(hint, (w//2 - hint.get_width()//2, h - 80))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w): selected = max(1, selected - 1)
                elif event.key in (pygame.K_DOWN, pygame.K_s): selected = min(3, selected + 1)
                elif event.key == pygame.K_RETURN: return options[selected - 1]
                elif event.key == pygame.K_f:
                    # Alternar Fullscreen
                    pygame.display.toggle_fullscreen()

def pantalla_pausa():
    w, h = SCREEN.get_width(), SCREEN.get_height()
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((12, 12, 20, 200))
    SCREEN.blit(overlay, (0, 0))

    txt_pause = FONT_LG.render("JUEGO PAUSADO", True, COLOR_PLAYER)
    txt_inst = FONT_SM.render("Presiona [P] o [ESC] para Reanudar", True, COLOR_TEXT)
    txt_quit = FONT_SM.render("Presiona [Q] para salir al Menú", True, COLOR_ACCENT)

    SCREEN.blit(txt_pause, (w//2 - txt_pause.get_width()//2, h//2 - 60))
    SCREEN.blit(txt_inst, (w//2 - txt_inst.get_width()//2, h//2))
    SCREEN.blit(txt_quit, (w//2 - txt_quit.get_width()//2, h//2 + 40))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_p, pygame.K_ESCAPE): return "resume"
                elif event.key == pygame.K_q: return "quit"

# ==========================================
# 🎮 BUCLE PRINCIPAL
# ==========================================
def ejecutar_juego(diff_config):
    player = Player()
    player.max_vidas = diff_config["vidas"]
    player.vidas = diff_config["vidas"]
    
    bullets, enemy_bullets, meteors, powerups, particles = [], [], [], [], []
    score = 0
    boss = None
    spawn_counter = 0

    running = True
    while running:
        CLOCK.tick(FPS)
        w, h = SCREEN.get_width(), SCREEN.get_height()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    if pantalla_pausa() == "quit": return
                elif event.key == pygame.K_SPACE:
                    if SOUND_LASER: SOUND_LASER.play()
                    if player.weapon_level == 1:
                        bullets.append([player.x + player.width//2 - 2, player.y, 0])
                    elif player.weapon_level == 2:
                        bullets.append([player.x + 6, player.y, 0])
                        bullets.append([player.x + player.width - 12, player.y, 0])
                    else:
                        bullets.append([player.x + player.width//2 - 2, player.y, 0])
                        bullets.append([player.x + 4, player.y, -2])
                        bullets.append([player.x + player.width - 10, player.y, 2])

        keys = pygame.key.get_pressed()
        player.move(keys)

        if score > 0 and score % BOSS_SCORE_INTERVAL == 0 and boss is None:
            boss = Boss(score, diff_config)
            meteors.clear()

        if boss is None:
            spawn_counter += 1
            if spawn_counter >= diff_config["spawn_rate"]:
                spawn_counter = 0
                meteors.append(Meteor(diff_config))

            if random.random() < POWERUP_SPAWN_CHANCE:
                powerups.append(PowerUp())

            for m in meteors[:]:
                m.update()
                dist_sq = (player.x + player.width/2 - m.x)**2 + (player.y + player.height/2 - m.y)**2
                if dist_sq < (m.radius + 18)**2:
                    meteors.remove(m)
                    if SOUND_EXPLOSION: SOUND_EXPLOSION.play()
                    for _ in range(14): particles.append(Particle(m.x, m.y, COLOR_METEOR))
                    if player.shield_active: player.shield_active = False
                    else: player.vidas -= 1
                    if player.vidas <= 0: running = False
                elif m.y > h + 60: meteors.remove(m)
        else:
            boss.update()
            boss.shoot_timer += 1
            if boss.shoot_timer >= 35:
                boss.shoot_timer = 0
                bx = boss.x + boss.w // 2
                by = boss.y + boss.h
                enemy_bullets.append([bx, by, 0])
                enemy_bullets.append([bx, by, -2])
                enemy_bullets.append([bx, by, 2])

            if (boss.x < player.x + player.width and boss.x + boss.w > player.x and
                boss.y < player.y + player.height and boss.y + boss.h > player.y):
                if not player.shield_active: player.vidas -= 1
                if player.vidas <= 0: running = False

        for p in powerups[:]:
            p.update()
            if (player.x < p.x + p.w and player.x + player.width > p.x and
                player.y < p.y + p.h and player.y + player.height > p.y):
                if SOUND_POWERUP: SOUND_POWERUP.play()
                if p.type == 'weapon': player.weapon_level = min(3, player.weapon_level + 1)
                elif p.type == 'shield':
                    player.shield_active = True
                    player.shield_timer = 300
                elif p.type == 'life': player.vidas = min(player.max_vidas, player.vidas + 1)
                powerups.remove(p)
            elif p.y > h: powerups.remove(p)

        for b in bullets[:]:
            b[1] -= 10
            b[0] += b[2]
            if b[1] < 0:
                bullets.remove(b)
                continue

            if boss is not None:
                if (boss.x < b[0] < boss.x + boss.w and boss.y < b[1] < boss.y + boss.h):
                    if b in bullets: bullets.remove(b)
                    boss.health -= 1
                    if SOUND_EXPLOSION: SOUND_EXPLOSION.play()
                    for _ in range(5): particles.append(Particle(b[0], b[1], COLOR_BOSS))
                    if boss.health <= 0:
                        score += 15
                        for _ in range(50): particles.append(Particle(boss.x + boss.w//2, boss.y + boss.h//2, COLOR_ACCENT))
                        boss = None
            else:
                hit = False
                for m in meteors[:]:
                    if (m.x - m.radius < b[0] < m.x + m.radius) and (m.y - m.radius < b[1] < m.y + m.radius):
                        meteors.remove(m)
                        score += 1
                        if SOUND_EXPLOSION: SOUND_EXPLOSION.play()
                        for _ in range(12): particles.append(Particle(m.x, m.y, COLOR_METEOR))
                        hit = True
                        break
                if hit and b in bullets: bullets.remove(b)

        for eb in enemy_bullets[:]:
            eb[1] += 5
            eb[0] += eb[2]
            if eb[1] > h or eb[0] < 0 or eb[0] > w:
                enemy_bullets.remove(eb)
                continue
            if (player.x < eb[0] < player.x + player.width and player.y < eb[1] < player.y + player.height):
                enemy_bullets.remove(eb)
                if player.shield_active: player.shield_active = False
                else: player.vidas -= 1
                if player.vidas <= 0: running = False

        for pt in particles[:]:
            pt.update()
            if pt.life <= 0: particles.remove(pt)

        # Renderizado
        SCREEN.fill(COLOR_BG)
        for x in range(0, w, 50):
            pygame.draw.line(SCREEN, COLOR_GRID, (x, 0), (x, h))

        player.draw(SCREEN)
        for m in meteors: m.draw(SCREEN)
        for p in powerups: p.draw(SCREEN)
        for pt in particles: pt.draw(SCREEN)
        for b in bullets: pygame.draw.rect(SCREEN, COLOR_BULLET, (b[0], b[1], 5, 14), border_radius=2)
        for eb in enemy_bullets: pygame.draw.rect(SCREEN, COLOR_ENEMY_BULLET, (eb[0], eb[1], 7, 14), border_radius=2)
        if boss is not None: boss.draw(SCREEN)

        txt_score = FONT_MD.render(f"SCORE: {score}", True, COLOR_TEXT)
        txt_lives = FONT_MD.render(f"VIDAS: {player.vidas}", True, COLOR_ACCENT if player.vidas == 1 else COLOR_TEXT)
        txt_weapon = FONT_MD.render(f"ARMA LVL: {player.weapon_level}", True, COLOR_BULLET)
        
        SCREEN.blit(txt_score, (20, 15))
        SCREEN.blit(txt_lives, (250, 15))
        SCREEN.blit(txt_weapon, (480, 15))

        pygame.display.flip()

    guardar_highscore(score)
    highscore_actual = cargar_highscore()

    SCREEN.fill(COLOR_BG)
    txt_go = FONT_LG.render("GAME OVER", True, COLOR_ACCENT)
    txt_sc = FONT_MD.render(f"Puntuación Final: {score}", True, COLOR_TEXT)
    txt_hs = FONT_MD.render(f"Mejor Récord: {highscore_actual}", True, COLOR_BULLET)
    txt_re = FONT_SM.render("Presiona [ENTER] para reiniciar o [Q] para salir", True, (150, 150, 180))
    
    SCREEN.blit(txt_go, (w//2 - txt_go.get_width()//2, h//2 - 100))
    SCREEN.blit(txt_sc, (w//2 - txt_sc.get_width()//2, h//2 - 40))
    SCREEN.blit(txt_hs, (w//2 - txt_hs.get_width()//2, h//2), )
    SCREEN.blit(txt_re, (w//2 - txt_re.get_width()//2, h//2 + 60))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    while True:
        configuracion = menu_dificultad()
        ejecutar_juego(configuracion)