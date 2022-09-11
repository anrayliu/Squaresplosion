import pygame
import functions

class SongButton():
    def __init__(self,song,x,y,window,list):
        self.song=song 
        self.x=x
        self.y=y
        self.window=window
        self.list=list
        self.select=0
        
    def update(self):
        self.rect=pygame.Rect(self.x,self.y,200,50)
        if self.rect.colliderect(self.window.cursor_rect):
            if self.select==0:
                functions.play_sound("select2")
                self.select=1
        else:
            self.select=0
        
    def draw(self):
        self.rect=pygame.Rect(self.x,self.y,200,50)
        if self.window.selected_song==(self.song,self.list):
            pygame.draw.rect(self.window.surface,pygame.Color("blue"),self.rect)
            if self.window.click==1 and self.window.can_click==1 and self.rect.collidepoint(self.window.x,self.window.y):
                self.window.selected_song=None
        elif self.rect.collidepoint((self.window.x,self.window.y)):
            pygame.draw.rect(self.window.surface,pygame.Color("yellow"),self.rect)
            if self.window.can_click==1 and self.window.click==1:
                self.window.selected_song=(self.song,self.list)
        else:
            pygame.draw.rect(self.window.surface,pygame.Color("dark green"),self.rect)
        functions.write(self.song,0,0,40,center=self.rect)