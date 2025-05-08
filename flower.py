import turtle

screen = turtle.Screen()
screen.bgcolor("white")
pen = turtle.Turtle()
pen.speed(0)
pen.color("red")
pen.width(3)

n = int(input())
angle = 360 / n

for _ in range(n):
    pen.circle(200, 60)
    pen.left(120)
    pen.circle(200, 60)
    pen.left(120)

    pen.left(angle)

pen.hideturtle()
turtle.done()
