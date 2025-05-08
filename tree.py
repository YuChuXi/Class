import turtle

def draw_flower(t):
    current_color = t.color()
    current_width = t.width()
    
    t.color("pink")
    t.width(1)
    n = 6
    angle = 360 / n
    for _ in range(n):
        t.pd()
        t.circle(15, 60)
        t.left(120)
        t.circle(15, 60)
        t.left(120)
        t.pu()
        t.left(angle)
    
    t.color(*current_color)
    t.width(current_width)
    t.pd()

def draw_branch(branch_len, t):
    current_color = t.color()
    
    if branch_len > 30:
        t.color("brown")
    else:
        t.color("green")
    
    t.width(1)
    
    t.forward(branch_len)
    
    t.right(30)
    draw_tree(branch_len-15, t)
    
    t.left(60)
    draw_tree(branch_len-15, t)
    
    t.right(30)
    t.backward(branch_len)
    
    t.color(*current_color)

def draw_tree(branch_len, t):
    """递归绘制树"""
    if branch_len > 5:
        draw_branch(branch_len, t)
    else:
        draw_flower(t)

screen = turtle.Screen()
screen.bgcolor("white")
t = turtle.Turtle()
t.speed(0)
t.width(3)
t.left(90)
t.up()
t.backward(200)
t.down()

draw_tree(100, t)

screen.update()
t.hideturtle()
turtle.done()
