import pygame
import functions
from math import cos,sin,radians,degrees,atan2

class CircleParticle():
    def __init__(self,x,y,window,size,stroke):
        self.x=x
        self.y=y
        self.window=window
        self.stroke_size=functions.random(stroke[0],stroke[1])
        self.radius=functions.random(size[0],size[1])
        self.type="circle"
        
    def update(self):
        self.stroke_size-=0.5
        self.radius+=5
        
        if self.window.keys[self.window.right]:
            self.x-=5
        if self.window.keys[self.window.left]:
            self.x+=5
            
    def draw(self):
        pygame.draw.circle(self.window.surface,pygame.Color("white"),(self.x-self.window.camerax+self.window.shakex,self.y-self.window.cameray+self.window.shakey),self.radius,round(self.stroke_size))
        
class DebrisParticle():
    def __init__(self,x,y,window,angle,gravity,speed,colour,size):
        self.x=x
        self.y=y
        self.window=window 
        self.angle=radians(functions.random(angle[0],angle[1]))
        self.gravity=0
        self.gravity_change=functions.random(gravity[0],gravity[1])
        self.speed=speed
        self.size=size
        self.colour=colour
        self.type="debris"
        
    def update(self):
        self.x+=cos(self.angle)*self.speed
        self.y+=sin(self.angle)*self.speed
        
        self.y+=self.gravity
        self.gravity+=self.gravity_change
        
        if self.window.can_move==1:
            if self.window.keys[self.window.right]:
                self.x-=5
            if self.window.keys[self.window.left]:
                self.x+=5
            
    def draw(self):
        pygame.draw.circle(self.window.surface,pygame.Color(self.colour),(self.x-self.window.camerax+self.window.shakex,self.y-self.window.cameray+self.window.shakey),self.size)

class ShellParticle():
    def __init__(self,window):
        self.window=window
        self.x=self.window.w/2+self.distance_from_middle()
        self.y=self.window.h/2-self.window.player.y
        self.angle=atan2(self.window.y-self.y,self.window.x-self.x)
        self.direction=functions.random(70,110)

        self.gravity=0
        self.type="shell"
        
    def update(self):
        self.x+=cos(radians(self.direction))*10
        self.y-=10
        
        self.y+=self.gravity
        self.gravity+=1
        
        if self.window.keys[self.window.right]:
            self.x-=5
        if self.window.keys[self.window.left]:
            self.x+=5
            
    def draw(self):
        #pygame.draw.circle(self.window.surface,pygame.Color("white"),(self.x-self.window.camerax,self.y-self.window.cameray),3)
        functions.draw("shell",self.x-self.window.camerax+self.window.shakex,self.y-self.window.cameray+self.window.shakey,angle=360-degrees(self.angle))
        
    def distance_from_middle(self):
        if abs(self.window.x-self.window.w/2)>50:
            if self.window.x>self.window.w/2:
                return 50
            else:
                return -50
        else:
            return self.window.x-self.window.w/2
            
class Rain():
    def __init__(self,window,x_change,y_change):
        self.window=window
        self.x=functions.random(self.window.w*-0.5,self.window.w*1.5)
        self.y=functions.random(self.window.h*-0.5,self.window.h*1.5)
        self.x_change=x_change
        self.y_change=y_change
    def update(self):
        self.y+=self.y_change
        self.x+=self.x_change
        if self.y>self.window.h*1.5:
            self.y=self.window.h*-0.5
        if self.x<self.window.w*-0.5:
            self.x=self.window.w*1.5
        elif self.x>self.window.w*1.5:
            self.x=self.window.w*-0.5
    def draw(self):
        pygame.draw.line(self.window.surface,pygame.Color("blue"),(self.x-self.window.camerax,self.y-self.window.cameray),(self.x+self.x_change-self.window.camerax,self.y+self.y_change-self.window.cameray),3)

class ShotParticle():
    def __init__(self,window):
        self.window=window
        self.x=self.window.w/2
        self.y=self.window.h*0.6-70-self.window.player.y
        self.life_time=10
        self.type="shot"
        
        self.angle=atan2(self.window.y-self.y,self.window.x-self.x)
        
        self.x+=cos(self.angle)*130
        self.y+=sin(self.angle)*130
        
    def update(self):
        self.life_time-=1

    def draw(self):
        pass
        #functions.draw("shot",self.x-self.window.camerax+self.window.shakex,self.y-self.window.cameray+self.window.shakey,angle=360-degrees(self.angle))

class LineParticle():
    def __init__(self,x,y,window,angle,length,speed,colour,thickness):
        self.x=x
        self.y=y
        self.window=window 
        self.angle=radians(functions.random(angle[0],angle[1]))
        self.speed=functions.random(speed[0],speed[1])
        self.thickness=functions.random(thickness[0],thickness[1])
        self.colour=colour
        self.type="line"
        self.length=functions.random(length[0],length[1])
        
    def update(self):
        self.x+=cos(self.angle)*self.speed
        self.y+=sin(self.angle)*self.speed
        self.length-=1
        self.thickness-=1        
        
        if self.window.can_move==1:
            if self.window.keys[self.window.right]:
                self.x-=5
            if self.window.keys[self.window.left]:
                self.x+=5
            
    def draw(self):
        pygame.draw.line(self.window.surface,pygame.Color(self.colour),(self.x-self.window.camerax+self.window.shakex,self.y-self.window.cameray+self.window.shakey),(self.x-self.window.camerax+self.window.shakex+cos(self.angle)*self.length,self.y-self.window.cameray+self.window.shakey+sin(self.angle)*self.length),self.thickness)