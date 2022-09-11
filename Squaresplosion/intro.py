import pygame
import functions

class Intro():
    def __init__(self,window):
        self.window=window
        self.running=0

    def update(self):
        self.timer+=0.0125
        if self.timer>3:
            self.alpha+=self.alpha_change
            if self.timer>6.5:
                self.running=0
                self.window.execute("menu")
            if self.alpha>255:
                self.alpha_change=-2
                self.timer=0
        if self.alpha==256 and self.play_sound==1 and self.timer>1.5:
            functions.play_sound("intro")
            self.play_sound=0
            self.glide_change=20

        self.glide-=self.glide_change
        
        if self.window.keys[pygame.K_SPACE]:
            self.running=0
            self.window.execute("menu")
        
    def draw(self):
        self.window.surface.fill(pygame.Color("black"))
        functions.write("Ree1261",0,0,80,alpha=self.alpha,center="middle",font="font3")
        pygame.draw.line(self.window.surface,pygame.Color("black"),(self.glide,0),(self.glide,self.window.h),50)

    def run(self):
        self.running=1
        self.timer=0
        self.alpha=0
        self.alpha_change=2
        self.play_sound=1
        self.glide=self.window.w
        self.glide_change=0
        
        while (self.running):
            self.window.get_events()
            if self.window.escape_pressed==1 and self.window.can_escape==1:
                self.window.quit()
                
            self.update()
            self.draw()
            
            self.window.update_screen()
