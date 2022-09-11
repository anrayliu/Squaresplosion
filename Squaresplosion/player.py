import pygame
import functions

class Player():
    def __init__(self,window):
        self.x=0
        self.y=0
        self.window=window
        self.jump=0
        self.rect=pygame.Rect(self.x,self.y,30,70)
        self.y_vel=-10
        self.hp=255 #hp starts at 255 because that's max rgb value - adds pizazz
        
    def update(self):
        if self.window.can_move==1:
            if self.window.keys[self.window.up]:
                if self.jump==0:
                    self.jump=1
                    self.y_vel=10
            if self.window.keys[self.window.left]:
                self.x+=5
            if self.window.keys[self.window.right]:
                self.x-=5
            
        self.y+=self.y_vel
        self.y_vel-=0.4
        if self.y<0:
            self.y=0
            self.jump=0
        
        self.rect.x=self.window.w/2-15-self.window.camerax+self.window.shakex
        self.rect.y=self.window.h*0.6-70-self.y-self.window.cameray+self.window.shakey
        
    def draw(self):
        pygame.draw.rect(self.window.surface,pygame.Color("blue"),self.rect)           