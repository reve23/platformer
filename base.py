import pygame
from pygame.locals import *
import sys
import random

pygame.init()
vec = pygame.math.Vector2 # 2 for two dimentional

height = 450
width = 400
acc = 0.5
fric = -0.12
fps = 60

frame_per_sec = pygame.time.Clock()
display_surface = pygame.display.set_mode((width,height))
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.surf = pygame.Surface((30,30))
		self.surf.fill((128,255,40))
		self.rect = self.surf.get_rect()

	#physics
		self.pos = vec((10,360))
		self.vel = vec(0,0)
		self.acc = vec(0,0)

	def move(self):
		self.acc = vec(0,0.5)
		pressed_keys = pygame.key.get_pressed()

		if pressed_keys[K_LEFT]:
			self.acc.x = -acc
		if pressed_keys[K_RIGHT]:
			self.acc.x = acc
		self.acc.x += self.vel.x * fric
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		# you can “go through” the left side of the screen, and pop up on the right side.
		if self.pos.x > width:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = width
		self.rect.midbottom = self.pos
	#collision detection
	def update(self):
		hits = pygame.sprite.spritecollide(player1,platforms,False)
		if player1.vel.y > 0:
			if hits:
				self.pos.y = hits[0].rect.top +1
				self.vel.y = 0

	#jumping mechanics
	def jump(self):
		hits = pygame.sprite.spritecollide(self,platforms,False)
		if hits:
			self.vel.y = -15



class Platform(pygame.sprite.Sprite):
	def  __init__(self):
		super().__init__()
		self.surf = pygame.Surface((random.randint(50,100),12))
		self.surf.fill((0,255,0))
		self.rect = self.surf.get_rect(center=(random.randint(0,width-10),random.randint(0,height-30)))
	def move(self):
		pass

platform1 = Platform()
player1 = Player()

platforms = pygame.sprite.Group()
platforms.add(platform1)

all_sprites = pygame.sprite.Group()
all_sprites.add(platform1)
all_sprites.add(player1)

platform1.surf = pygame.Surface((width,20))
platform1.surf.fill((255,0,0))
platform1.rect = platform1.surf.get_rect( center = (width/2,height-10))

for x in range(random.randint(5,6)):
	pl = Platform()
	platforms.add(pl)
	all_sprites.add(pl)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		#making jump button
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player1.jump()


	display_surface.fill((0,0,0))
	player1.move()

	if player1.rect.top <= height / 3:
		player1.pos.y += abs(player1.vel.y)
		for plat in platforms:
			plat.rect.y += abs(player1.vel.y)
			if plat.rect.top >= height:
				plat.kill()

	for entity in all_sprites:
		display_surface.blit(entity.surf,entity.rect)
		entity.move()

	pygame.display.update()
	frame_per_sec.tick(fps)
