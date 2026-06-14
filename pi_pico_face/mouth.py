from machine import Pin
import neopixel
import time
import random

# -------------------------------------------------
# Hardware
# -------------------------------------------------
WIDTH = 16
HEIGHT = 10
NUM_LEDS = WIDTH * HEIGHT

MOUTH_PIN = 6      # ggf. anpassen
BRIGHTNESS = 0.10
WS_TIMING = (350, 900, 800, 450)

mouth = neopixel.NeoPixel(Pin(MOUTH_PIN), NUM_LEDS, timing=WS_TIMING)

# -------------------------------------------------
# Hilfsfunktionen
# -------------------------------------------------
def scale(color):
    return (
        int(color[0] * BRIGHTNESS),
        int(color[1] * BRIGHTNESS),
        int(color[2] * BRIGHTNESS)
    )

def xy_to_i(x, y):
    return y * WIDTH + x

def clear():
    for i in range(NUM_LEDS):
        mouth[i] = (0, 0, 0)

def set_pixel(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        mouth[xy_to_i(x, y)] = scale(color)

def show():
    mouth.write()
    time.sleep_us(300)

# -------------------------------------------------
# Farben
# -------------------------------------------------
BLUE = (0, 120, 255)

# -------------------------------------------------
# Mund zeichnen
# -------------------------------------------------
def draw_mouth(left_lift=0, right_lift=0):
    clear()

    base_y = 5

    # mittlere Grundlinie
    for x in range(4, 12):
        set_pixel(x, base_y, BLUE)

    # linkes Ende
    set_pixel(2, base_y - left_lift, BLUE)
    set_pixel(3, base_y - left_lift, BLUE)

    # rechtes Ende
    set_pixel(12, base_y - right_lift, BLUE)
    set_pixel(13, base_y - right_lift, BLUE)

    show()

# -------------------------------------------------
# Animationen
# -------------------------------------------------
def neutral():
    draw_mouth(0, 0)

def soft_smile():
    clear()

    points = [
        (2, 3), (3, 4),
        (4, 5), (5, 5),
        (6, 5), (7, 5),
        (8, 5), (9, 5),
        (10, 5), (11, 5),
        (12, 4), (13, 3)
    ]

    for x, y in points:
        set_pixel(x, y, BLUE)

    show()

def surprised():
    clear()

    points = [
        # obere Kante
        (7, 2), (8, 2),

        # obere Rundung
        (6, 3), (9, 3),

        # Mitte links/rechts verbreitern
        (5, 4), (6, 4), (9, 4), (10, 4),
        (5, 5), (6, 5), (9, 5), (10, 5),

        # untere Rundung
        (6, 6), (9, 6),

        # untere Kante
        (7, 7), (8, 7)
    ]

    for x, y in points:
        set_pixel(x, y, BLUE)

    show()

def random_expression():
    expression = random.choice([
        neutral,
        neutral,
        neutral,
        soft_smile,
        neutral,
        surprised
    ])

    expression()

# -------------------------------------------------
# Start
# -------------------------------------------------
neutral()

while True:
    random_expression()
    time.sleep(random.uniform(0.8, 2.2))