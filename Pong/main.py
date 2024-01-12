import turtle
import winsound


left_player = 0
right_player = 0
wm = turtle.Screen()
wm.title("Pong by Tharv")
wm.bgcolor("black")
wm.setup(width=800, height=600)
wm.tracer(0)

# Bat A

batA = turtle.Turtle()
batA.speed(0)
batA.shape("square")
batA.shapesize(stretch_wid=5, stretch_len=1)
batA.color("red")
batA.penup()
batA.goto(-350, 0)

# Bat B

batB = turtle.Turtle()
batB.speed(0)
batB.shape("square")
batB.shapesize(stretch_wid=5, stretch_len=1)
batB.color("red")
batB.penup()
batB.goto(350, 0)


# Ball

ball = turtle.Turtle()
ball.speed(20)
ball.shape("square")
ball.color("red")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.125
ball.dy = 0.125


# batA movement

def batA_moveup():

    y = batA.ycor()
    y += 20
    batA.sety(y)


def batA_movedn():

    y = batA.ycor()
    y -= 20
    batA.sety(y)

# ball movement


# def ball_movedn():

#     y = ball.ycor()
#     y -= 20
#     ball.sety(y)


# def ball_moveup():

#     y = ball.ycor()
#     y += 20
#     ball.sety(y)


# def ball_movelf():

#     x = ball.xcor()
#     x -= 20
#     ball.setx(x)


# def ball_movert():

#     x = ball.xcor()
#     x += 20
#     ball.setx(x)

# batB movemnet


def batB_moveup():

    y = batB.ycor()
    y += 20
    batB.sety(y)


def batB_movedn():

    y = batB.ycor()
    y -= 20
    batB.sety(y)


# keyboard binding
wm.listen()
wm.onkeypress(batA_moveup, "w")
wm.onkeypress(batA_movedn, "s")
# wm.onkeypress(ball_moveup, "8")
# wm.onkeypress(ball_movedn, "2")
wm.onkeypress(batB_moveup, "Up")
wm.onkeypress(batB_movedn, "Down")
# wm.onkeypress(ball_movelf, "4")
# wm.onkeypress(ball_movert, "6")


def playBatSound():
    winsound.PlaySound('HIT.wav', winsound.SND_ASYNC)


def bgmusic():
    winsound.PlaySound('game-bg.wav', winsound.SND_ASYNC)


def scoreincrease():
    winsound.PlaySound('score-increase.wav', winsound.SND_ASYNC)


# Displaying of the score
sketch_1 = turtle.Turtle()
sketch_1.speed(0)
sketch_1.color("blue")
sketch_1.penup()
sketch_1.hideturtle()
sketch_1.goto(0, 260)
sketch_1.write("Left Player : 0    Right Player: 0",
               align="center", font=("Courier", 24, "normal"))

# mainfun

while True:
    wm.update()

    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # border checking
    if ball.ycor() > 280:
        ball.sety(280)
        ball.dy *= -1

    if ball.ycor() < -280:
        ball.sety(-280)
        ball.dy *= -1

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        left_player += 1
        scoreincrease()
        sketch_1.clear()
        sketch_1.write("left_player : {}    right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        right_player += 1
        scoreincrease()
        sketch_1.clear()
        sketch_1.write("left_player : {}    right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))

    # bat and ball collision

    if (ball.xcor() > 340 and
            ball.xcor() < 350) and (ball.ycor() < batB.ycor() + 40 and ball.ycor() > batB.ycor() - 40):
        ball.setx(330)
        ball.dx *= -0.8
        playBatSound()

    if (ball.xcor() < -340 and
            ball.xcor() > -350) and (ball.ycor() < batA.ycor() + 40 and ball.ycor() > batA.ycor() - 40):
        ball.setx(-330)
        ball.dx *= -0.8
        playBatSound()
