import pygame
import random
import sys
import math
import os

# ============================================================
# ================== ANTIBODY: INMUNO-LABERINTO ================
# ============================================================
# Reconstruido con todos los pedidos de Enero a Febrero
# Imágenes biológicas reales (buscadas y cargadas)
# Estilo Laberinto y Presentación FNF

pygame.init()
pygame.mixer.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pygame.display.set_caption("ANTIBODY: Inmuno-Laberinto")
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

# Forzar inicialización de audio con parámetros estándar
try:
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 512)
    print("Mixer inicializado correctamente")
except Exception as e:
    print(f"Error inicializando mixer: {e}")

# Colores (Paleta Biológica)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (220, 20, 60)
ROJO_OSCURO = (100, 5, 5)
VERDE = (50, 205, 50)
AZUL = (30, 144, 255)
AMARILLO = (255, 215, 0)
CIAN = (0, 255, 255)
MAGENTA = (199, 21, 133)
GRIS_OSCURO = (30, 30, 30)

# Fuentes
fuente_std = pygame.font.SysFont("Impact", 24)
fuente_grande = pygame.font.SysFont("Impact", 60)
fuente_peque = pygame.font.SysFont("Impact", 18)

# ============================================================
# ===================== CARGA DE ACTIVOS ======================
# ============================================================

def cargar_grafico(nombre, tamano, color_fallback):
    # Buscamos en la carpeta assets dentro de Sistemas
    path = os.path.join(os.path.dirname(__file__), "assets", nombre)
    try:
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, tamano)
    except Exception as e:
        print(f"Error cargando {nombre}: {e}")
    
    # Fallback si no se encuentra la imagen (Crea un gráfico procedural)
    surf = pygame.Surface(tamano, pygame.SRCALPHA)
    if "virus" in nombre or "bacteria" in nombre:
        pygame.draw.circle(surf, color_fallback, (tamano[0]//2, tamano[1]//2), tamano[0]//2)
        for i in range(8):
            rad = math.radians(i * 45)
            px = tamano[0]//2 + math.cos(rad) * tamano[0]//2
            py = tamano[1]//2 + math.sin(rad) * tamano[1]//2
            pygame.draw.line(surf, color_fallback, (tamano[0]//2, tamano[1]//2), (px, py), 2)
    elif "profesor" in nombre:
        pygame.draw.rect(surf, color_fallback, (0, 0, tamano[0], tamano[1]), border_radius=10)
        pygame.draw.circle(surf, BLANCO, (tamano[0]//2, tamano[1]//3), tamano[0]//4)
    else:
        pygame.draw.ellipse(surf, color_fallback, (0, 0, tamano[0], tamano[1]))
    return surf

# Carga de imágenes reales
IMG_PLAYER = cargar_grafico("jugador.png", (45, 45), AZUL)
IMG_PLAYER_MUSCLE = cargar_grafico("jugador_muscular.png", (60, 60), AZUL)
IMG_VIRUS = cargar_grafico("virus.png", (40, 40), ROJO)
IMG_BACTERIA = cargar_grafico("bacteria.png", (50, 50), VERDE)
IMG_BOSS = cargar_grafico("boss5.png", (80, 80), MAGENTA)
IMG_FINAL_BOSS = cargar_grafico("boss10.png", (120, 120), (150, 0, 150))
IMG_RAYO = cargar_grafico("rayo.png", (80, 40), AMARILLO)
IMG_PROFESOR = cargar_grafico("profesor.png", (120, 120), CIAN)
IMG_TUMOR_AVATAR = cargar_grafico("avatar_tumor.png", (120, 120), (150, 0, 150))
IMG_ESPADA = cargar_grafico("espada.png", (60, 30), BLANCO)
IMG_ITEM_VIDA = cargar_grafico("item_vida.png", (30, 30), VERDE)
IMG_ITEM_XP = cargar_grafico("item_xp.png", (30, 30), AMARILLO)
IMG_ITEM_TROFEO = cargar_grafico("trofeo.png", (35, 35), (255, 215, 0))
IMG_PUERTA = cargar_grafico("puerta.png", (60, 60), (0, 255, 100))
IMG_INICIO = cargar_grafico("pantalla_inicio.png", (ANCHO, ALTO), NEGRO)

# ============================================================
# ===================== CARGA DE SONIDOS ======================
# ============================================================

def cargar_sonido(nombre):
    path = os.path.join(os.path.dirname(__file__), "assets", "sounds", nombre)
    try:
        if os.path.exists(path):
            s = pygame.mixer.Sound(path)
            s.set_volume(0.6) # Volumen al 60%
            return s
        else:
            print(f"Archivo no encontrado: {path}")
    except Exception as e:
        print(f"Error cargando sonido {nombre}: {e}")
    return None

SND_GOLPE = cargar_sonido("golpe.wav")
SND_MUERTE = cargar_sonido("muerte.wav")
SND_NIVEL = cargar_sonido("nivel.wav")
SND_PUERTA = cargar_sonido("puerta.wav")
SND_DANO = cargar_sonido("dano.wav")
SND_TALK = cargar_sonido("talk.wav")

def reproducir_snd(snd):
    if snd: 
        try:
            snd.play()
        except:
            pass

# ============================================================
# ========================= CLASES ===========================
# ============================================================

class Puerta(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo="SALIDA"):
        super().__init__()
        self.tipo = tipo
        self.image = IMG_PUERTA
        if tipo == "ENTRADA":
            # Puerta de entrada es azulada/cian
            self.image = pygame.transform.rotate(IMG_PUERTA, 180)
            self.image.fill((0, 100, 255, 150), special_flags=pygame.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect(center=(x, y))
        self.visible = True # Siempre visible

    def update(self):
        pass # Ya no depende de enemigos

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)
            # Efecto de brillo
            color = (0, 255, 100, 100) if self.tipo == "SALIDA" else (0, 150, 255, 100)
            glow = pygame.Surface((self.rect.width+10, self.rect.height+10), pygame.SRCALPHA)
            pygame.draw.rect(glow, color, (0, 0, self.rect.width+10, self.rect.height+10), border_radius=15)
            surface.blit(glow, (self.rect.x-5, self.rect.y-5))

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = IMG_PLAYER
        self.rect = self.image.get_rect(center=(ANCHO//2, ALTO//2))
        self.velocidad = 5
        self.vida = 100
        self.vida_max = 100
        self.energia = 100
        self.escudo_activo = False
        self.escudo_energia = 0
        self.xp = 0
        self.nivel = 1
        self.area_actual = 1
        self.trofeos = 0
        self.rayos = 0
        self.invencible = False
        self.timer_invencible = 0
        self.evolucionado = False
        self.direccion = [0, 1]
        self.last_attack = 0
        self.last_shot = 0
        self.boss5_derrotado = False

    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -1; self.direccion = [-1, 0]
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = 1; self.direccion = [1, 0]
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -1; self.direccion = [0, -1]
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = 1; self.direccion = [0, 1]

        if dx != 0 and dy != 0:
            dx *= 0.707; dy *= 0.707

        # Movimiento con colisión de laberinto
        old_x = self.rect.x
        self.rect.x += dx * self.velocidad
        if pygame.sprite.spritecollideany(self, paredes_grp):
            self.rect.x = old_x
            
        old_y = self.rect.y
        self.rect.y += dy * self.velocidad
        if pygame.sprite.spritecollideany(self, paredes_grp):
            self.rect.y = old_y

        self.rect.clamp_ip(pantalla.get_rect())

        # Mecánica de Energía
        if dx != 0 or dy != 0:
            self.energia = max(0, self.energia - 0.08)
        else:
            self.energia = min(100, self.energia + 0.15)

        # Escudo (Se desbloquea a los 7 trofeos)
        if self.trofeos >= 7:
            self.escudo_activo = True
            if self.escudo_energia < 100:
                self.escudo_energia += 0.05
        else:
            self.escudo_activo = False

        # Evolución al Nivel 5 (ELIMINADO por petición del usuario)
        # Solo evoluciona contra el Boss Final si la vida < 50%
        if self.area_actual == 10 and boss is not None and self.vida < 50 and not self.evolucionado:
            self.evolucionado = True
            self.image = IMG_PLAYER_MUSCLE
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)
            iniciar_intro("¡EVOLUCIÓN MUSCULAR FINAL!")

        # Estado Invencible
        if self.timer_invencible > 0:
            self.timer_invencible -= 1
            # Parpadeo más rápido para feedback de invulnerabilidad
            if (self.timer_invencible // 5) % 2 == 0: 
                self.image.set_alpha(150)
            else: 
                self.image.set_alpha(255)
                
            if self.timer_invencible == 0:
                self.invencible = False
                self.image.set_alpha(255)

    def recibir_dano(self, cantidad):
        if not self.invencible:
            if self.escudo_activo and self.escudo_energia > 0:
                self.escudo_energia -= cantidad * 0.5
            else:
                self.vida -= cantidad
            
            # Activar invulnerabilidad por 3 segundos (180 frames a 60 FPS)
            self.invencible = True
            self.timer_invencible = 180
            return True
        return False

    def atacar_espada(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.last_attack > 300:
            self.last_attack = ahora
            espada = Espada(self.rect.centerx, self.rect.centery, self.direccion)
            espadas_grp.add(espada)
            todos_sprites.add(espada)

    def disparar(self):
        # Disparo normal (opcional, ahora el ataque principal es espada)
        ahora = pygame.time.get_ticks()
        if ahora - self.last_shot > 400:
            self.last_shot = ahora
            b = Bala(self.rect.centerx, self.rect.centery, self.direccion)
            balas_grp.add(b)
            todos_sprites.add(b)

class Espada(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        super().__init__()
        angle = math.degrees(math.atan2(-dir[1], dir[0]))
        self.original_image = IMG_ESPADA
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x + dir[0]*40, y + dir[1]*40)
        self.timer = 10

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo="VIDA"):
        super().__init__()
        self.tipo = tipo
        if tipo == "VIDA": self.image = IMG_ITEM_VIDA
        elif tipo == "XP": self.image = IMG_ITEM_XP
        elif tipo == "TROFEO": self.image = IMG_ITEM_TROFEO
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Animación simple
        self.rect.y += math.sin(pygame.time.get_ticks() * 0.01) * 0.5

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        super().__init__()
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, CIAN, (6, 6), 6)
        pygame.draw.circle(self.image, BLANCO, (6, 6), 3)
        self.rect = self.image.get_rect(center=(x, y))
        self.dir = dir
        self.vel = 12

    def update(self):
        self.rect.x += self.dir[0] * self.vel
        self.rect.y += self.dir[1] * self.vel
        if not pantalla.get_rect().contains(self.rect) or pygame.sprite.spritecollideany(self, paredes_grp):
            self.kill()

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, tipo="VIRUS"):
        super().__init__()
        self.image = IMG_VIRUS if tipo == "VIRUS" else IMG_BACTERIA
        self.vida = 30 if tipo == "VIRUS" else 60
        self.vel = random.uniform(1.5, 3.5) if tipo == "VIRUS" else random.uniform(0.8, 2.0)
        
        intentos = 0
        while intentos < 100:
            self.rect = self.image.get_rect(center=(random.randint(50, ANCHO-50), random.randint(120, ALTO-50)))
            dist_jugador = math.hypot(self.rect.centerx - jugador.rect.centerx, self.rect.centery - jugador.rect.centery)
            if not pygame.sprite.spritecollideany(self, paredes_grp) and dist_jugador > 200:
                break
            intentos += 1

    def update(self):
        dx = jugador.rect.centerx - self.rect.centerx
        dy = jugador.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.rect.x += (dx / dist) * self.vel
            self.rect.y += (dy / dist) * self.vel

class Boss(pygame.sprite.Sprite):
    def __init__(self, tipo="NORMAL"):
        super().__init__()
        self.tipo = tipo
        if tipo == "FINAL":
            self.image = IMG_FINAL_BOSS
            self.vida = 2500
            self.vida_max = 2500
        else:
            self.image = IMG_BOSS
            self.vida = 800
            self.vida_max = 800
        
        self.rect = self.image.get_rect(center=(ANCHO//2, 250))
        self.timer_shot = 0
        self.angulo = 0
        self.vel = 1.8 if tipo == "NORMAL" else 3
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

    def update(self):
        # Movimiento del Boss (Ambos jefes se mueven ahora)
        self.rect.x += self.dx * self.vel
        self.rect.y += self.dy * self.vel
        
        # Rebotar en bordes o seguir al jugador levemente
        limite_inferior = ALTO - 200 if self.tipo == "NORMAL" else ALTO - 150
        if self.rect.left < 50 or self.rect.right > ANCHO - 50: self.dx *= -1
        if self.rect.top < 50 or self.rect.bottom > limite_inferior: self.dy *= -1
        
        # El jefe final es más agresivo en su seguimiento
        prob_cambio = 0.04 if self.tipo == "FINAL" else 0.02
        if random.random() < prob_cambio:
            if jugador.rect.centerx > self.rect.centerx: self.dx = 1
            else: self.dx = -1
            if jugador.rect.centery > self.rect.centery: self.dy = 1
            else: self.dy = -1

        self.timer_shot += 1
        frecuencia = 15 if self.tipo == "FINAL" else 25
        if self.timer_shot % frecuencia == 0:
            paso = 20 if self.tipo == "FINAL" else 30
            for i in range(0, 360, paso):
                rad = math.radians(i + self.angulo)
                vx, vy = math.cos(rad), math.sin(rad)
                b = BalaEnemiga(self.rect.centerx, self.rect.centery, (vx, vy))
                balas_enemigas_grp.add(b)
                todos_sprites.add(b)
            self.angulo += 15 if self.tipo == "NORMAL" else 25

class BalaEnemiga(pygame.sprite.Sprite):
    def __init__(self, x, y, vec):
        super().__init__()
        self.image = pygame.Surface((14, 14), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 50, 50), (7, 7), 7)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx, self.vy = vec
        self.speed = 6

    def update(self):
        self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed
        if not pantalla.get_rect().contains(self.rect): self.kill()

class Rayo(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        super().__init__()
        angle = math.degrees(math.atan2(-dir[1], dir[0]))
        self.image = pygame.transform.rotate(IMG_RAYO, angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.dir = dir
        self.vel = 18
        self.hits = 0
        self.objetivos_golpeados = []

    def update(self):
        self.rect.x += self.dir[0] * self.vel
        self.rect.y += self.dir[1] * self.vel
        
        # Atraviesa hasta 5 enemigos
        for e in enemigos_grp:
            if self.rect.colliderect(e.rect) and e not in self.objetivos_golpeados:
                e.vida -= 60
                self.objetivos_golpeados.append(e)
                self.hits += 1
                if e.vida <= 0:
                    drop_item(e.rect.centerx, e.rect.centery)
                    jugador.xp += 25; e.kill()
        
        if boss and self.rect.colliderect(boss.rect) and boss not in self.objetivos_golpeados:
            boss.vida -= 80
            self.objetivos_golpeados.append(boss)
            self.hits += 1

        if self.hits >= 5 or not pantalla.get_rect().contains(self.rect):
            self.kill()

class Pared(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((90, 15, 15)) # Pared muscular
        for _ in range(w*h // 2000):
            rx, ry = random.randint(0, w), random.randint(0, h)
            pygame.draw.circle(self.image, (120, 30, 30), (rx, ry), random.randint(5, 15))
        self.rect = self.image.get_rect(topleft=(x, y))

# ============================================================
# ================== SISTEMAS DEL JUEGO ======================
# ============================================================

def lanzar_rayos():
    if jugador.trofeos >= 5:
        ahora = pygame.time.get_ticks()
        if ahora - jugador.last_shot > 400:
            jugador.last_shot = ahora
            r = Rayo(jugador.rect.centerx, jugador.rect.centery, jugador.direccion)
            todos_sprites.add(r)
    else:
        iniciar_intro("NECESITAS 5 TROFEOS PARA LOS RAYOS")

def drop_item(x, y):
    r = random.random()
    if r < 0.15:
        it = Item(x, y, "VIDA")
        items_grp.add(it); todos_sprites.add(it)
    elif r < 0.30:
        it = Item(x, y, "XP")
        items_grp.add(it); todos_sprites.add(it)

def generar_laberinto(area_num, desde_entrada=True):
    # Limpiar todo excepto el jugador
    for s in todos_sprites:
        if s != jugador:
            s.kill()
    
    paredes_grp.empty()
    puertas_grp.empty()
    enemigos_grp.empty()
    items_grp.empty()
    balas_grp.empty()
    balas_enemigas_grp.empty()

    # Muros exteriores (La cabina)
    muros = [
        Pared(0, 100, ANCHO, 20),           # Techo
        Pared(0, ALTO-20, ANCHO, 20),        # Suelo
        Pared(0, 100, 20, ALTO-100),         # Pared Izquierda
        Pared(ANCHO-20, 100, 20, ALTO-100)   # Pared Derecha
    ]
    
    # Laberinto interno procedimental
    random.seed(area_num * 123)
    if area_num != 9: # En el área 9 no generamos obstáculos internos para evitar bloqueos
        for _ in range(2 + area_num):
            w = random.randint(80, 200)
            h = 30
            x = random.randint(100, ANCHO-w-100)
            y = random.randint(150, ALTO-h-100)
            muros.append(Pared(x, y, w, h))
    
    for m in muros:
        paredes_grp.add(m); todos_sprites.add(m)
        
    # Puerta de ENTRADA (Lado izquierdo)
    puerta_entrada = Puerta(40, ALTO//2 + 50, "ENTRADA")
    puertas_grp.add(puerta_entrada)
    
    # Puerta de SALIDA (Lado derecho)
    puerta_salida = Puerta(ANCHO - 40, ALTO//2 + 50, "SALIDA")
    puertas_grp.add(puerta_salida)

    # Añadir un trofeo garantizado en cada área
    if area_num < 10: # En el área 10 lo suelta el boss
        if area_num == 5:
            # En el área 5, el trofeo está en el centro para ser recogido durante el Boss
            tx, ty = ANCHO//2, ALTO//2 + 150
        else:
            tx = random.randint(200, ANCHO-200)
            ty = random.randint(200, ALTO-100)
        trofeo = Item(tx, ty, "TROFEO")
        items_grp.add(trofeo); todos_sprites.add(trofeo)

    # Posicionar jugador
    if desde_entrada:
        jugador.rect.center = (100, ALTO//2 + 50)
    else:
        jugador.rect.center = (ANCHO - 100, ALTO//2 + 50)
    
    # Asegurarse de que el jugador no quede atrapado en una pared recién generada
    intentos = 0
    while pygame.sprite.spritecollideany(jugador, paredes_grp) and intentos < 50:
        # Empujar hacia el centro de la pantalla si está atrapado
        if jugador.rect.centerx < ANCHO // 2: jugador.rect.x += 5
        else: jugador.rect.x -= 5
        if jugador.rect.centery < ALTO // 2: jugador.rect.y += 5
        else: jugador.rect.y -= 5
        intentos += 1

def avanzar_area():
    if jugador.area_actual < 10:
        reproducir_snd(SND_PUERTA)
        print("Reproduciendo sonido puerta (avanzar)") # Debug
        jugador.area_actual += 1
        generar_laberinto(jugador.area_actual, desde_entrada=True)
        iniciar_intro(f"ÁREA {jugador.area_actual}")
        
        # Diálogos de curiosidades automáticos
        if jugador.area_actual in CURIOSIDADES:
            iniciar_dialogo(CURIOSIDADES[jugador.area_actual])
        
        # Jefes específicos
        if jugador.area_actual == 5 and not jugador.boss5_derrotado:
            estado_juego("BOSS")
            global boss
            boss = Boss("NORMAL")
            todos_sprites.add(boss)
            iniciar_intro("!!! JEFE INTERMEDIO !!!")
        elif jugador.area_actual == 10:
            estado_juego("BOSS")
            boss = Boss("FINAL")
            todos_sprites.add(boss)
            iniciar_intro("!!! JEFE FINAL: EL NÚCLEO !!!")

def retroceder_area():
    if jugador.area_actual > 1:
        reproducir_snd(SND_PUERTA)
        jugador.area_actual -= 1
        generar_laberinto(jugador.area_actual, desde_entrada=False)
        iniciar_intro(f"ÁREA {jugador.area_actual}")
        # Al retroceder, el estado siempre vuelve a PLAYING por si veníamos de un boss
        estado_juego("PLAYING")
        global boss
        if boss: boss.kill(); boss = None

def estado_juego(nuevo_estado):
    global estado
    estado = nuevo_estado

# ============================================================
# ===================== DIÁLOGOS FNF =========================
# ============================================================

dialogos = []
idx_dialogo = 0
mostrando_dialogo = False

CURIOSIDADES = {
    1: ["Profesor Bio: ¿Sabías que el corazón late unas 100,000 veces al día?", "Profesor Bio: ¡Eso es suficiente energía para conducir un camión por 30 kilómetros!"],
    2: ["Profesor Bio: El sistema nervioso transmite señales a más de 400 km/h.", "Profesor Bio: ¡Es más rápido que un coche de Fórmula 1!"],
    3: ["Profesor Bio: Si extendiéramos todos los vasos sanguíneos, darían la vuelta al mundo dos veces.", "Profesor Bio: ¡Son más de 96,000 kilómetros de conductos!"],
    4: ["Profesor Bio: El cerebro humano genera suficiente electricidad para encender una bombilla pequeña.", "Profesor Bio: ¡Es la computadora más potente que existe!"],
    5: ["Profesor Bio: ¡Cuidado! El virus del Área 5 es pequeño pero muy concentrado.", "Profesor Bio: ¡Usa tu espada con precisión!"],
    6: ["Profesor Bio: Los glóbulos rojos tardan solo 20 segundos en recorrer todo el cuerpo.", "Profesor Bio: ¡Es un sistema de transporte ultra eficiente!"],
    7: ["Profesor Bio: Hay más neuronas en tu cerebro que estrellas en la Vía Láctea.", "Profesor Bio: ¡Eres un universo en miniatura!"],
    8: ["Profesor Bio: La aorta, la arteria más grande, tiene casi el diámetro de una manguera de jardín.", "Profesor Bio: ¡Por aquí pasa mucha presión!"],
    9: ["Profesor Bio: El sistema nervioso entérico es como un 'segundo cerebro' en tu estómago.", "Profesor Bio: ¡Por eso sentimos 'mariposas' cuando estamos nerviosos!"],
    10: ["Profesor Bio: ¡Has llegado al Núcleo! El centro de mando del organismo.", "Profesor Bio: ¡Si cae el Núcleo, el sistema entero colapsará!"]
}

def render_texto_ajustado(texto, fuente, color, ancho_max):
    palabras = texto.split(' ')
    lineas = []
    linea_actual = []
    
    for palabra in palabras:
        linea_prueba = ' '.join(linea_actual + [palabra])
        ancho, _ = fuente.size(linea_prueba)
        if ancho <= ancho_max:
            linea_actual.append(palabra)
        else:
            lineas.append(' '.join(linea_actual))
            linea_actual = [palabra]
    lineas.append(' '.join(linea_actual))
    
    surfaces = [fuente.render(linea, True, color) for linea in lineas]
    return surfaces

def iniciar_dialogo(lista):
    global dialogos, idx_dialogo, mostrando_dialogo
    dialogos = lista; idx_dialogo = 0; mostrando_dialogo = True
    reproducir_snd(SND_NIVEL) # Sonido de notificación de diálogo

def draw_dialogo():
    if not mostrando_dialogo: return
    # Caja de diálogo más elegante
    pygame.draw.rect(pantalla, (20, 20, 40), (40, ALTO-180, ANCHO-80, 150), border_radius=15)
    pygame.draw.rect(pantalla, CIAN, (40, ALTO-180, ANCHO-80, 150), 3, border_radius=15)
    
    # Avatares dinámicos según quién hable
    texto_completo = dialogos[idx_dialogo]
    
    if "Profesor Bio:" in texto_completo:
        pantalla.blit(IMG_PROFESOR, (ANCHO-180, ALTO-280))
        pantalla.blit(IMG_PLAYER, (60, ALTO-260)) # Antibody escucha
    elif "El Tumor:" in texto_completo or "El Nucleo:" in texto_completo:
        pantalla.blit(IMG_TUMOR_AVATAR, (ANCHO-180, ALTO-280))
        pantalla.blit(IMG_PLAYER, (60, ALTO-260))
    else:
        # Default o solo Antibody
        pantalla.blit(IMG_PLAYER, (60, ALTO-260))
    
    # Texto con ajuste automático (word wrap)
    ancho_texto = ANCHO - 220 # Espacio para el texto entre márgenes
    lineas_renderizadas = render_texto_ajustado(texto_completo, fuente_std, BLANCO, ancho_texto)
    
    y_offset = ALTO - 150
    for linea in lineas_renderizadas:
        pantalla.blit(linea, (70, y_offset))
        y_offset += 30 # Espaciado entre líneas
        
    pantalla.blit(fuente_peque.render("PRESIONA ESPACIO PARA CONTINUAR", True, AMARILLO), (ANCHO-320, ALTO-60))

intro_txt = ""; intro_timer = 0
def iniciar_intro(t):
    global intro_txt, intro_timer
    intro_txt = t; intro_timer = 120

def draw_intro():
    global intro_timer
    if intro_timer > 0:
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA); s.fill((0, 0, 0, 160)); pantalla.blit(s, (0, 0))
        zoom = 1.0 + (math.sin(intro_timer * 0.15) * 0.25)
        txt = fuente_grande.render(intro_txt, True, AMARILLO)
        txt = pygame.transform.rotozoom(txt, 0, zoom)
        pantalla.blit(txt, txt.get_rect(center=(ANCHO//2, ALTO//2)))
        intro_timer -= 1

# ============================================================
# ========================= UI Y HUD =========================
# ============================================================

def draw_ui():
    pygame.draw.rect(pantalla, GRIS_OSCURO, (0, 0, ANCHO, 100))
    pygame.draw.line(pantalla, CIAN, (0, 100), (ANCHO, 100), 3)
    # Vida (Barra proporcional a vida_max)
    ancho_vida = 250
    pygame.draw.rect(pantalla, ROJO_OSCURO, (25, 20, ancho_vida, 25))
    porcentaje_vida = max(0, jugador.vida / jugador.vida_max)
    pygame.draw.rect(pantalla, ROJO, (25, 20, int(ancho_vida * porcentaje_vida), 25))
    pantalla.blit(fuente_std.render(f"HP: {int(jugador.vida)}/{jugador.vida_max}", True, BLANCO), (35, 20))
    
    # Experiencia (Barra debajo de la vida)
    xp_nec = int(100 * (1.4 ** (jugador.nivel - 1)))
    pygame.draw.rect(pantalla, (50, 50, 50), (25, 50, ancho_vida, 8))
    porcentaje_xp = min(1.0, jugador.xp / xp_nec)
    pygame.draw.rect(pantalla, BLANCO, (25, 50, int(ancho_vida * porcentaje_xp), 8))
    
    # Energía y Escudo
    pygame.draw.rect(pantalla, (120, 120, 0), (25, 70, 180, 15))
    pygame.draw.rect(pantalla, AMARILLO, (25, 70, jugador.energia * 1.8, 15))
    if jugador.escudo_activo:
        pygame.draw.rect(pantalla, (0, 0, 150), (215, 55, 100, 15))
        pygame.draw.rect(pantalla, AZUL, (215, 55, jugador.escudo_energia, 15))
        pantalla.blit(fuente_peque.render("ESCUDO", True, BLANCO), (230, 53))
    # Stats Derecha
    pantalla.blit(fuente_std.render(f"ÁREA: {jugador.area_actual}/10", True, CIAN), (ANCHO-280, 20))
    if jugador.trofeos >= 5:
        pantalla.blit(fuente_std.render(f"RAYOS: {jugador.rayos}", True, AMARILLO), (ANCHO-280, 55))
    pantalla.blit(fuente_std.render(f"TROFEOS: {jugador.trofeos}", True, (255, 215, 0)), (ANCHO-130, 20))
    if jugador.invencible:
        txt = fuente_std.render("!!! INVENCIBLE !!!", True, MAGENTA)
        pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, 60))

def draw_background():
    pantalla.fill((35, 5, 5))
    for i in range(20):
        t = pygame.time.get_ticks() * 0.0008
        x = (i * 180 + math.sin(t + i) * 60) % ANCHO
        y = (i * 140 + math.cos(t * 0.6 + i) * 40) % ALTO
        pygame.draw.circle(pantalla, (55, 10, 10), (int(x), int(y)), 45)
        pygame.draw.circle(pantalla, (75, 20, 20), (int(x)+12, int(y)+12), 22)

# ============================================================
# ===================== INICIALIZACIÓN =======================
# ============================================================

todos_sprites = pygame.sprite.Group()
enemigos_grp = pygame.sprite.Group()
espadas_grp = pygame.sprite.Group()
balas_grp = pygame.sprite.Group()
balas_enemigas_grp = pygame.sprite.Group()
paredes_grp = pygame.sprite.Group()
items_grp = pygame.sprite.Group()
puertas_grp = pygame.sprite.Group()

jugador = Jugador(); todos_sprites.add(jugador); boss = None; estado = "START"
generar_laberinto(1)
iniciar_intro("ANTIBODY: EL COMIENZO")
iniciar_dialogo([
    "Profesor Bio: Antibody, fuiste creado en este laboratorio para una misión vital.",
    "Profesor Bio: El organismo está bajo un ataque viral masivo sin precedentes.",
    "Profesor Bio: Tu historia comenzó como un simple anticuerpo, pero ahora eres nuestra única esperanza.",
    "Profesor Bio: Por eso diseñamos los inhibidores. Cada vez que absorbes uno, tu estructura mejora.",
    "Profesor Bio: Estos inhibidores desbloquean poderes latentes como los rayos y el escudo protector.",
    "Profesor Bio: ¡Ve y limpia estas 10 áreas! Encuentra los trofeos para fortalecerte.",
    "Antibody: Entendido, Profesor. Limpiaré cada cabina del organismo."
])

def reiniciar_area():
    global boss
    # Guardar el área actual antes de resetear
    area_actual = jugador.area_actual
    
    # Restaurar jugador sin perder todo
    jugador.vida = jugador.vida_max
    # No reseteamos trofeos ni nivel para que no sea frustrante
    jugador.invencible = False
    jugador.timer_invencible = 0
    jugador.evolucionado = False
    jugador.image = IMG_PLAYER
    
    # Regenerar el área donde murió
    generar_laberinto(area_actual, desde_entrada=True)
    estado_juego("PLAYING")
    if boss: 
        boss.kill()
        boss = None
    iniciar_intro(f"REINTENTO: ÁREA {area_actual}")

# ============================================================
# ===================== BUCLE PRINCIPAL ======================
# ============================================================

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if estado == "START":
                    estado = "PLAYING"
                if mostrando_dialogo and event.key == pygame.K_SPACE:
                    reproducir_snd(SND_TALK)
                    idx_dialogo += 1
                    if idx_dialogo >= len(dialogos): 
                        mostrando_dialogo = False
                        # Si estábamos en transición a WIN, ahora sí mostramos la pantalla final
                        if estado == "BOSS" and jugador.area_actual == 10 and not boss:
                            estado = "WIN"
                if not mostrando_dialogo and estado in ["PLAYING", "BOSS"]:
                     if event.key == pygame.K_SPACE: jugador.atacar_espada()
                     if event.key == pygame.K_f: jugador.disparar()
                     if event.key == pygame.K_r: lanzar_rayos()
                if estado in ["GAMEOVER", "WIN"]:
                    if event.key == pygame.K_r:
                        if estado == "GAMEOVER":
                            reiniciar_area()
                        else:
                            # Para WIN, sí reiniciamos todo el juego
                            pygame.quit()
                            os.execl(sys.executable, sys.executable, *sys.argv)
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        if not mostrando_dialogo:
            if estado in ["PLAYING", "BOSS"]:
                todos_sprites.update()
                
                # Items (Recolección común para ambos estados)
                hits = pygame.sprite.spritecollide(jugador, items_grp, True)
                for it in hits:
                    if it.tipo == "VIDA": jugador.vida = min(jugador.vida_max, jugador.vida + 30)
                    elif it.tipo == "XP": jugador.xp += 50
                    elif it.tipo == "TROFEO": 
                        jugador.trofeos += 1
                        if jugador.trofeos == 5:
                            iniciar_intro("¡PODER DEL RAYO DESBLOQUEADO (TECLA R)!")

            if estado == "PLAYING":
                if len(enemigos_grp) < 6 + jugador.nivel:
                    e = Enemigo("VIRUS" if random.random() > 0.4 else "BACTERIA")
                    enemigos_grp.add(e); todos_sprites.add(e)
                
                # Lógica de subida de nivel
                xp_necesaria = int(100 * (1.4 ** (jugador.nivel - 1)))
                if jugador.xp >= xp_necesaria:
                    reproducir_snd(SND_NIVEL)
                    jugador.xp = 0
                    jugador.nivel += 1
                    # Aumentar vida máxima y curar un poco
                    jugador.vida_max += 25
                    jugador.vida = min(jugador.vida_max, jugador.vida + 40)
                    iniciar_intro(f"¡NIVEL {jugador.nivel}! HP MAX: {jugador.vida_max}")

                # Colisiones Espada
                for e in enemigos_grp:
                    hits = pygame.sprite.spritecollide(e, espadas_grp, False)
                    if hits:
                        reproducir_snd(SND_GOLPE)
                        e.vida -= 40
                        if e.vida <= 0:
                            reproducir_snd(SND_MUERTE)
                            drop_item(e.rect.centerx, e.rect.centery)
                            e.kill(); jugador.xp += 25

                # Colisiones Balas
                for b in balas_grp:
                    hits = pygame.sprite.spritecollide(b, enemigos_grp, False)
                    for h in hits:
                        h.vida -= 15; b.kill()
                        if h.vida <= 0:
                            drop_item(h.rect.centerx, h.rect.centery)
                            h.kill(); jugador.xp += 20

                # Puerta
                puertas_grp.update()
                hits_puerta = pygame.sprite.spritecollide(jugador, puertas_grp, False)
                for p in hits_puerta:
                    if p.tipo == "SALIDA" and p.visible:
                        avanzar_area()
                        break # Evitar múltiples activaciones en el mismo frame
                    elif p.tipo == "ENTRADA":
                        retroceder_area()
                        break

                if not jugador.invencible:
                    if pygame.sprite.spritecollide(jugador, enemigos_grp, False):
                        if jugador.recibir_dano(10): # Daño base al chocar
                            reproducir_snd(SND_DANO)
                        if jugador.vida <= 0: estado = "GAMEOVER"

            elif estado == "BOSS":
                if boss:
                    # Colisiones Espada con Boss
                    hits = pygame.sprite.spritecollide(boss, espadas_grp, True)
                    for h in hits:
                        boss.vida -= 30
                        if boss.vida <= 300 and not jugador.invencible and boss.tipo == "FINAL":
                            jugador.invencible = True; jugador.timer_invencible = 1200
                            jugador.vida = jugador.vida_max; iniciar_intro("¡ESTADO DE FURIA INVENCIBLE!")

                    # Colisiones Balas con Boss
                    hits = pygame.sprite.spritecollide(boss, balas_grp, True)
                    for h in hits:
                        boss.vida -= 12
                        if boss.vida <= 300 and not jugador.invencible and boss.tipo == "FINAL":
                            jugador.invencible = True; jugador.timer_invencible = 1200
                            jugador.vida = jugador.vida_max; iniciar_intro("¡ESTADO DE FURIA INVENCIBLE!")

                    if boss.vida <= 0:
                        # Soltar trofeo al morir el boss
                        it = Item(boss.rect.centerx, boss.rect.centery, "TROFEO")
                        items_grp.add(it); todos_sprites.add(it)
                        
                        if boss.tipo == "NORMAL":
                            jugador.boss5_derrotado = True
                        
                        boss.kill(); boss = None;
                        
                        if jugador.area_actual == 10: 
                            iniciar_dialogo([
                                "El Tumor: ¡Argh! No... ¿Cómo es posible?",
                                "El Tumor: Antibody... crees que has ganado, pero solo has destruido mi forma física.",
                                "El Tumor: Yo no nací del azar. Fui creado por los restos de cada toxina que este cuerpo ignoró durante años.",
                                "El Tumor: Soy el resultado del descuido y la negligencia... y mientras el portador siga descuidándose, yo volveré.",
                                "El Tumor: No soy el final, Antibody. Soy solo el primer síntoma de algo mucho más grande.",
                                "El Tumor: Disfruta tu victoria... por ahora."
                            ])
                        else:
                            estado = "PLAYING"
                            iniciar_intro("¡JEFE DERROTADO! RECOGE EL TROFEO")

                if not jugador.invencible:
                    # Daño por proyectiles
                    if pygame.sprite.spritecollide(jugador, balas_enemigas_grp, True):
                        if jugador.recibir_dano(15):
                            reproducir_snd(SND_DANO)
                    
                    # Daño por contacto con el Jefe
                    if boss and pygame.sprite.collide_rect(jugador, boss):
                        if jugador.recibir_dano(20):
                            reproducir_snd(SND_DANO)
                        
                    if jugador.vida <= 0: estado = "GAMEOVER"

        # Dibujado
        draw_background()
        if estado == "START":
            pantalla.blit(IMG_INICIO, (0, 0))
            txt = fuente_grande.render("PULSA CUALQUIER TECLA", True, BLANCO)
            pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, ALTO//2 + 150))
        else:
            # Dibujar el jugador manualmente si es necesario o asegurar que esté en todos_sprites
            todos_sprites.draw(pantalla)
            # Dibujar al jugador explícitamente para asegurar visibilidad
            pantalla.blit(jugador.image, jugador.rect)
            
            puertas_grp.update()
            for p in puertas_grp:
                p.draw(pantalla)
            draw_ui()
        
        draw_dialogo(); draw_intro()
        if estado == "GAMEOVER":
            s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA); s.fill((0, 0, 0, 200)); pantalla.blit(s, (0, 0))
            pantalla.blit(fuente_grande.render("MUERTE CELULAR", True, ROJO), (ANCHO//2-200, ALTO//2-60))
            pantalla.blit(fuente_std.render("PRESIONA 'R' PARA REINTENTAR LA CURA", True, BLANCO), (ANCHO//2-180, ALTO//2+40))
        if estado == "WIN":
            s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA); s.fill((0, 0, 0, 230)); pantalla.blit(s, (0, 0))
            
            txt_congrats = fuente_grande.render("¡CONGRATULATIONS!", True, AMARILLO)
            pantalla.blit(txt_congrats, (ANCHO//2 - txt_congrats.get_width()//2, ALTO//2 - 160))
            
            pantalla.blit(fuente_grande.render("¡CUERPO CURADO!", True, VERDE), (ANCHO//2-200, ALTO//2-80))
            
            # Efecto de texto parpadeante para "CONTINUARÁ..."
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                txt_cont = fuente_grande.render("CONTINUARÁ...", True, CIAN)
                pantalla.blit(txt_cont, (ANCHO//2 - txt_cont.get_width()//2, ALTO//2 + 10))
            
            pantalla.blit(fuente_peque.render("PRESIONA 'R' PARA VOLVER AL INICIO", True, BLANCO), (ANCHO//2-160, ALTO//2+120))
            pantalla.blit(fuente_peque.render("PRESIONA 'Q' PARA SALIR DEL JUEGO", True, ROJO), (ANCHO//2-160, ALTO//2+150))
            pantalla.blit(fuente_std.render(f"TROFEOS GANADOS: {jugador.trofeos}", True, BLANCO), (ANCHO//2-130, ALTO//2+80))

        pygame.display.flip(); reloj.tick(60)

except Exception as e:
    print(f"ERROR CRÍTICO EN EL JUEGO: {e}")
    import traceback
    traceback.print_exc()
    pygame.quit()
    input("Presiona Enter para cerrar...")
