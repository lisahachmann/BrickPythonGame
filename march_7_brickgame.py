import math
import pygame
import random
import time
print time
from pygame import *
if not pygame.font: print 'Warning, fonts disabled'
red = (255,0,0)
green = (0,255,63)
purple = (238,130,238)
black = (0,0,0)
white = (255, 255, 255)
blue = (8, 146, 208)

# collision between ball and wall different between ball and bottom wall, ball and brick

class Level1Nonmoving_brick(pygame.sprite.Sprite):
	def __init__(self, color, xpos, ypos):
		super(Level1Nonmoving_brick, self).__init__()
		self.width = 77
		self.height = 30
		width = self.width
		height = self.height
		self.image = pygame.Surface([width, height])
		self.image.fill((color))	

		self.rect = self.image.get_rect()
		self.screenheight = pygame.display.get_surface().get_height()
		self.screenwidth = pygame.display.get_surface().get_width()

		self.rect.x = xpos
		self.rect.y = ypos

class Ball(pygame.sprite.Sprite):
	def __init__(self,color):
		super(Ball, self).__init__()

		self.width = 20
		self.height = 20
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
		# self.x = 320
		# self.y = 400

		self.reset()

	def reset(self): # initial random conditions
		self.x = random.randrange(10,630)
		self.y = 120

		self.direction = random.randrange(-45,45)

	def bounce(self):
		self.direction = (180-self.direction)%360

	def update(self):
		width = 640
		height = 480

		direction_rad = math.radians(self.direction)

		self.x += math.sin(direction_rad)
		self.y += math.cos(direction_rad)

		if self.y < 0: # this is the top!
			self.y = 0
			self.direction = (180-self.direction)%360

		if self.y > self.screenheight: # this is the bottom!
			done = True
			font = pygame.font.Font(None, 60)
			text = font.render("Game Over", 1, black)
			textpos = (200, 200)
			screen.blit(text, textpos)

		self.rect.x = self.x
		self.rect.y = self.y

		if self.x < self.width:
			self.direction = (360 - self.direction)%360.0
		if self.x > width - self.width:
			self.direction = (360 - self.direction)%360.0

class PlayerBrick(pygame.sprite.Sprite):
	def __init__(self):
		super(PlayerBrick, self).__init__()
		self.width = 640 # width of bottom brick
		self.height = 20 # height of bottom brick
		self.image = pygame.Surface([self.width, self.height])
		self.image.fill((green))	
		# pygame.key.get_pressed() = key # this is possibly completet bullshit

		self.rect = self.image.get_rect()
		self.screenheight = pygame.display.get_surface().get_height()
		self.screenwidth = pygame.display.get_surface().get_width()

		self.rect.x = 320
		self.rect.y = 400

	def update(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.rect.x -= 10
		if keys[pygame.K_RIGHT]:
			self.rect.x += 10
		if self.rect.x > self.screenwidth - self.width:
			self.rect.x = self.screenwidth - self.width
		if self.rect.x < 0:
			self.rect.x = 0



pygame.init()
screen = pygame.display.set_mode([640,480])
pygame.display.set_caption('Brick Breaker')

Background = pygame.Surface(screen.get_size())


ball = Ball(red)
balls = pygame.sprite.Group()
balls.add(ball)

player = PlayerBrick()
players = pygame.sprite.Group()
players.add(player)

moving_things = pygame.sprite.Group()
moving_things.add(ball)
moving_things.add(player)

to_be_broken = pygame.sprite.Group()

class Level(pygame.sprite.Sprite):
	def __init__(self):
		super(Level, self).__init__()
	def reset_bricks(self):
		BRICKS = []

		for i in range(0,8, 2):
			j = random.randrange(1,4)
			for k in range(1,j):
				non_moving_brick = Level1Nonmoving_brick(red, 80 * i, 60*j)
				non_moving_brick2 = Level1Nonmoving_brick(blue, 80 * (i+1), 60*j)
				BRICKS.append(non_moving_brick)
				BRICKS.append(non_moving_brick2)

				non_moving_brick3 = Level1Nonmoving_brick(blue, 80 * i, 93)
				non_moving_brick4 = Level1Nonmoving_brick(red, 80 * (i+1), 93)	
				BRICKS.append(non_moving_brick3)
				BRICKS.append(non_moving_brick4)

				to_be_broken.add(BRICKS)

score = 0 

clock = pygame.time.Clock()
done = False
exit_program = False

level = Level()
level.reset_bricks()
pygame.display.flip()

counting_levels = 2

while exit_program != True:
	clock.tick(500)

	screen.blit(Background, (0,0))

	screen.fill(purple)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit_program = True
	if len(to_be_broken) == 0:
		done = True
	if not done:
		player.update()
		ball.update()
		#screen.blit(text, textpos)
	if done:
		counting_levels -=1
		level.reset_bricks()
		time.delay(1000)
		score = 0
		if counting_levels > 0:
			done = False
		# if counting_levels == 0:
		else:
			font = pygame.font.Font(None, 60)
			text = font.render("Congrats!", 1, black)
			textpos = (200, 200)
			screen.blit(text, textpos)
			done = True
			time.delay(2000)
			# pygame.QUIT()
		# else:
		# 	done = False

	if pygame.sprite.spritecollide(player, balls, False):
		ball.bounce()

	if pygame.sprite.spritecollide(ball,to_be_broken,True):
		ball.bounce()
		score+=1

	font = pygame.font.Font(None, 36)
	scoreprint = "Score: "+ str(score)
	text = font.render(scoreprint, 1, black)
	textpos = (30, 30)
	screen.blit(text,textpos)
	moving_things.draw(screen)
	to_be_broken.draw(screen)
	pygame.display.flip()

pygame.quit()