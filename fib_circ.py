import turtle
import random

pen = turtle.Turtle()
step = 1
radius = 100
pen.speed(3)
pen.color("red")
pen.circle(radius)
pen.penup()

x1 = 1
x2 = 1
for n in range(110000):
    pen.goto(x1, x2)  # 57 is to scale the fern and -275 is to start the drawing from the bottom.
    pen.pendown()
    pen.dot()
    pen.penup()
    r = random.random()  # to get probability
    r = r * 360
    x1n = x1
    x2n = x2
    x1 = x2
    x2 = x2 + x1n
