import pygame
from pygame.locals import *
import sys
import time
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
		self.jumping  = False
		self.score = 0

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
		if self.vel.y > 0:
			if hits:
				if self.pos.y < hits[0].rect.bottom:
					if hits[0].point == True:
						hits[0].point == False
						self.score += 1
					self.pos.y = hits[0].rect.top +1
					self.vel.y = 0
					self.jumping = False

	#jumping mechanics
	def jump(self):
		hits = pygame.sprite.spritecollide(self,platforms,False)
		if hits and not self.jumping:
			self.vel.y = -15
			self.jumping = True

	def cancel_jump(self):
		if self.jumping:
			if self.vel.y < -3:
				self.vel.y = -3


class Platform(pygame.sprite.Sprite):
	def  __init__(self):
		super().__init__()
		self.surf = pygame.Surface((random.randint(50,100),12))
		self.surf.fill((0,255,0))
		self.rect = self.surf.get_rect(center=(random.randint(0,width-10),random.randint(0,height-30)))
		self.moving = True
		self.point = True
	def move(self):
		pass
	#random platform generation

def plat_gen():
	while len(platforms) < 7:
		Width = random.randrange(50,100)
		p = Platform()
		C = True
		while C:
			p = Platform()
			p.rect.center = (random.randrange(0,width - Width),random.randrange(-50,0))
			C = check(p,platforms)
		platforms.add(p)
		all_sprites.add(p)	

def check(platform,groupies):
	if pygame.sprite.spritecollideany(platform,groupies):
		return True
	else:
		for entity in groupies:
			if entity == platform:
				continue
			if (abs(platform.rect.top - entity.rect.bottom) < 50) and (abs(platform.rect.bottom - entity.rect.top)<50):
				return True
		C = False

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
platform1.moving = False
platform1.point = False

for x in range(random.randint(5,6)):
	pl = Platform()
	platforms.add(pl)
	all_sprites.add(pl)  

while True:
	#check for inputs
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		#making jump button
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player1.jump()
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				player1.cancel_jump()

	display_surface.fill((0,0,0))
	f = pygame.font.SysFont("Verdana",20)
	g = f.render(str(player1.score),True,(123,255,0))
	display_surface.blit(g,(width/2,10))
	player1.update()
	plat_gen()
	if player1.rect.top <= height / 3:
		player1.pos.y += abs(player1.vel.y)
		for plat in platforms:
			plat.rect.y += abs(player1.vel.y)
			if plat.rect.top >= height:
				plat.kill()
	if player1.rect.top >height:
		for entity in all_sprites:
			entity.kill()
			time.sleep(1)
			display_surface.fill((255,0,0))
			pygame.display.update()
			time.sleep(1)
			pygame.quit()
			sys.exit()

	for entity in all_sprites:
		display_surface.blit(entity.surf,entity.rect)
		entity.move()

	pygame.display.update()
	frame_per_sec.tick(fps)
