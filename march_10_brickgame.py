import math
import pygame
from pygame import mixer
import random
import time
from pygame import *
if not pygame.font: print 'Warning, fonts disabled'
red = (255,0,0)
green = (0,255,63)
purple = (238,130,238)
black = (0,0,0)
white = (255, 255, 255)
blue = (8, 146, 208)
# collision between ball and wall different between ball and bottom wall, ball and brick

class Nonmoving_brick(pygame.sprite.Sprite):
	"""Creates dimensions and visual details for the bricks that will be hit with a ball and then eliminated"""
	def __init__(self, color, xpos, ypos):
		super(Nonmoving_brick, self).__init__()
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
		"""Creates dimensions and visual details for the moving ball"""
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

		self.reset()

	def reset(self): 
	# initial random conditions of ball start position
		self.x = random.randrange(10,630)
		self.y = 120
		self.direction = random.randrange(-45,45)

	def bounce(self):
		#how the ball bounces
		self.direction = (180-self.direction)%360

	def update(self):
		#update the ball position
		width = 640
		height = 480
		direction_rad = math.radians(self.direction)
		self.x += math.sin(direction_rad)
		self.y += math.cos(direction_rad)

		if self.y < 0: 
			# if ball hits the top make it reverse direction
			self.y = 0
			self.direction = (180-self.direction)%360

		if self.y > self.screenheight: 
			#if ball hits the bottom, Game is Over
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
	"""Creates dimensions, visual details and controls movement of the paddle/player's brick"""
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

class Level(pygame.sprite.Sprite):
	"""Creates new bricks for each level"""
	def __init__(self):
		super(Level, self).__init__()

	def reset_bricks(self):
		#empty list of bricks
		BRICKS = []

		for i in range(0,8, 2):
			#create bricks in every two spots
			j = random.randrange(1,4)
			for k in range(1,j):
				#create random amounts of bricks
				non_moving_brick = Nonmoving_brick((random.randint(0,255),random.randint(0,255),random.randint(0,255)), 80 * i, 60*j)
				non_moving_brick2 = Nonmoving_brick((random.randint(0,255),random.randint(0,255),random.randint(0,255)), 80 * (i+1), 60*j)
				non_moving_brick3 = Nonmoving_brick((random.randint(0,255),random.randint(0,255),random.randint(0,255)), 80 * i, 93)
				non_moving_brick4 = Nonmoving_brick((random.randint(0,255),random.randint(0,255),random.randint(0,255)), 80 * (i+1), 93)	

				BRICKS.append(non_moving_brick)
				BRICKS.append(non_moving_brick2)
				BRICKS.append(non_moving_brick3)
				BRICKS.append(non_moving_brick4)
				#add to sprite group
				to_be_broken.add(BRICKS)

#Outside code that uses classes in pygame
pygame.init()
#screen initialization
screen = pygame.display.set_mode([640,480])
pygame.display.set_caption('Brick Breaker')
Background = pygame.Surface(screen.get_size())
#Sprites
#ball initialization into sprite
ball = Ball(red)
balls = pygame.sprite.Group()
balls.add(ball)
#paddle/playerbrick initialization into sprite
player = PlayerBrick()
players = pygame.sprite.Group()
players.add(player)
#intializes movement of ball and sprite
moving_things = pygame.sprite.Group()
moving_things.add(ball)
moving_things.add(player)
#creates sprite group for bricks
to_be_broken = pygame.sprite.Group()

#game startpoints
score = 0
CurrentLevel = 1
clock = pygame.time.Clock()
done = False
exit_program = False
home_page = True
level = Level()
level.reset_bricks()
pygame.display.flip()
counting_levels = 5

while exit_program == False and home_page == True:
	print "IN HOME PAGE"
  	keyboard = pygame.key.get_pressed()
  	print keyboard
  	print pygame.K_UP
  	if keyboard[pygame.K_UP]:
  		print 'press'
  		home_page = False
  		exit_program = False
  	else:
  		"key not detected"
 	 	intro_title = "Brick Breaker"
 	 	font = pygame.font.Font(None, 40)
 	 	text = font.render(intro_title, 1, white)
 	 	textpos = (100, 100)
 	 	screen.blit(Background, (0,0))
 	 	galaxyback = pygame.image.load("galaxies.jpg")
 	 	get_galaxy = galaxyback.get_rect()
 	 	screen.blit(galaxyback, get_galaxy)
 	 	screen.blit(text, textpos)
 	 	import time
 	 	time.sleep(5)
 	 	home_page = False

while exit_program != True: #and home_page != True:
	clock.tick(200)
	screen.blit(Background, (0,0))
	#creates sound background
	sound_background = pygame.mixer.Sound('starwarstheme.wav')
	sound_background.play(-1)
	#image background
	galaxyback = pygame.image.load("galaxies.jpg")
	get_galaxy = galaxyback.get_rect()
	screen.blit(galaxyback, get_galaxy)
	for event in pygame.event.get():
		#be able to exit pygame
		if event.type == pygame.QUIT:
			exit_program = True
	if len(to_be_broken) == 0:
		#if all bricks have been broken
		done = True
	if not done:
		#keep game updated
		player.update()
		ball.update()
	if done:
		counting_levels -=1
		time.delay(1000)
		score = 0
		if counting_levels > 0:
			#go to the next level
			CurrentLevel += 1
			done = False
			level.reset_bricks()
		elif counting_levels == 0:
			#you've finished all the levels so display Congrats and finish
			font = pygame.font.Font(None, 60)
			text = font.render("Congrats! You've Won!", 1, white)
			textpos = (80, 200)
			screen.blit(text, textpos)
			done = True
			counting_levels -= 1
		else:
			#this theoretically never happens, but just in case of errors. 
			time.delay(3000)
			pygame.QUIT()

	if pygame.sprite.spritecollide(player, balls, False):
		#When the paddle/player hits the ball
		ball.bounce()

	if pygame.sprite.spritecollide(ball,to_be_broken,True):
		#When the ball hits a brick (and brick disappears)
		ball.bounce()
		score+=1
	#Render the Score and Level to the screen during gameplay"
	font = pygame.font.Font(None, 36)
	scoreprint = "Score: "+ str(score) + "     " + "Level: " + str(CurrentLevel)
	text = font.render(scoreprint, 1, white)
	textpos = (30, 30)
	screen.blit(text,textpos)
	#Draw each of these groups
	moving_things.draw(screen)
	to_be_broken.draw(screen)
	pygame.display.flip()



pygame.quit()