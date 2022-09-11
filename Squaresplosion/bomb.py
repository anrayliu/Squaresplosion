import pygame
import functions
from math import atan2,cos,sin,degrees,radians

class Bomb(): #dropped by flying enemies
    def __init__(self,x,y,window):
        self.window=window
        self.x=x
        self.y=y
        self.type="bomb"
        
        if self.x>self.window.w/2:
            self.angle=radians(functions.random(-250,-160))
        else:
            self.angle=radians(functions.random(-380,-290))
        
        self.speed=5
        self.gravity=0
        
    def update(self):
        self.x+=cos(self.angle)*self.speed 
        self.y+=sin(self.angle)*self.speed
        self.y+=self.gravity
        self.gravity+=0.4
                
        if self.window.keys[self.window.right]:
            self.x-=5
        if self.window.keys[self.window.left]:
            self.x+=5
            
        self.rect=pygame.Rect(self.x-self.window.camerax+self.window.shakex-15,self.y-self.window.cameray+self.window.shakey-15,30,30)
                        
    def draw(self):
        pygame.draw.circle(self.window.surface,pygame.Color("white"),(self.x-self.window.camerax+self.window.shakex,self.y-self.window.cameray+self.window.shakey),15)
        pygame.draw.circle(self.window.surface,pygame.Color("black"),(self.x-self.window.camerax+self.window.shakex,self.y-self.window.cameray+self.window.shakey),5)
        
class Missile(): #shot by green cubes
    def __init__(self,x,y,window):
        self.window=window
        self.x=x
        self.y=y
        self.type="missile"
        
    def update(self):
        if self.direction=="right":
            self.x+=20
        else:
            self.x-=20

        if self.window.keys[self.window.right]:
            self.x-=5
        if self.window.keys[self.window.left]:
            self.x+=5
            
        self.rect=pygame.Rect(self.x-self.window.camerax+self.window.shakex,self.y-self.window.cameray+self.window.shakey,30,30)
                        
    def draw(self):
        self.rect=pygame.Rect(self.x-self.window.camerax+self.window.shakex,self.y-self.window.cameray+self.window.shakey,30,30)
        pygame.draw.circle(self.window.surface,pygame.Color("green3"),(self.rect[0]+15,self.rect[1]+15),15)
        #pygame.draw.rect(self.window.surface,pygame.Color("dark green"),self.rect)