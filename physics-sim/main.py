# Author: Andrew Tissi
# Date: 5/22/21

import pygame#imports the pygame library
import random#imports the random library
import math
class ball:
	def __init__(self,surface,x,y,_id):
		self._id=_id
		self.surface=surface
		self.radius=10
		self.mode="Create"
		self.startX=x
		self.startY=y
		self.default_radius=10
		self.x=self.startX
		self.y=self.startY
		self.vx=0
		self.vy=0
		self.a=1
		self.w=surface.get_width()
		self.h=surface.get_height()
		self.f=0
		self.borderX=self.startX
		self.borderY=self.startY

	def draw(self):
		pygame.draw.circle(self.surface, (255, 255, 255), (self.x, self.y), self.radius)
		if self.mode=="Create":
			pygame.draw.aaline(self.surface,(0,255,0),(self.startX,self.startY),(self.borderX,self.borderY))

	def expand(self,x,y):
		if self.mode=="Create":
			self.borderX=x
			self.borderY=y
			newrad=math.hypot(self.startX-self.borderX,self.startY-self.borderY)
			if newrad>=self.default_radius:
				self.radius=newrad

	def fall(self):
		if self.mode=="FreeFall":
			self.vy+=self.a
			self.y+=self.vy
			self.x-=self.vx
			self.vx-=self.vx*self.f
			self.vy-=self.vy*self.f
	
	def colision(self,balllist):
		if self.mode=="FreeFall":
			if self.y>=self.h-self.radius:
				self.vy*=-1
				self.y=self.h-self.radius
			if self.y<=self.radius:
				self.vy*=-1
				self.y=self.radius
			if self.x<=self.radius:
				self.vx*=-1
				self.x=self.radius
			if self.x>=self.w-self.radius:
				self.vx*=-1
				self.x=self.w-self.radius
			for i in balllist:
				if i.mode=="FreeFall":
					if i._id!=self._id:
						# xcomp=i.x-self.x
						# ycomp=i.y-self.y
						# # if -(self.radius+i.radius)<=xcomp<=(self.radius+i.radius) and -(self.radius+i.radius)<=ycomp<=(self.radius+i.radius):
						# distance=math.hypot(xcomp,ycomp)

						v1 = pygame.math.Vector2(self.x, self.y)
						v2 = pygame.math.Vector2(i.x, i.y)

						# if distance <= self.radius + i.radius:
						if v1.distance_to(v2) < self.radius + i.radius - 2:
							nv = v2 - v1
							m1 = pygame.math.Vector2(self.vx, self.vy).reflect(nv)
							m2 = pygame.math.Vector2(i.vx, i.vy).reflect(nv)
							self.vx, self.vy = m1.x, m1.y
							i.vx, i.vy = m2.x, m2.y
							


							# self.vf=math.hypot(self.vy,self.vx)
							# self.theta=math.asin(abs(ycomp)/abs(distance)) *180/math.pi
							# print(self.theta)
							# if i.y>self.y:#main up
							# 	self.vy=-1*(math.cos(self.theta)*self.vf)
							# 	i.vy=(math.cos(self.theta)*self.vf)
							# if i.y==self.y:
							# 	self.vy*=-1
							# 	i.vy*=-1
							# if i.y<self.y:#main down
							# 	self.vy=(math.cos(self.theta)*self.vf)
							# 	i.vy=-1*(math.cos(self.theta)*self.vf)
							# if i.x>self.x:#main left
							# 	self.vx=-1*(math.sin(self.theta)*self.vf)
							# 	i.vx=(math.sin(self.theta)*self.vf)
							# if i.x==self.x:
							# 	self.vx*=-1
							# 	i.vx*=-1
							# if i.x<self.x:#main right
							# 	self.vx=(math.sin(self.theta)*self.vf)
							# 	i.vx=-1*(math.sin(self.theta)*self.vf)



							# if i.x>self.x:
							# 		#right
							# 	if i.y>self.y:
							# if i.x<self.x:
									#left


				
w = 600#creates the width for the screen
h = 500#creates the height for the screen

screen = pygame.display.set_mode((w, h))#creates the screen
clock = pygame.time.Clock()#creates the clock
balllist=[]
running=1
created=0
while running:#runs while the snake has more than 0 lives
	screen.fill((0, 0, 0))#fills the screen black

	for event in pygame.event.get():#loops through every event
		mouse1=pygame.mouse.get_pressed()[0]
		
		if event.type == pygame.QUIT:#checks if the user wnats to quit
			running=0
		elif event.type == pygame.KEYDOWN:#checks if the user presses a key
			pass
		elif event.type == pygame.MOUSEBUTTONDOWN:
			print("created")
			x,y=event.pos
			b=ball(screen,x,y,random.randint(0,1000000))
			created=1
			balllist.append(b)
		elif event.type == pygame.MOUSEMOTION and created==1:
			print("motion")
			x,y=event.pos
			b.expand(x,y)
		elif event.type == pygame.MOUSEBUTTONUP and created==1:
			created=0
			print("let go")
			b.mode="FreeFall"

	for i in balllist:
		i.draw()
		i.fall()
		i.colision(balllist)
	pygame.display.flip()#draws everything to the screen
	clock.tick(60)#delays, draws once every 60ms