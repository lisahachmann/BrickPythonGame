import math
import pygame
import random
from pygame import *
if not pygame.font: print 'Warning, fonts disabled'
red = (255,0,0)
green = (0,255,63)
purple = (238,130,238)
black = (0,0,0)
white = (255, 255, 255)

# collision between ball and wall different between ball and bottom wall, ball and brick

class Nonmoving_brick(pygame.sprite.Sprite):
	def __init__(self, color, xpos, ypos):
		super(Nonmoving_brick, self).__init__()
		self.width = 80
		self.height = 30
		width = self.width
		height = self.height

		self.image = pygame.Surface([width, height])
		self.image.fill((red))	

		self.rect = self.image.get_rect()
		self.screenheight = pygame.display.get_surface().get_height()
		self.screenwidth = pygame.display.get_surface().get_width()

		self.rect.x = xpos
		self.rect.y = ypos

		# self.image = pygame.Surface([width, height])
		# self.image.fill(red)
		# self.rect = self.image.get_rect()
		# #def draw_bricks(self):
		# rect = pygame.Rect((80,0),(80,30))
		# pygame.draw.rect(self.image, red, rect, 2)

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
		self.y = 50.0

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
			self.direction = (self.direction + 90)%360.0
		if self.y > self.screenheight: # this is the bottom!
			self.direction = (self.direction - 90)%360.0
			self.y = self.screenheight - self.width

		self.rect.x = self.x
		self.rect.y = self.y

		if self.x < self.width:
			self.direction = (360 - self.direction)%360.0
		if self.x > width - self.width:
			self.direction = (360 - self.direction)%360.0

class PlayerBrick(pygame.sprite.Sprite):
	def __init__(self):
		super(PlayerBrick, self).__init__()
		self.width = 50 # width of bottom brick
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

# nonmoving_bricks = Nonmoving_brick(red, 60, 40)

BRICKS = []
for i in range(0,5):
	non_moving_brick = Nonmoving_brick(red, 90 * i, 60 )
	BRICKS.append(non_moving_brick)

to_be_broken = pygame.sprite.Group()
# to_be_broken.add(nonmoving_bricks)
to_be_broken.add(BRICKS)

score = 0 

clock = pygame.time.Clock()
done = False
exit_program = False


#textpos.centerx = Background.get_rect().centerx
#Background.blit(text, textpos)

pygame.display.flip()
while exit_program != True:
	clock.tick(100)
	font = pygame.font.Font(None, 36)
	text = font.render("Score: ", 1, black)
	textpos = text.get_rect()
	screen.blit(Background, (0,0))
	screen.blit(text,textpos)
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit_program = True
	if score == 10:
		done = True
	if not done:
		player.update()
		ball.update()
		screen.blit(text, textpos)
	if done:
		font = pygame.font.Font(None, 40)
		endtext = font.render("Game Over", 1, black)
		endtextpos = text.get_rect()
		screen.blit(endtext, endtextpos)

	if pygame.sprite.spritecollide(player, balls, False):
		ball.bounce()
		score +=1

	if pygame.sprite.spritecollide(ball,to_be_broken,True):
		ball.bounce()
		score+=1

	#score_text = RenderText(score_text, "./fonts/newfont.ttf", 20, black)
	screen.fill(purple)
	moving_things.draw(screen)
	#RenderText.print_text(score_text, "./fonts/newfont.ttf", 20, black)
	#score_text.print_text()
	to_be_broken.draw(screen)
	pygame.display.flip()


pygame.quit()