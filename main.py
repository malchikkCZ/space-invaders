from turtle import Screen, Turtle
import random
import time

# screen definition
wn = Screen()
wn.setup(600, 800)
wn.bgcolor("black")
wn.title("Space Invaders")
wn.tracer(0)


class Rocket(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.color("white")
        self.shape("square")
        self.shapesize(stretch_len=2, stretch_wid=1)
        self.goto(0, -350)
        self.bullet = None
        self.bullet_speed = 10
    
    def move_left(self):
        x = self.xcor() - 10
        if x <= -270:
            x = -270
        self.setx(x)

    def move_right(self):
        x = self.xcor() + 10
        if x >= 270:
            x = 270
        self.setx(x)
    
    def fire(self):
        if self.bullet is None:
            self.bullet = Bullet(self.xcor(), self.ycor(), self.bullet_speed)


class Bullet(Turtle):
    def __init__(self, x, y, direction):
        super().__init__()
        self.color("white")
        self.shape("square")
        self.penup()
        self.shapesize(stretch_len=0.2)
        self.goto(x, y)
        self.direction = direction
        
    def move(self):
        self.sety(self.ycor() + self.direction)

    def hit(self, targets):
        for row in targets:
            for target in row:
                if (self.ycor() > target.ycor() - 20 and self.ycor() < target.ycor() + 20) and (self.xcor() > target.xcor() - 20 and self.xcor() < target.xcor() + 20):
                    target.sety(9999)
                    self.sety(9999)
                    return True
        return False


class Alien(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.color("white")
        self.shape("square")
        self.penup()
        self.shapesize(stretch_len=2, stretch_wid=2)
        self.goto(x, y)
        self.bullet = None
    
    def move(self, speed):
        self.setx(self.xcor() + speed)
        if random.randint(0,9999) == 42:
            self.fire(speed)
    
    def fire(self, speed):
        if self.bullet is None:
            self.bullet = Bullet(self.xcor(), self.ycor(), abs(speed) * -1)

    def descend(self, speed):
        self.sety(self.ycor() - speed)

    def landed(self):
        if self.ycor() <= -300:
            return True
        return False
    
        
def cleared(aliens):
    for row in aliens:
        for alien in row:
            if alien.ycor() < 400:
                return False
    return True


rocket = Rocket()

aliens = [[Alien(x, y) for x in range(-230, 230, 50)] for y in range(350, 100, -50)]
alies = [[rocket]]

speed = 1
descend = False

wn.listen()
wn.onkey(rocket.move_left, "Left")
wn.onkey(rocket.move_right, "Right")
wn.onkey(rocket.fire, "space")

game = True
while game:
    time.sleep(1/30)

    if rocket.bullet is not None and rocket.bullet.ycor() < 450:
        if rocket.bullet.hit(aliens):
            speed *= 1.03
            print(speed)
        else:
            rocket.bullet.move()
    else:
        rocket.bullet = None

    for row in aliens:
        for alien in row:
            alien.move(speed)

            if alien.bullet is not None and alien.bullet.ycor() > -450:
                if alien.bullet.hit(alies):
                    print("Game over")
                    game = False
                else:
                    alien.bullet.move()
            else:
                alien.bullet = None

            if not descend and (alien.xcor() < -250 or alien.xcor() > 250):
                descend = True    

    if descend:
        speed *= -1
        for row in aliens:
            for alien in row:
                alien.descend(abs(speed * 5))
                if alien.landed():
                    print("Game over")
                    game = False
        descend = False
    
    if cleared(aliens):
        print("You win!")
        game = False
  
    wn.update()


wn.exitonclick()
