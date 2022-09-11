import pygame
import functions
from math import atan2,cos,sin,degrees,radians

class Bullet():
    def __init__(self,window,enemies):
        self.window=window
        self.startx=self.window.w/2
        self.starty=self.window.h*0.6-70-self.window.player.y
        self.can_hit=1
        
        self.angle=atan2(self.window.y-self.starty,self.window.x-self.startx) #Angle in radians
        self.angle=radians(degrees(self.angle)+functions.random(-3,3))
        
        self.speed=10
        self.x=self.startx
        self.y=self.starty
        self.alpha=275
        
        self.startx+=cos(self.angle)*130 #Moves the starting point so that it matches the gun sprite
        self.starty+=sin(self.angle)*130
        
        self.breakk=0 #For some off reason, self.break throughs an error, whereas self.breakk is fine
        while (self.x>self.window.w*2 or self.x<-self.window.w  or self.y<-self.window.h or self.y>self.window.h*0.6)==False:
            self.x+=cos(self.angle)*self.speed
            self.y+=sin(self.angle)*self.speed
                        
            for enemy in enemies:
                if enemy.rect.collidepoint((self.x-self.window.camerax+self.window.shakex,self.y-self.window.cameray+self.window.shakey)):
                    self.breakk=1
                    enemy.hp-=40
                    enemy.flashtime=10 #how many frames it will flash white
                    '''
                    if self.window.x>self.window.w/2: knockback
                        enemy.x+=80
                    else:
                        enemy.x-=80'''
                    self.enemy_hit=enemy
                    
                    if enemy.type=="tank":
                        functions.play_sound(functions.random_from(("thud1","thud2")))
            
            if self.breakk==1:
                self.can_hit=0
                break
        
    def update(self):
        if self.window.keys[self.window.right]:
            self.x-=5
            self.startx-=5
        if self.window.keys[self.window.left]:
            self.x+=5
            self.startx+=5
        
        self.alpha-=20
                
    def draw(self):
        '''
        for i in functions.init.alpha_surfaces:
            if int(i)==self.alpha:
                pygame.draw.line(functions.init.alpha_surfaces[i],pygame.Color("red"),(self.x-self.window.camerax,self.y-self.window.cameray),(self.startx-self.window.camerax,self.starty-self.window.cameray),3)
                self.window.surface.blit(functions.init.alpha_surfaces[i],(0,0))
                break'''
        #alpha trails
                
        pygame.draw.line(self.window.surface,pygame.Color("red"),(self.x-self.window.camerax,self.y-self.window.cameray),(self.startx-self.window.camerax,self.starty-self.window.cameray),3)