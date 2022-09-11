import pygame 
import functions
from math import cos,sin,radians

class DefeatedExploding():
    def __init__(self,x,y,window,enemy="exploding enemy"):
        self.window=window
        self.window.score+=1*self.window.strength
        self.x=x
        self.y=y
        self.draw_angle=0        
        if self.window.x>self.window.w/2:
            self.move_angle=radians(functions.random(-75,-45))
            self.rotation=functions.random(-30,-10)
        else:
            self.move_angle=radians(functions.random(-135,-105))
            self.rotation=functions.random(10,30)
        
        self.speed=functions.random(15,20)
        self.gravity_change=functions.random(0.2,0.4)
        self.gravity=0
        self.added_size=0
        self.enemy=enemy
        
    def update(self):
        self.draw_angle+=self.rotation
        self.added_size+=0.2
        
        self.x+=cos(self.move_angle)*self.speed
        self.y+=sin(self.move_angle)*self.speed
        
        self.y+=self.gravity
        self.gravity+=self.gravity_change
        
        if self.window.keys[self.window.right]:
            self.x-=5
        if self.window.keys[self.window.left]:
            self.x+=5
        
    def draw(self):
        functions.draw(self.enemy,self.x-self.window.camerax+self.window.shakex,self.y-self.window.cameray+self.window.shakey,angle=self.draw_angle,size=(self.added_size+40,self.added_size+40))
        
class DefeatedFlying():
    def __init__(self,x,y,window):
        self.window=window
        self.window.score+=1*self.window.strength
        self.x=x
        self.y=y
        self.speed=functions.random(10,15)
        self.gravity_change=functions.random(0.5,1)
        self.gravity=0
        self.added_size=0
        
    def update(self):
        self.added_size+=0.4
        
        self.y-=self.speed
        self.y+=self.gravity
        self.gravity+=self.gravity_change
        
        if self.window.keys[self.window.right]:
            self.x-=5
        if self.window.keys[self.window.left]:
            self.x+=5
        
    def draw(self):
        functions.draw("flying enemy",self.x-self.window.camerax+self.window.shakex,self.y-self.window.cameray+self.window.shakey,size=(self.added_size+40,self.added_size+40))