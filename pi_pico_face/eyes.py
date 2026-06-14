from machine import Pin
import neopixel
import time
import random
import math

# -------------------------------------------------
# Hardware
# -------------------------------------------------
WIDTH = 16
HEIGHT = 10
NUM_LEDS = WIDTH * HEIGHT

LEFT_PIN = 6
RIGHT_PIN = 7   # ggf. 22, je nach Jumper/Lötpad

BRIGHTNESS = 0.10

WS_TIMING = (350, 900, 800, 450)

left_eye = neopixel.NeoPixel(Pin(LEFT_PIN), NUM_LEDS, timing=WS_TIMING)
right_eye = neopixel.NeoPixel(Pin(RIGHT_PIN), NUM_LEDS, timing=WS_TIMING)

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

def clear(np_obj):
    for i in range(NUM_LEDS):
        np_obj[i] = (0, 0, 0)

def set_pixel(np_obj, x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        np_obj[xy_to_i(x, y)] = scale(color)

def write_both():
    left_eye.write()
    time.sleep_us(300)
    right_eye.write()
    time.sleep_us(300)

# -------------------------------------------------
# Auge zeichnen
# -------------------------------------------------
def draw_eye(np_obj, pupil_x=0.0, pupil_y=0.0, open_amount=1.0):
    clear(np_obj)

    cx = 7.5 + pupil_x
    cy = 4.5 + pupil_y

    rx = max(7.1 * open_amount, 0.25)
    ry = 4.1

    if open_amount < 0.12:
        for y in range(1, 9):
            set_pixel(np_obj, 7, y, (0, 90, 150))
            set_pixel(np_obj, 8, y, (0, 45, 90))
        return

    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = (x - 7.5) / rx
            dy = (y - 4.5) / ry
            d = dx * dx + dy * dy

            if d <= 1.0:
                if d > 0.78:
                    set_pixel(np_obj, x, y, (0, 35, 90))
                else:
                    glow = int(170 - d * 70)
                    set_pixel(np_obj, x, y, (0, glow, 255))

    # Iris
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = x - cx
            dy = y - cy
            dist = (dx * dx + dy * dy) ** 0.5

            if dist <= 2.1:
                set_pixel(np_obj, x, y, (0, 120, 220))

    # Pupille: immer 2x2 Pixel
    px0 = int(round(cx - 0.5))
    py0 = int(round(cy - 0.5))

    for py in range(py0, py0 + 2):
        for px in range(px0, px0 + 2):
            set_pixel(np_obj, px, py, (0, 0, 18))

# -------------------------------------------------
# Rendering
# -------------------------------------------------
def render(pupil_x=0.0, pupil_y=0.0, open_amount=1.0):
    draw_eye(left_eye, pupil_x, pupil_y, open_amount)
    draw_eye(right_eye, pupil_x, pupil_y, open_amount)
    write_both()

# -------------------------------------------------
# Animationen
# -------------------------------------------------
def smooth_look(start_x, start_y, end_x, end_y, steps=12):
    for i in range(steps + 1):
        t = i / steps
        s = t * t * (3 - 2 * t)

        x = start_x + (end_x - start_x) * s
        y = start_y + (end_y - start_y) * s

        render(x, y, 1.0)
        time.sleep(0.035)

def blink(current_x=0.0, current_y=0.0):
    for a in [1.0, 0.75, 0.45, 0.22, 0.08]:
        render(current_x, current_y, a)
        time.sleep(0.025)

    time.sleep(0.06)

    for a in [0.18, 0.42, 0.72, 1.0]:
        render(current_x, current_y, a)
        time.sleep(0.03)

def double_blink(current_x=0.0, current_y=0.0):
    blink(current_x, current_y)
    time.sleep(0.12)
    blink(current_x, current_y)

def focused_scan():
    open_amount = 0.32

    sequence = [-2, -1, 0, 1, 2, 1, 0, -1, -2, -1, 0]

    for y_pos in sequence:
        render(0, y_pos, open_amount)
        time.sleep(0.045)

    for a in [0.45, 0.6, 0.8, 1.0]:
        render(0, 0, a)
        time.sleep(0.035)

# -------------------------------------------------
# Hauptprogramm
# -------------------------------------------------
current_x = 0.0
current_y = 0.0

render(current_x, current_y)

while True:
    r = random.random()

    if r < 0.35:
        new_x = random.choice([0, 0, 0])
        new_y = random.choice([-2, -1, 0, 1, 2])

        smooth_look(current_x, current_y, new_x, new_y)
        current_x = new_x
        current_y = new_y

    elif r < 0.60:
        blink(current_x, current_y)

    elif r < 0.75:
        double_blink(current_x, current_y)

    elif r < 0.90:
        focused_scan()
        current_x = 0
        current_y = 0

    else:
        render(current_x, current_y)

    time.sleep(random.uniform(1.0, 3.0))

