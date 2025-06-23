import pygame
import numpy as np
import random

# Constants
WIDTH, HEIGHT = 1000, 600
BAR_COUNT = 100
FPS = 144
SAMPLE_RATE = 44100

# Setup
pygame.init()
pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, 512)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🔒 JD Slope Sorter")
clock = pygame.time.Clock()

# Sound
def generate_smooth_tone(freq, duration=0.07):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = 0.3 * np.sin(2 * np.pi * freq * t) * np.exp(-4 * t)
    audio = (wave * 32767).astype(np.int16)
    stereo = np.stack((audio, audio), axis=-1)
    return pygame.sndarray.make_sound(stereo)

# Color gradient
def get_color_gradient(i, total):
    r = int(100 + 155 * (i / total))
    g = int(100 + 80 * ((total - i) / total))
    b = 220
    return (r, g, b)

# Bars
class Bar:
    def __init__(self, value, index, total):
        self.value = value
        self.index = index
        self.total = total
        self.width = WIDTH // total
        self.color = get_color_gradient(index, total)

    def draw(self, surface):
        x = self.index * self.width
        height = int(self.value * HEIGHT)
        y = HEIGHT - height

        glow = pygame.Surface((self.width, height), pygame.SRCALPHA)
        glow.fill((*self.color, 80))
        surface.blit(glow, (x, y))
        pygame.draw.rect(surface, self.color, (x, y, self.width - 1, height))

    def play_note(self):
        freq = 180 + self.value * 1000
        tone = generate_smooth_tone(freq)
        tone.play()

# Create data
values = [i / BAR_COUNT for i in range(BAR_COUNT)]
random.shuffle(values)
bars = [Bar(values[i], i, BAR_COUNT) for i in range(BAR_COUNT)]

# Sort
def instant_sort(bars):
    n = len(bars)
    for i in range(n):
        for j in range(n - i - 1):
            yield
            if bars[j].value > bars[j + 1].value:
                bars[j], bars[j + 1] = bars[j + 1], bars[j]
                bars[j].index, bars[j + 1].index = j, j + 1
                bars[j].play_note()
                yield

sort_gen = instant_sort(bars)
sorting = True
running = True

# Fonts
font_corner = pygame.font.SysFont("Arial", 18, bold=True)
font_overlay = pygame.font.SysFont("Arial", 60, bold=True)

# Main loop
while running:
    clock.tick(FPS)
    screen.fill((15, 10, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if sorting:
        try:
            next(sort_gen)
        except StopIteration:
            sorting = False

    for i, bar in enumerate(bars):
        bar.index = i
        bar.draw(screen)

    # 🔒 Uncroppable Watermark
    overlay = font_overlay.render("@JD  //  Dopamine Sort", True, (255, 255, 255))
    overlay.set_alpha(25)  # transparency
    overlay_rect = overlay.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(overlay, overlay_rect)

    # Corner tag too
    watermark = font_corner.render("@JD  //  Dopamine Sort", True, (200, 200, 255))
    screen.blit(watermark, (10, HEIGHT - 30))

    pygame.display.flip()

pygame.quit()
