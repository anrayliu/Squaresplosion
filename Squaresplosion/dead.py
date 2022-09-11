import pygame 
import functions
from time import time
from math import floor

class Dead():
    def __init__(self,window):
        self.window=window 
        self.back_button=functions.Button(window.w*0.03,window.h*0.1,200,100,50,"Back")
        self.colour1=functions.random(0,255)
        self.colour2=functions.random(0,255)
        self.colour3=functions.random(0,255)
        
    def update(self):
        self.back_button.update()
        if self.back_button.click==1:
            self.window.transition("menu","dead")
        
    def draw(self):
        self.window.surface.fill(pygame.Color("black"))
        functions.draw("game over",0,0)
        self.header_rect=pygame.Rect(functions.rounded_rectangle(0,self.window.h*0.1,self.window.w*0.6,self.window.h*0.2,80,center="x",return_info=1))
        functions.write("GAME OVER",0,0,100,center=self.header_rect)
        self.back_button.draw()
        
        functions.rounded_rectangle(0,self.window.h*0.35,self.window.w*0.3,self.window.h*0.4,60,center="x")
        
        functions.write("Shots fired: {}".format(self.window.bullets_shot),0,self.window.h*0.4,40,center="x")
        functions.write("Explosive enemies killed: {}".format(self.window.red_shot),0,self.window.h*0.45,40,center="x")
        functions.write("Flying enemies killed: {}".format(self.window.yellow_shot),0,self.window.h*0.5,40,center="x")
        functions.write("Tank enemies killed: {}".format(self.window.tank_shot),0,self.window.h*0.55,40,center="x")
        functions.write("Laser enemies killed: {}".format(self.window.laser_shot),0,self.window.h*0.6,40,center="x")
        functions.write("Time survived: {}:{}:{}".format(floor(self.survived_time/3600),floor((self.survived_time-floor(self.survived_time/3600)*3600)/60),self.survived_time-floor(self.survived_time/3600)*3600-floor((self.survived_time-floor(self.survived_time/3600)*3600)/60)*60),0,self.window.h*0.65,40,center="x")
        if self.new_highscore==1:
            functions.write("Highscore: {}".format(self.window.highscore),0,self.window.h*0.75,40,center="x",colour="blue")
        else:
            functions.write("Highscore: {}".format(self.window.highscore),0,self.window.h*0.75,40,center="x")
        functions.write("Score: {}".format(round(self.window.score*10)),0,self.window.h*0.8,40,center="x")
        
        self.colour1+=functions.random(1,10)
        if self.colour1>255:
            self.colour1=0
        self.colour2+=functions.random(1,10)
        if self.colour2>255:
            self.colour2=0
        self.colour3+=functions.random(1,10)
        if self.colour3>255:
            self.colour3=0
        
        if self.new_highscore==1:
            info=functions.write("NEW!",-self.window.w*0.25,0,80,center="middle",colour=(self.colour1,self.colour2,self.colour3),return_info=1,write=0)
            functions.write("NEW!",-self.window.w*0.25-info[0]/2,0,80,center="middle",colour=(self.colour1,self.colour2,self.colour3))
            functions.write("NEW!",self.window.w*0.25,0,80,center="middle",colour=(self.colour1,self.colour2,self.colour3))
    
    def run(self):
        self.running=1
        self.window.show_cursor=1
        self.window.cursor_image="cursor"
        self.survived_time=round(time()-self.window.start_time)
        if round(self.window.score*10)>self.window.highscore:
            self.window.highscore=round(self.window.score*10)
            self.new_highscore=1
        else:
            self.new_highscore=0
            
        while (self.running):
            self.window.get_events()
            if self.window.escape_pressed==1 and self.window.can_escape==1:
                self.running=0
                self.window.execute("menu")
            self.update()
            self.draw()
            self.window.update_screen()