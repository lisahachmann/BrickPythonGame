""" Brick Breaker by Lisa Hachmann and Maggie Jakus, 3/11/15

This game takes user input (the left and right arrow keys) 
to control a paddle. The user uses the paddle to hit a ball to
try to break the bricks at the top of the screen.

"""

import math
import pygame
import random
import time
from pygame import *
if not pygame.font: print 'Warning, fonts disabled'

# defining colors
red = (255,0,0)
green = (0,255,63)
purple = (238,130,238)
black = (0,0,0)
white = (255, 255, 255)
blue = (8, 146, 208)

class Nonmoving_brick(pygame.sprite.Sprite):
	"""Creates dimensions and visual details for the bricks
	that will be hit with a ball and then eliminated"""

	def __init__(self, color, xpos, ypos):
		super(Nonmoving_brick, self).__init__()
		self.width = 77 # brick dimension
		self.height = 30 # brick dimension
		width = self.width
		height = self.height
		self.image = pygame.Surface([width, height])
		self.image.fill((color))	

		self.rect = self.image.get_rect()
		self.screenheight = pygame.display.get_surface().get_height()
		self.screenwidth = pygame.display.get_surface().get_width()

		self.rect.x = xpos # brick position
		self.rect.y = ypos # brick position

class Ball(pygame.sprite.Sprite):
	"""Creates dimensions and visual details for the moving ball"""
	def __init__(self,color):
		super(Ball, self).__init__()

		self.width = 20 # ball dimensions
		self.height = 20 # ball dimensions
		width = self.width
		height = self.height

		self.image = pygame.Surface([width, height])
		self.image.fill(purple)
		self.image.set_colorkey(purple)
		self.rect = self.image.get_rect()
		pygame.draw.ellipse(self.image, color, [0,0,width, height])		

		self.rect = self.image.get_rect()

		self.screenheight = pygame.display.get_surface().get_height()
		self.screenwidth = pygame.display.get_surface().get_width()

		self.reset()

	def reset(self): # initial random conditions
		self.x = random.randrange(10,630)
		self.y = 120

		self.direction = random.randrange(-45,45)

	def bounce(self): # ball bounces off walls
		self.direction = (180-self.direction)%360

	def update(self):
		width = 640
		height = 480

		direction_rad = math.radians(self.direction)

		self.x += math.sin(direction_rad)
		self.y += math.cos(direction_rad)

		if self.y < 0: # this is the top! Make the ball bounce off
			self.y = 0 
			self.direction = (180-self.direction)%360

		if self.y > self.screenheight: # this is the bottom! End the game
			done = True
			font = pygame.font.Font(None, 60)
			text = font.render("Game Over", 1, black)
			textpos = (200, 200)
			screen.blit(text, textpos)

		self.rect.x = self.x
		self.rect.y = self.y

		# keep the ball within walls 
		if self.x < self.width:
			self.direction = (360 - self.direction)%360.0

  		if self.x > width - self.width:
			self.direction = (360 - self.direction)%360.0

class PlayerBrick(pygame.sprite.Sprite):
	"""Creates dimensions, visual details and controls 
	movement of the paddle/player's brick"""
	def __init__(self):
		super(PlayerBrick, self).__init__()
		self.width = 100 # width of bottom brick
		self.height = 15 # height of bottom brick
		self.image = pygame.Surface([self.width, self.height])
		self.image.fill((green))	

		self.rect = self.image.get_rect()
		self.screenheight = pygame.display.get_surface().get_height()
		self.screenwidth = pygame.display.get_surface().get_width()

		self.rect.x = 320
		self.rect.y = 400

	def update(self):
		#update the balls position with keyboard input
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.rect.x -= 10
		if keys[pygame.K_RIGHT]:
			self.rect.x += 10
		if self.rect.x > self.screenwidth - self.width:
			self.rect.x = self.screenwidth - self.width
		if self.rect.x < 0:
			self.rect.x = 0

# initialize
pygame.init()
screen = pygame.display.set_mode([640,480])
pygame.display.set_caption('Brick Breaker')
Background = pygame.Surface(screen.get_size())

sound_background = pygame.mixer.Sound('starwarstheme.wav')
sound_background.play( -1)


# Create sprites and sprite groups to collide
ball = Ball(red)
balls = pygame.sprite.Group()
balls.add(ball)

player = PlayerBrick()
players = pygame.sprite.Group()
players.add(player)

moving_things = pygame.sprite.Group() # group of everything that is moving
moving_things.add(ball)
moving_things.add(player)

to_be_broken = pygame.sprite.Group() # group of bricks to be broken

class Level(pygame.sprite.Sprite):
	"""Creates new bricks for each level"""	
	def __init__(self):
		super(Level, self).__init__()
	def reset_bricks(self): 
		""" resets the bricks randomly by color and position 
		each level"""
		BRICKS = []
		for i in range(0,8, 2):
			j = random.randrange(1,4)
			for k in range(1,j):
				non_moving_brick = Nonmoving_brick((random.randint(0,255),random.randint(0,255),random.randint(0,255)), 80 * i, 60*j)
				non_moving_brick2 = Nonmoving_brick((random.randint(0,255),random.randint(0,255),random.randint(0,255)), 80 * (i+1), 60*j)
				BRICKS.append(non_moving_brick)
				BRICKS.append(non_moving_brick2)

				non_moving_brick3 = Nonmoving_brick((random.randint(0,255),random.randint(0,255),random.randint(0,255)), 80 * i, 93)
				non_moving_brick4 = Nonmoving_brick((random.randint(0,255),random.randint(0,255),random.randint(0,255)), 80 * (i+1), 93)	
				BRICKS.append(non_moving_brick3)
				BRICKS.append(non_moving_brick4)

				to_be_broken.add(BRICKS)

# Initial conditions
score = 0
CurrentLevel = 1

clock = pygame.time.Clock()
done = False
exit_program = False

level = Level()
level.reset_bricks()
pygame.display.flip()

counting_levels = 5

while exit_program != True:
	clock.tick(200)

	screen.blit(Background, (0,0))
	galaxyback = pygame.image.load("galaxies.jpg")
	get_galaxy = galaxyback.get_rect()
	screen.blit(galaxyback, get_galaxy)

	for event in pygame.event.get(): # for every collision
		if event.type == pygame.QUIT:
			exit_program = True
	if len(to_be_broken) == 0: # if you've cleared all the bricks
		done = True
	if not done:
		player.update()
		ball.update()
	if done:
		counting_levels -=1
		time.delay(1000)
		score = 0
		if counting_levels > 0: # if you still have more levels
			CurrentLevel += 1
			done = False
			level.reset_bricks()
		elif counting_levels == 0: # if you've cleared all 5 levels
			font = pygame.font.Font(None, 60)
			text = font.render("Congrats! You've Won!", 1, white)
			textpos = (80, 200)
			screen.blit(text, textpos)
			done = True
			counting_levels -= 1
		else: # end after you've cleared all the levels
			time.delay(3000)
			pygame.QUIT()

	""" handles collisions between ball, player, bricks, removes
	bricks when they're hit"""
	if pygame.sprite.spritecollide(player, balls, False):
		ball.bounce()

	if pygame.sprite.spritecollide(ball,to_be_broken,True):
		ball.bounce()
		score+=1

	# print current stats
	font = pygame.font.Font(None, 36)
	scoreprint = "Score: "+ str(score) + "     " + "Level: " + str(CurrentLevel)
	text = font.render(scoreprint, 1, white)
	textpos = (30, 30)

	# redraw everything
	screen.blit(text,textpos)
	moving_things.draw(screen)
	to_be_broken.draw(screen)
	pygame.display.flip()

pygame.quit()