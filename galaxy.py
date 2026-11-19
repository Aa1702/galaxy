
import turtle
import colorsys
import math
import random

random.seed(7)

INCLINATION = math.radians(65)
ROTATION = math.radians(25)

screen = turtle.Screen()
screen.setup(780, 480)
screen.bgcolor("#03030b")
screen.colormode(1.0)
screen.tracer(0)

BATCH_SIZE = 8
DELAY = 20

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.penup()


def glow(h, v=1.0):
    return colorsys.hsv_to_rgb(h % 1, 0.7, v)


def project(x, y):
    y *= math.cos(INCLINATION)

    c = math.cos(ROTATION)
    s = math.sin(ROTATION)

    return x * c - y * s, x * s + y * c


def stars():
    for _ in range(140):
        x = random.randint(-385, 385)
        y = random.randint(-235, 235)
        size = random.randint(1, 3)

        yield x, y, size, "white"


def dust():
    for _ in range(700):
        r = random.gauss(0, 120)
        a = random.uniform(0, 6.283)

        x = r * math.cos(a)
        y = r * math.sin(a)

        size = random.randint(2, 4)
        px, py = project(x, y)
        color = glow(0.7, 0.3)

        yield px, py, size, color


def arms(count):
    for i in range(count):
        for k in range(4):
            d = i / count
            a = k * math.pi / 2 + d * 10
            r = 10 + d * 290
            s = 2 + d * 10

            x = r * math.cos(a) + random.gauss(0, s)
            y = r * math.sin(a) + random.gauss(0, s)

            hue = 0.13 - d * 0.55
            v = random.uniform(0.6, 1)
            size = random.randint(2, 4)

            px, py = project(x, y)
            color = glow(hue, v)

            yield px, py, size, color


def core():
    for _ in range(260):
        r = random.gauss(0, 26)
        a = random.uniform(0, 6.283)

        x = r * math.cos(a)
        y = r * math.sin(a)

        size = random.randint(2, 5)
        px, py = project(x, y)
        color = glow(0, 1.0)

        yield px, py, size, color


def sparkle():
    for _ in range(40):
        r = random.gauss(0, 150)
        a = random.uniform(0, 6.283)

        x = r * math.cos(a)
        y = r * math.sin(a)

        size = random.randint(5, 8)
        px, py = project(x, y)

        yield px, py, size, "white"


def particles():
    yield from stars()
    yield from dust()
    yield from arms(900)
    yield from core()
    yield from sparkle()
    yield 0, 0, 26, "#fff3c4"


def animate():
    for _ in range(BATCH_SIZE):
        try:
            x, y, size, color = next(particles)
        except StopIteration:
            screen.update()
            return

        t.goto(x, y)
        t.dot(size, color)

    screen.update()
    screen.ontimer(animate, DELAY)


particles = iter(particles())

animate()

turtle.done()
