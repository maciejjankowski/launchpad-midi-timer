import sys

import launchpad_py as launchpad

import random
from datetime import datetime
import time

# https://en.wikipedia.org/wiki/Hilbert_curve

BLACK = (0, 0)
RED = (3, 0)
GREEN = (0, 3)
YELLOW = (3, 3)

def calc_pixels(frac):
    pixels = [[0 for _ in range(8)] for _ in range(8)]
    n = int(frac * 64)
    k = int((frac * 64 - n) * n)
    if n >= 64:
        k = 64

    for x in range(8):
        for y in range(8):
            d = xy2d(64, x, y)
            if d <= k:
                color = YELLOW
            elif d == n:
                color = RED
            elif d < n:
                color = GREEN
            else:
                color = BLACK

            pixels[x][y] = color

    return pixels


def xy2d(n, x, y):
    d = 0
    s = n // 2
    while s > 0:
        rx = (x & s) > 0
        ry = (y & s) > 0
        d += s * s * ((3 * rx) ^ ry)
        x, y = rot(s, x, y, rx, ry)
        s //= 2
    return d


def d2xy(n, d):
    x = y = 0
    t = d
    s = 1
    while s < n:
        rx = 1 & (t // 2)
        ry = 1 & (t ^ rx)
        x, y = rot(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        t //= 4
        s *= 2

    return x, y


def rot(n, x, y, rx, ry):
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        x, y = y, x
    return x, y


def clear(lp):
    for x in range(9):
        for y in range(9):
            lp.LedCtrlXY( x, y, 0, 0)


def display(lp, frac):
    pixels = calc_pixels(frac)
    for x in range(8):
        for y in range(8):
            red, green = pixels[x][y]
            lp.LedCtrlXY( x, y+1, red, green)


def main():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} 12:00 13:00')
        exit()

    h1, m1 = sys.argv[1].split(':')
    h2, m2 = sys.argv[2].split(':')

    dt1 = datetime.now().replace(hour=int(h1), minute=int(m1), second=0, microsecond=0)
    dt2 = datetime.now().replace(hour=int(h2), minute=int(m2), second=0, microsecond=0)

    lp = launchpad.Launchpad()
    if not lp.Open():
        print('Error open()')
        exit(1)

    clear(lp)

    interval = dt2.timestamp() - dt1.timestamp()

    try:
        while True:
            now = datetime.now().timestamp()
            seconds = now - dt1.timestamp()
            frac = seconds / interval
            clamped = max(0, min(1, frac))
            print(' ' * 78 + '\r', end='')
            print(f'elapsed: {seconds:.0f} / {interval:.0f} seconds ({frac*64:.2f} / 64)\r', end='')
            sys.stdout.flush()
            display(lp, clamped)
            time.sleep(0.02)
    except KeyboardInterrupt:
        clear(lp)
        print()


if __name__ == '__main__':
	main()
