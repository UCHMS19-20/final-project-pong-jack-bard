import pygame
import random
import sys

pygame.init()

# Creates clock to track time
clock = pygame.time.Clock()

# Defining colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255,255,0)

# Defining variables
radius = 10
radius2 = 20 
thickness = 10
paddle_length = 100
score1 = 0
score2 = 0
maxnum = 100

# Setting the height and width of the screen
screen_width = 800
screen_height = 600
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PONG")

def screen_setup():
   """ Create background screen that will remain unchanged"""
   screen.fill(BLACK)
  
   # Draws white border
   pygame.draw.rect(screen, WHITE, [0, 0, screen_width - 1, 599], 2)
   pygame.draw.line(screen, WHITE, [0, 100], [screen_width, 100], 2)
   pygame.draw.line(screen, WHITE, [200, 0], [200, 100], 2)
   pygame.draw.line(screen, WHITE, [600, 0], [600, 100], 2)
   
   # Displays name of the game, score, and controls at top of the screen
   font = pygame.font.SysFont('Calibri', 40, True, False)
   text = font.render("PONG", True, WHITE)
   screen.blit(text, [50, 35])
   text = font.render(str(score1), True, WHITE)
   screen.blit(text, [300, 35])
   text = font.render(str(score2), True, WHITE)
   screen.blit(text, [500, 35])
   font = pygame.font.SysFont('Calibri', 15, True, False)
   text = font.render("Player 1: w and s", True, WHITE)
   screen.blit(text, [620, 30])
   text = font.render("Player 2: up and down", True, WHITE)
   screen.blit(text, [620, 60])
   
   return

class Ball:
   """ Class to keep track of a ball's location and velocity vector."""
   def __init__(self):
       self.x = 0
       self.y = 0
       self.dx = 0
       self.dy = 0

def make_ball(n):
    """Sets velocity of the ball and makes a new ball at a position based on the last player to score."""
    ball = Ball()

    # Determines the angle the ball starts with
    dir_x = random.randrange(50,100)/100
    dir_y = (1 - dir_x**2)**0.5
    # Constant determining the speed of the ball
    vel_x = 5
    vel_y = 5
    # Randomizes the direction of the y component of the ball
    flip_y = 1 - 2*random.randint(0,1)

    # Creates ball in the center of the screen at start of game
    if n == 0:
        flip_x = 1 - 2*random.randint(0,1)
        ball.x = screen_width/2
        ball.y = screen_height/2
    # If player 1 scores, the ball is created at player 1's paddle and is given a positive x velocity
    elif n==1:
        flip_x = 1
        ball.x = 30 + thickness + radius
        ball.y = paddle1.y
    # If player 2 scores, the ball is created at player 2's paddle and is given a negative x velocity
    else:
        flip_x = -1
        ball.x = screen_width - 30 - thickness - radius
        ball.y = paddle2.y        
           
    # Equation for the velocity vector of the ball
    ball.dx = dir_x * vel_x * flip_x
    ball.dy = dir_y * vel_y * flip_y
   
    return ball

class Paddle:
   """Class used to keep track of a Paddle's location and vector."""
   def __init__(self, name, x, y, dy):
       self.name = name
       self.x = x
       self.y = y
       self.dy = dy

# Assigns values to the position and velocity of each paddle
paddle1 = Paddle("paddle1", 30, 350, 10)
paddle2 = Paddle("paddle2", 770, 350, 10)

class Powerup:
   """"Class used to control position of powerups."""
   def __init__(self):
       self.x = 0
       self.y = 0

def make_powerup():
   """"Determines a random location for the powerup."""
   powerup = Powerup()
   powerup.x = random.randint(200, screen_width - 200)
   powerup.y = random.randint(150, screen_height - 50)
  
   return powerup


def wingame():
    """Checks to see if either player has won the game and displays which player won."""

    font = pygame.font.SysFont('Calibri', 80, True, False)

    if score1 == 5:
        # Creates a black screen displaying "Player 1 Wins" and briefly pauses the game 
        text = font.render("Player 1 Wins!", True, WHITE)
        screen.fill(BLACK)
        screen.blit(text, [160, 250])
        pygame.display.flip()
        pygame.time.delay (2500)
        pygame.quit()

    elif score2 == 5:
        # Creates a black screen displaying "Player 2 Wins" and briefly pauses the game     
        text = font.render("Player 2 Wins!", True, WHITE)
        screen.fill(BLACK)
        screen.blit(text, [160, 250])
        pygame.display.flip()
        pygame.time.delay (2500)
        pygame.quit()
  
    return

# Creates the background
screen_setup()
# Creates the ball in the center of the play area
ball = make_ball(0)

# Used to determine when a powerup can be created
powerup_on = False
# Used to create only one powerup at a time
switch = True

# Holding down a key will create an event every 10 milliseconds
pygame.key.set_repeat(10)

# Main loop
while True:

   # Sets fps to 60
   clock.tick(60)

   # Allows user's key inputs to move paddles 
   for event in pygame.event.get():
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_UP:
               paddle2.y -= paddle2.dy
           if event.key == pygame.K_DOWN:
               paddle2.y += paddle2.dy
           if event.key == pygame.K_w:
               paddle1.y -= paddle1.dy
           if event.key == pygame.K_s:
               paddle1.y += paddle1.dy
  
   # Changes the balls position every frame
   ball.x += ball.dx
   ball.y += ball.dy
  
   # Bounces the ball off the top or bottom border if there is a collision
   if ball.y >= screen_height - radius or ball.y <= 2*radius + 100:
       ball.dy *= -1

   # Increases a player's score when the ball passes by the other player's paddle
   if ball.x > screen_width - thickness/2 - 30:
       score1 += 1
       paddle_length = 100
       # Makes a new ball at Player 1's paddle
       ball = make_ball(1)
   if ball.x < 30 + thickness/2:
       score2 += 1
       paddle_length = 100
       # Makes a new ball at Player 2's paddle
       ball = make_ball(2)
      
   # Bounces the ball off the paddles with an increased velocity   
   if ball.x >= paddle2.x - thickness/2 - radius and ball.y < paddle2.y + paddle_length/2 and ball.y > paddle2.y - paddle_length/2:
       ball.dx *= -1.1
       ball.dy *= 1.1
   if ball.x <= paddle1.x + thickness/2 + radius and ball.y < paddle1.y + paddle_length/2 and ball.y > paddle1.y - paddle_length/2:
       ball.dx *= -1.1
       ball.dy *= 1.1
    
    # Keeps paddles in the game area
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

   # Draws the ball and both paddles
   pygame.draw.circle(screen, WHITE, [int(ball.x), int(ball.y)], radius)
   pygame.draw.line(screen, WHITE, [paddle1.x, paddle1.y - paddle_length/2], [paddle1.x, paddle1.y + paddle_length/2], thickness)
   pygame.draw.line(screen, WHITE, [paddle2.x, paddle2.y - paddle_length/2], [paddle2.x, paddle2.y + paddle_length/2], thickness)
   
   # Determines chance of a powerup will be created
   if powerup_on == False and random.randint(0, maxnum) == 0:
        # Randomly chooses 1 out of the 3 possible powerups to be created
        choice = random.randint (0,2)
        powerup = make_powerup()
        powerup_on = True

   if  powerup_on == True and switch == True:
        if choice == 0:
            switch == False
            # Draws powerup 1
            pygame.draw.circle(screen, BLUE, [int(powerup.x), int(powerup.y)], radius2)
            # If the ball collides with powerup 1, the velocity vector doubles          
            if ball.x + radius + radius2 > powerup.x and ball.x - radius - radius2 < powerup.x and ball.y + radius + radius2 > powerup.y and ball.y - radius - radius2 < powerup.y:
                ball.dx *= 2
                ball.dy *= 2
                # Removes the powerup and allows another pwoerup to be created
                powerup_on = False
                switch == True
        elif choice == 1:
            switch == False
            # Draws powerup 2
            pygame.draw.circle(screen, RED, [int(powerup.x), int(powerup.y)], radius2)
            # If the ball collides with powerup 2, the x velocity doubles and goes in opposite direction
            if ball.x + radius + radius2 > powerup.x and ball.x - radius - radius2 < powerup.x and ball.y + radius + radius2 > powerup.y and ball.y - radius - radius2 < powerup.y:
                ball.dx *= -2
                # Removes the powerup and allows another pwoerup to be created
                powerup_on = False
                switch == True
        elif choice == 2:
            switch == False
            # Draws powerup 3
            pygame.draw.circle(screen, YELLOW, [int(powerup.x), int(powerup.y)], radius2)
           # If the ball collides with powerup 3, the paddle length is cut in half
            if ball.x + radius + radius2 > powerup.x and ball.x - radius - radius2 < powerup.x and ball.y + radius + radius2 > powerup.y and ball.y - radius - radius2 < powerup.y:
                paddle_length = paddle_length/2
                # Removes the powerup and allows another pwoerup to be created               
                powerup_on = False
                switch == True
  

   # Updates screen
   pygame.display.flip()

   # Checks to see if either player has won the game
   wingame()