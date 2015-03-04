import math
import pygame
import random

red = (255,0,0)
green = (0,255,63)
purple = (238,130,238)
white = (0,0,0)

# collision between ball and wall different between ball and bottom wall, ball and brick

class Ball(pygame.sprite.Sprite):
	def __init__(self,color):
		super(Ball, self).__init__()

		self.width = 20
		self.height = 20
		width = self.width
		height = self.height



		self.image = pygame.Surface([width, height])
		# circle = pygame.Surface([width,height])
		# circle = circle.convert()
		self.image.fill(purple)
		self.image.set_colorkey(purple)
		self.rect = self.image.get_rect()
		pygame.draw.ellipse(self.image, color, [0,0,width, height])
		# circle.set_colorkey(circle.get_at((0,0)),pygame.RLEACCEL)
		

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

		if self.y < self.height:
			self.y = height
			self.direction = random.randrange(-45,45)
		if self.y > height:
			self.y = height - self.height
			self.direction = (self.direction + 90)%360.0
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
			self.rect.x -= 20
		if keys[pygame.K_RIGHT]:
			self.rect.x += 20
		if self.rect.x > self.screenwidth - self.width:
			self.rect.x = self.screenwidth - self.width
		if self.rect.x < self.width:
			self.rect.x = self.width

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

# to_be_broken = pygame.sprite.Group()
# to_be_broken.add(Nonmoving_brick)



score = 0 

clock = pygame.time.Clock()
done = False
exit_program = False
while exit_program != True:
	clock.tick(30)

	pygame.display.update()
	screen.blit(Background, (0,0))
	# my_particles = []
	# my_particles.clear(screen, Background)


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit_program = True
	if score == 10:
		done = True
	if not done:
		player.update()
		ball.update()
	if done:
		text = font.render("Game Over", 1, (200,200,200))
		textpos = text.get_rect(centerx = background.get_width()/2)
		textpos.top = 50
		screen.blit(text, textpos)

	if pygame.sprite.spritecollide(player, balls, False):

		# ball.y = 40
		ball.bounce()
		score +=1

	# if pygame.sprite.spritecollide(ball,nonmoving_bricks,True):
	

	screen.fill(purple)
	moving_things.draw(screen)
	pygame.display.flip()


pygame.quit()