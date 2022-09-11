import pygame 
import functions
from math import sin
from bomb import Bomb

class Exploding(): #Charges towards player, explodes on contact
    def __init__(self,window):
        self.window=window
        if functions.random(1,2)==1:
            self.x=self.window.w+self.window.camerax+300
        else:
            self.x=-self.window.w-self.window.camerax-300
        self.y=self.window.h*0.6-40
        self.rect=pygame.Rect(self.x,self.y,40,40)
        self.flashtime=0
        self.hp=40*self.window.strength
        self.explode=0
        self.colour="red"
        self.type="exploding"
        self.explode_damage=40
        
        #self.id=self.window.id
        #print(self.id)
        
    def update(self):
        if self.x>self.window.w/2:
            self.x-=6
        else:
            self.x+=6
            
        if self.window.keys[self.window.right]:
            self.x-=5
        if self.window.keys[self.window.left]:
            self.x+=5
    
        if self.rect.colliderect(self.window.player.rect):
            self.explode=1 #tells the game to delete self
        
        self.rect.x=self.x-self.window.camerax+self.window.shakex
        self.rect.y=self.y-self.window.cameray+self.window.shakey
        
        if self.flashtime>0:
            self.flashtime-=1
            self.colour=pygame.Color("white")
        else:
            self.colour=pygame.Color("red")
        
    def draw(self):
        pygame.draw.rect(self.window.surface,self.colour,self.rect)
        
        #functions.write(self.id,0,0,30,center=self.rect,font="font2")
        
class Flying(): #Flies above player, throwing explosives
    def __init__(self,window):
        self.window=window
        if functions.random(1,2)==1:
            self.x=self.window.w+self.window.camerax+300
        else:
            self.x=-self.window.w-self.window.camerax-300
        self.y=functions.random(self.window.h*-0.4,self.window.h*0.3)
        self.rect=pygame.Rect(self.x,self.y,40,40)
        self.flashtime=0
        self.hp=20*self.window.strength
        self.colour="yellow"
        self.timer=0
        self.type="flying"
        self.fire_timer=0
        self.range=functions.random(250,350)
        self.explode=0
        self.explode_damage=20
        
    def update(self):
        if abs(self.x-self.window.w/2)>self.range:
            self.fire_timer=0
            if self.x>self.window.w/2:
                self.x-=2
            else:
                self.x+=2
        else:
            self.fire_timer+=1/60
        
        if self.rect.colliderect(self.window.player.rect):
            self.explode=1 #tells the game to delete self
                
        self.timer+=0.08
        self.y+=sin(self.timer)*4
            
        if self.window.keys[self.window.right]:
            self.x-=5
        if self.window.keys[self.window.left]:
            self.x+=5
        
        self.rect.x=self.x-self.window.camerax+self.window.shakex
        self.rect.y=self.y-self.window.cameray+self.window.shakey
        
        if self.flashtime>0:
            self.flashtime-=1
            self.colour=pygame.Color("white")
        else:
            self.colour=pygame.Color("yellow")
        
    def draw(self):
        pygame.draw.rect(self.window.surface,self.colour,self.rect)
        
class Laser(): #Shoots a horizontal laser when dies
    def __init__(self,window):
        self.window=window
        if functions.random(1,2)==1:
            self.x=self.window.w+self.window.camerax+300
        else:
            self.x=-self.window.w-self.window.camerax-300
        self.y=self.window.h*0.6-40
        self.rect=pygame.Rect(self.x,self.y,40,40)
        self.flashtime=0
        self.hp=60*self.window.strength
        self.explode=0
        self.colour="dark green"
        self.type="laser"
        self.explode_damage=60
        
    def update(self):
        if self.x>self.window.w/2:
            self.x-=4
        else:
            self.x+=4
            
        if self.window.keys[self.window.right]:
            self.x-=5
        if self.window.keys[self.window.left]:
            self.x+=5
    
        if self.rect.colliderect(self.window.player.rect):
            self.explode=1 #tells the game to delete self
        
        self.rect.x=self.x-self.window.camerax+self.window.shakex
        self.rect.y=self.y-self.window.cameray+self.window.shakey
        
        if self.flashtime>0:
            self.flashtime-=1
            self.colour=pygame.Color("white")
        else:
            self.colour=pygame.Color("dark green")
        
    def draw(self):
        pygame.draw.rect(self.window.surface,self.colour,self.rect)
        
class Tank(): #Becomes stronger by explosives
    def __init__(self,window):
        self.window=window
        if functions.random(1,2)==1:
            self.x=self.window.w+self.window.camerax+300
        else:
            self.x=-self.window.w-self.window.camerax-300
        self.y=self.window.h*0.6-40
        self.rect=pygame.Rect(self.x,self.y,40,40)
        self.flashtime=0
        self.hp=100*self.window.strength
        self.explode=0
        self.colour="purple"
        self.type="tank"
        self.explode_damage=0
        
    def update(self):
        self.explode_damage=40+round(self.hp/5)
        if self.x>self.window.w/2:
            self.x-=2
        else:
            self.x+=2
            
        if self.window.keys[self.window.right]:
            self.x-=5
        if self.window.keys[self.window.left]:
            self.x+=5
    
        if self.rect.colliderect(self.window.player.rect):
            self.explode=1 #tells the game to delete self
            
        self.rect=pygame.Rect(self.x-self.window.camerax+self.window.shakex,self.y-self.window.cameray+self.window.shakey-round(self.hp/5),40+round(self.hp/5),40+round(self.hp/5))
        
        if self.flashtime>0:
            self.flashtime-=1
            self.colour=pygame.Color("white")
        else:
            self.colour=pygame.Color("purple")
        
    def draw(self):
        pygame.draw.rect(self.window.surface,self.colour,self.rect)
        
        #functions.write(self.id,0,0,30,center=self.rect,font="font2")