import pygame 
import functions
from time import time
from math import floor

class Chest():
    def __init__(self,window):
        self.window=window 
        self.angle=0
        self.select=0
        
    def update(self):
        self.angle+=0.01
        self.time_left=round(self.window.chest_time-time())
        if self.time_left<0:
            self.time_left=0
        self.hours=floor(self.time_left/3600)
        self.minutes=floor((self.time_left-self.hours*3600)/60)
        self.seconds=self.time_left-self.hours*3600-self.minutes*60
        
        if self.window.click==1 and self.window.can_click==1 and self.rect.colliderect(self.window.cursor_rect) and self.time_left==0:
            self.window.chest_time=time()+28800
            self.window.save()
        
        self.rect=pygame.Rect(self.window.w-300,self.window.h-(250+(self.time_left==0)*50),200,200-(self.time_left!=0)*50)
        if self.rect.colliderect(self.window.cursor_rect):
            self.colour=1
            if self.select==0:
                functions.play_sound("select")
                self.select=1
        else:
            self.colour=0
            self.select=0
        
    def draw(self):
        if self.time_left==0:
            functions.draw("glow",self.rect[0]+self.rect[2]/2,self.rect[1]+self.rect[3]/2,angle=self.angle*50)
            functions.draw("open{}".format(self.colour),self.rect[0],self.rect[1])
            functions.write("Ready!",0,-150,40,center=self.rect)
        else:
            functions.draw("closed{}".format(self.colour),self.rect[0],self.rect[1])
            functions.write("{}:{}:{}".format(self.hours,self.minutes,self.seconds),0,-150,30,center=self.rect,font="font1")
    