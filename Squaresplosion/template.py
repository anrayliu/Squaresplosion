import pygame 
import functions

class Template():
    def __init__(self,window):
        self.window=window 
        
    def update(self):
        pass
        
    def draw(self):
        self.window.surface.fill(pygame.Color("green"))
    
    def run(self):
        self.running=1
        while (self.running):
            self.window.get_events()
            if self.window.escape_pressed==1 and self.window.can_escape==1:
                self.window.quit()
            self.update()
            self.draw()
            self.window.update_screen()