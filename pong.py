"""
Jack Bard
"""

import pygame
import random
import sys
import math

pygame.init()
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255,255,0)

radius = 10
radius2 = 20 
thickness = 10
paddle_length = 100
score1 = 0
score2 = 0
maxnum = 100

# Set the height and width of the screen
screen_width = 800
screen_height = 600
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PONG")

def screen_setup():
   """ Create background screen """
   screen.fill(BLACK)
  
   pygame.draw.rect(screen, WHITE, [0, 0, screen_width - 1, 599], 2)
   pygame.draw.line(screen, WHITE, [0, 100], [screen_width, 100], 2)
   pygame.draw.line(screen, WHITE, [200, 0], [200, 100], 2)
   pygame.draw.line(screen, WHITE, [600, 0], [600, 100], 2)
   font = pygame.font.SysFont('Calibri', 40, True, False)
   text = font.render("PONG", True, WHITE)
   screen.blit(text, [50, 35])
   text = font.render(str(score1), True, WHITE)
   screen.blit(text, [300, 35])
   text = font.render(str(score2), True, WHITE)
   screen.blit(text, [500, 35])
   font = pygame.font.SysFont('Calibri', 20, True, False)
   text = font.render("CONTROLS...", True, WHITE)
   screen.blit(text, [650, 35])
   return

winon = True

def wingame():

    font = pygame.font.SysFont('Calibri', 80, True, False)

    if score1 == 3 and winon == True :
        winon == False
        text = font.render("Player 1 Wins!", True, WHITE)
        screen.fill(BLACK)
        screen.blit(text, [160, 250])
        pygame.display.flip()
        pygame.time.delay (2500)
        pygame.quit()
    elif score2 == 3 and winon == True :
        winon == False
        text = font.render("Player 2 Wins!", True, WHITE)
        screen.fill(BLACK)
        screen.blit(text, [160, 250])
        pygame.display.flip()
        pygame.time.delay (2500)
        pygame.quit()
  
    return
  
class Ball:
   """ Class to keep track of a ball's location and vector """
   def __init__(self):
       self.x = 0
       self.y = 0
       self.dx = 0
       self.dy = 0

def make_ball(n):
    """ Function to make a new, random ball """
    ball = Ball()
    dir_x = random.randrange(50,100)/100
    dir_y = (1 - dir_x**2)**0.5
    vel_x = 5
    vel_y = 5
    flip_y = 1 - 2*random.randint(0,1)

    if n == 0:
        flip_x = 1 - 2*random.randint(0,1)
        ball.x = screen_width/2
        ball.y = screen_height/2
    elif n==1:
        flip_x = 1
        ball.x = 30 + thickness + radius
        ball.y = paddle1.y
    else:
        flip_x = -1
        ball.x = screen_width - 30 - thickness - radius
        ball.y = paddle2.y        
           
    ball.dx = dir_x * vel_x * flip_x
    ball.dy = dir_y * vel_y * flip_y
   
    return ball

class Paddle:
   """ Class to keep track of a Paddle's location and vector """
   def __init__(self, name, x, y, dy):
       self.name = name
       self.x = x
       self.y = y
       self.dy = dy

paddle1 = Paddle("paddle1", 30, 350, thickness)
paddle2 = Paddle("paddle2", 770, 350, thickness)

class Powerup:
   def __init__(self):
       self.x = 0
       self.y = 0

def make_powerup():
   powerup = Powerup()
   powerup.x = random.randint(200, screen_width - 200)
   powerup.y = random.randint(150, screen_height - 50)
  
   return powerup

done = False

screen_setup()
ball = make_ball(0)

powerup_on = False
switch = True

pygame.key.set_repeat(10)

# Main program loop
while not done:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           done = True
       elif event.type == pygame.KEYDOWN:
           if event.key == pygame.K_UP:
               paddle2.y -= paddle2.dy
           if event.key == pygame.K_DOWN:
               paddle2.y += paddle2.dy
           if event.key == pygame.K_w:
               paddle1.y -= paddle1.dy
           if event.key == pygame.K_s:
               paddle1.y += paddle1.dy
  
   # Move the ball's center
   ball.x += ball.dx
   ball.y += ball.dy
  
   # Bounces the ball if needed
   if ball.y >= screen_height - radius or ball.y <= 2*radius + 100:
       ball.dy *= -1
   if ball.x > screen_width - thickness/2 - 30:
       score1 += 1
       paddle_length = 100
       ball = make_ball(1)
   if ball.x < 30 + thickness/2:
       score2 += 1
       paddle_length = 100
       ball = make_ball(2)
      
   if ball.x >= paddle2.x - thickness/2 - radius and ball.y < paddle2.y + paddle_length/2 and ball.y > paddle2.y - paddle_length/2:
       ball.dx *= -1.1
       ball.dy *= 1.1
   if ball.x <= paddle1.x + thickness/2 + radius and ball.y < paddle1.y + paddle_length/2 and ball.y > paddle1.y - paddle_length/2:
       ball.dx *= -1.1
       ball.dy *= 1.1
    
    #Keep paddles in the game areasss
   if paddle1.y > screen_height - paddle_length/2:
       paddle1.y = screen_height - paddle_length/2
   if paddle1.y < 100 + paddle_length/2:
       paddle1.y = 100 + paddle_length/2
   if paddle2.y > screen_height - paddle_length/2:
       paddle2.y = screen_height - paddle_length/2
   if paddle2.y < 100 + paddle_length/2:
       paddle2.y = 100 + paddle_length/2
  
   # Sets the screen background
   screen_setup()

   pygame.draw.circle(screen, WHITE, [int(ball.x), int(ball.y)], radius)
   pygame.draw.line(screen, WHITE, [paddle1.x, paddle1.y - paddle_length/2], [paddle1.x, paddle1.y + paddle_length/2], thickness)
   pygame.draw.line(screen, WHITE, [paddle2.x, paddle2.y - paddle_length/2], [paddle2.x, paddle2.y + paddle_length/2], thickness)
   
   if powerup_on == False and random.randint(0, maxnum) == 0:
        choice = random.randint (0,2)
        powerup = make_powerup()
        powerup_on = True

   if  powerup_on == True and switch == True:
        if choice == 0:
            switch == False
            pygame.draw.circle(screen, BLUE, [int(powerup.x), int(powerup.y)], radius2)
            if ball.x + radius + radius2 > powerup.x and ball.x - radius - radius2 < powerup.x and ball.y + radius + radius2 > powerup.y and ball.y - radius - radius2 < powerup.y:
                ball.dx *= 2
                ball.dy *= 2
                powerup_on = False
                switch == True
        elif choice == 1:
            switch == False
            pygame.draw.circle(screen, RED, [int(powerup.x), int(powerup.y)], radius2)
            if ball.x + radius + radius2 > powerup.x and ball.x - radius - radius2 < powerup.x and ball.y + radius + radius2 > powerup.y and ball.y - radius - radius2 < powerup.y:
                ball.dx *= -2
                powerup_on = False
                switch == True
        elif choice == 2:
            switch == False
            pygame.draw.circle(screen, YELLOW, [int(powerup.x), int(powerup.y)], radius2)
            if ball.x + radius + radius2 > powerup.x and ball.x - radius - radius2 < powerup.x and ball.y + radius + radius2 > powerup.y and ball.y - radius - radius2 < powerup.y:
                paddle_length = paddle_length/2
                powerup_on = False
                switch == True


  
   # Sets fps to 60
   clock.tick(60)

   pygame.display.flip()
   wingame()
 
 
pygame.quit()
